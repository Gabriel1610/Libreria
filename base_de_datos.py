import mysql.connector
from datetime import datetime
import subprocess
import configparser
import logging
import time

NOMBRE_ARCHIVO_CONFIG = 'config.ini'
CANT_CONDICIONES = 4
MÁX_INTENTOS = 5

class BaseDeDatos:

    def abrir(self):
        """
        Abre una conexión a la base de datos MySQL utilizando la configuración
        del archivo 'config.ini'.

        Returns:
            mysql.connector.connection.MySQLConnection: Un objeto de conexión a la base de datos.
                Retorna la conexión abierta si la conexión es exitosa.

        Raises:
            mysql.connector.Error: Si ocurre algún error durante la conexión
                                   (credenciales incorrectas, servidor no disponible, etc.).
                                   Es IMPORTANTE capturar esta excepción en el código
                                   que llama a esta función.

        """
        # Obtiene un logger para esta clase.  El nombre suele ser __name__ (el nombre del módulo).
        logger = logging.getLogger(__name__)
        config = self.obtener_configuración()  # Obtiene la configuración desde el archivo .ini
        hostt = config['database']['host']      # Lee el host del archivo de configuración
        usuario = config['database']['user']    # Lee el usuario
        contraseña = config['database']['password'] # Lee la contraseña
        base_de_datos = config['database']['database'] # Lee el nombre de la base de datos

        # Intenta establecer la conexión.  Es crucial manejar los posibles errores aquí.
        try:
            conexión = mysql.connector.connect(host=hostt, 
                                               user=usuario, 
                                               passwd=contraseña, 
                                               database=base_de_datos
                                               )
            logger.info("Conexión a la base de datos establecida exitosamente.")  # Mensaje de éxito
            return conexión # Retorna la conexión abierta
        except mysql.connector.Error as err:
            logger.exception("Error al conectar a la base de datos:")  # Usamos exception para el traceback
            raise  # Relanzamos la excepción.
    
    def obtener_configuración(self):
        """
        Lee la configuración de la base de datos desde el archivo 'config.ini'.

        Returns:
            configparser.ConfigParser: Un objeto ConfigParser con la configuración leída.

        Raises:
            FileNotFoundError: Si el archivo 'config.ini' no se encuentra.
            configparser.Error: Si hay algún problema al parsear el archivo de configuración.
                                 (formato incorrecto, sección faltante, etc.).

        """
        config = configparser.ConfigParser()
        try:
            config.read(NOMBRE_ARCHIVO_CONFIG, encoding='utf-8')  # Lee el archivo
            if not config.sections():  # Verifica si el archivo está vacío o no contiene secciones.
                raise configparser.Error(f"El archivo de configuración '{NOMBRE_ARCHIVO_CONFIG}' está vacío o no tiene secciones.")

            #Verificar que las secciones y opciones necesarias existan
            if 'database' not in config:
                raise configparser.Error("Falta la sección 'database' en el archivo de configuración.")
            required_options = ['host', 'user', 'password', 'database']
            for option in required_options:
                if option not in config['database']:
                    raise configparser.Error(f"Falta la opción '{option}' en la sección 'database' del archivo de configuración.")

        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de configuración '{NOMBRE_ARCHIVO_CONFIG}'.")
            raise
        except configparser.Error as e:
            print(f"Error al leer el archivo de configuración: {e}")
            raise

        return config

    def ingresarProducto(self, datos, intentos=MÁX_INTENTOS):
        """
        Ingresa un nuevo producto en la tabla PRODUCTO.
        Maneja reintentos en caso de deadlock.

        Args:
            datos (list): Una lista con los datos del producto en el orden:
                          [codigo, nombre, descripcion, precio_venta, 
                           stock_actual, stock_minimo]
            intentos (int): Número máximo de reintentos en caso de deadlock.
        """
        intento = 0
        logger = logging.getLogger(__name__)  # Obtener el logger para este módulo
        reintentar = True
        
        # Declarar cursor y conexión fuera del try para que existan en el finally
        conexión = None
        cursor = None

        while intento < intentos and reintentar:
            try:
                conexión = self.abrir()  # Abrir la conexión
                cursor = conexión.cursor()
                
                # Consulta adaptada a la tabla PRODUCTO
                # (El orden de columnas coincide con la lista 'producto' de Programa.py)
                consulta = """INSERT INTO PRODUCTO(codigo, nombre, descripcion, precio_venta, stock_actual, stock_minimo)
                              VALUES(%s, %s, %s, %s, %s, %s);
                           """
                
                cursor.execute(consulta, datos)
                conexión.commit()  # confirmar la transacción
                reintentar = False
                logger.info(f"Producto '{datos[1]}' (Código: {datos[0]}) ingresado exitosamente.")

            except mysql.connector.errors.InternalError as err:
                intento += 1
                if err.errno == 1213:  # Deadlock
                    logger.warning(f"Deadlock detectado al ingresar producto. Intento {intento}/{intentos}.")
                    if intento < intentos:
                        time.sleep(1)  # espera antes de reintentar
                        continue
                    else:
                        logger.error("No se pudo resolver el deadlock después de varios intentos.")
                        raise
                else:
                    raise  # Relanzar otros InternalError

            except mysql.connector.Error as err:
                # Error 1062: Violación de restricción UNIQUE (código duplicado)
                if err.errno == 1062: 
                    mensaje_error = f"Error: Ya existe un producto con ese código. (Detalle: {err.msg})"
                    logger.warning(mensaje_error)
                    
                    # Lanza un error simple que la UI pueda capturar
                    raise ValueError(f"Ya existe un producto con ese código.")
                # --- FIN NUEVA LÓGICA ---
                else:
                    # Registra cualquier otro error de MySQL
                    logger.exception("Error de MySQL durante el ingreso del producto:")
                    raise # Relanza la excepción original si no es la 1062

            except Exception as e:
                # Registra cualquier otro error inesperado
                logger.exception("Error inesperado durante el ingreso del producto:")
                raise

            finally:
                # Este bloque se ejecuta siempre, haya habido error o no
                if cursor:
                    # Cierra el cursor si fue creado
                    cursor.close()
                    logger.debug("Cursor cerrado.")
                if conexión and conexión.is_connected():
                    # Cierra la conexión a la base de datos si está abierta
                    conexión.close()
                    logger.info("Conexión a la base de datos cerrada.")

    def buscarProductoPorCódigo(self, código):
        """
        Busca un producto en la tabla PRODUCTO usando su 'código' único.

        Args:
            código (str): El código del producto a buscar.

        Returns:
            tuple: Una tupla con los datos del producto si se encuentra:
                   (codigo, nombre, descripcion, precio_venta, 
                    stock_actual, stock_minimo)
            None: Si no se encuentra el producto o si ocurre un error.
        """
        logger = logging.getLogger(__name__)  # Obtener el logger
        conexión = None
        cursor = None

        try:
            conexión = self.abrir()  # Abrir la conexión
            cursor = conexión.cursor()
            
            consulta = """SELECT codigo, nombre, 
                                 precio_venta, stock_actual, stock_minimo, descripcion, id_producto
                          FROM PRODUCTO
                          WHERE codigo = %s;
                       """
            
            # Ejecutar la consulta pasando el 'código' como una tupla
            cursor.execute(consulta, (código,))
            
            # Obtener el único resultado (o None si no se encontró)
            producto = cursor.fetchone() 
            
            if producto:
                logger.info(f"Producto encontrado con código: {código}.")
            else:
                logger.warning(f"No se encontró ningún producto con código: {código}.")
                
            return producto # Devuelve la tupla del producto o None

        except mysql.connector.Error as err:
            # Registra un error específico de MySQL
            logger.exception(f"Error de MySQL durante la búsqueda del producto con código {código}:")
            return None

        except Exception as e:
            # Registra cualquier otro error inesperado
            logger.exception(f"Error inesperado durante la búsqueda del producto con código {código}:")
            return None

        finally:
            # Este bloque se ejecuta siempre
            if cursor:
                cursor.close()
                logger.debug("Cursor cerrado.")
            if conexión and conexión.is_connected():
                conexión.close()
                logger.info("Conexión a la base de datos cerrada.")

    def buscarProductoPorNombre(self, nombre):
        """
        Busca productos en la tabla PRODUCTO cuyo nombre contenga el término de búsqueda.
        La búsqueda ignora mayúsculas y minúsculas.

        Args:
            nombre (str): El término de búsqueda para el nombre del producto.

        Returns:
            list: Una lista de tuplas con los datos de los productos encontrados.
                  El orden de las tuplas es:
                  (codigo, nombre, precio_venta, stock_actual, 
                   stock_minimo, descripcion, id_producto)
            None: Si ocurre un error.
        """
        logger = logging.getLogger(__name__)  # Obtener el logger
        conexión = None
        cursor = None

        try:
            conexión = self.abrir()  # Abrir la conexión
            cursor = conexión.cursor()
            
            # Prepara el término de búsqueda para SQL LIKE (case-insensitive)
            # Añadimos '%' para que busque 'nombre' en cualquier parte de la cadena
            término_búsqueda = f"%{nombre.lower()}%"

            # Consulta para seleccionar productos por nombre (case-insensitive y contenido)
            # El orden de las columnas coincide con 'consultarDatosProductos'
            consulta = """SELECT codigo, nombre, precio_venta, stock_actual, 
                                 stock_minimo, descripcion, id_producto
                          FROM PRODUCTO
                          WHERE LOWER(nombre COLLATE utf8mb4_bin) LIKE %s
                          ORDER BY nombre; 
                       """
            
            # Ejecutar la consulta pasando el término de búsqueda
            cursor.execute(consulta, (término_búsqueda,))
            
            productos = cursor.fetchall() # Obtener todos los resultados
            
            if productos:
                logger.info(f"Se encontraron {len(productos)} productos con el nombre '{nombre}'.")
            else:
                # Esto no es un error, simplemente no hubo coincidencias
                logger.info(f"No se encontró ningún producto que contenga '{nombre}'.")
                
            return productos # Devuelve la lista de productos (puede estar vacía)

        except mysql.connector.Error as err:
            # Registra un error específico de MySQL
            logger.exception(f"Error de MySQL durante la búsqueda por nombre '{nombre}':")
            return None # Devuelve None en caso de error

        except Exception as e:
            # Registra cualquier otro error inesperado
            logger.exception(f"Error inesperado durante la búsqueda por nombre '{nombre}':")
            return None # Devuelve None en caso de error

        finally:
            # Este bloque se ejecuta siempre
            if cursor:
                cursor.close()
                logger.debug("Cursor cerrado.")
            if conexión and conexión.is_connected():
                conexión.close()
                logger.info("Conexión a la base de datos cerrada.")

    def buscarProductoPorDescripción(self, descripción):
        """
        Busca productos en la tabla PRODUCTO cuya descripción contenga el término de búsqueda.
        La búsqueda ignora mayúsculas y minúsculas.

        Args:
            descripción (str): El término de búsqueda para la descripción del producto.

        Returns:
            list: Una lista de tuplas con los datos de los productos encontrados.
                  El orden de las tuplas es:
                  (codigo, nombre, precio_venta, stock_actual, 
                   stock_minimo, descripcion, id_producto)
            None: Si ocurre un error.
        """
        logger = logging.getLogger(__name__)  # Obtener el logger
        conexión = None
        cursor = None

        try:
            conexión = self.abrir()  # Abrir la conexión
            cursor = conexión.cursor()
            
            # Prepara el término de búsqueda para SQL LIKE (case-insensitive)
            # Añadimos '%' para que busque 'descripción' en cualquier parte de la cadena
            término_búsqueda = f"%{descripción.lower()}%"

            # Consulta para seleccionar productos por descripción (case-insensitive y contenido)
            # El orden de las columnas coincide con 'consultarDatosProductos'
            consulta = """SELECT codigo, nombre, precio_venta, stock_actual, 
                                 stock_minimo, descripcion, id_producto
                          FROM PRODUCTO
                          WHERE LOWER(descripcion COLLATE utf8mb4_bin) LIKE %s
                          ORDER BY nombre; 
                       """
            
            # Ejecutar la consulta pasando el término de búsqueda
            cursor.execute(consulta, (término_búsqueda,))
            
            productos = cursor.fetchall() # Obtener todos los resultados
            
            if productos:
                logger.info(f"Se encontraron {len(productos)} productos con la descripción '{descripción}'.")
            else:
                # Esto no es un error, simplemente no hubo coincidencias
                logger.info(f"No se encontró ningún producto que contenga '{descripción}'.")
                
            return productos # Devuelve la lista de productos (puede estar vacía)

        except mysql.connector.Error as err:
            # Registra un error específico de MySQL
            logger.exception(f"Error de MySQL durante la búsqueda por descripción '{descripción}':")
            return None # Devuelve None en caso de error

        except Exception as e:
            # Registra cualquier otro error inesperado
            logger.exception(f"Error inesperado durante la búsqueda por descripción '{descripción}':")
            return None # Devuelve None en caso de error

        finally:
            # Este bloque se ejecuta siempre
            if cursor:
                cursor.close()
                logger.debug("Cursor cerrado.")
            if conexión and conexión.is_connected():
                conexión.close()
                logger.info("Conexión a la base de datos cerrada.")
    
    def consultarDetalleVenta(self, id_venta):
        """
        Consulta todos los detalles (productos, cantidades, precios)
        asociados con un id_venta específico.

        Utiliza un JOIN para obtener el código y nombre del producto.
        Calcula el subtotal (cantidad * precio_unitario) para cada fila.

        Args:
            id_venta (int): El ID de la venta a consultar.

        Devuelve:
            list: Una lista de tuplas, donde cada tupla es un detalle de la venta:
                  (codigo_producto, nombre_producto, precio_unitario, cantidad, subtotal)
            None: Si ocurre un error.
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None
        
        try:
            # 1. Abre la conexión a la base de datos
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            # 2. Consulta SQL con JOIN para obtener detalles legibles
            consulta = """
                SELECT
                    P.codigo,
                    P.nombre,
                    DV.precio_unitario,
                    DV.cantidad,
                    ROUND((DV.cantidad * DV.precio_unitario), 2) AS subtotal
                FROM
                    DETALLE_VENTA AS DV
                JOIN
                    PRODUCTO AS P ON DV.id_producto = P.id_producto
                WHERE
                    DV.id_venta = %s;
            """
            
            # 3. Ejecución de la consulta (pasamos el id_venta como tupla)
            cursor.execute(consulta, (id_venta,))
            filas = cursor.fetchall()
            logger.info(f"Se consultaron {len(filas)} detalles para la Venta ID: {id_venta}.")
            return filas
        
        except mysql.connector.Error as err:
            logger.exception(f"Error de MySQL al consultar detalles de Venta ID: {id_venta}:")
            return None
        except Exception as e:
            # 4. Manejo de excepciones
            logger.exception(f"Error inesperado al consultar detalles de Venta ID: {id_venta}: {e}")
            return None

        finally:
            # 5. Asegura que la conexión se cierre
            if cursor:
                cursor.close()
                logger.debug("Cursor cerrado.")
            if 'conexión' in locals() and conexión and conexión.is_connected():
                conexión.close()
                logger.info("Conexión a la base de datos cerrada.")

    def consultarProductosPorPorcentajeStock(self):
        """
        Consulta y devuelve productos ordenados por el porcentaje de
        stock actual sobre el stock mínimo, de menor a mayor.

        Incluye todos los productos, incluso aquellos con stock >= 100%.
        Los productos con stock_minimo = 0 se envían al final de la lista.

        Returns:
            list: Una lista de tuplas con los datos del producto:
                  (codigo, nombre, precio_venta, stock_actual, stock_minimo)
                  Retorna None si ocurre un error.
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None
        
        try:
            # 1. Abre la conexión a la base de datos
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            # 2. Base de la consulta SQL
            # Se calcula el ratio (stock_actual / stock_minimo)
            # Se usa CASE para evitar la división por cero si stock_minimo es 0.
            # Esos productos (con min_stock=0) se tratan como "infinitamente"
            # seguros y se envían al final de la lista (ASC).
            consulta = """SELECT 
                             codigo,
                             stock_actual, 
                             stock_minimo, 
                             nombre
                          FROM 
                             PRODUCTO
                          ORDER BY
                             CASE
                                 WHEN stock_minimo = 0 THEN 9999999.99
                                 ELSE (stock_actual / stock_minimo)
                             END ASC;
                       """
            
            # 3. Ejecución de la consulta
            cursor.execute(consulta)
            filas = cursor.fetchall()
            logger.info(f"Se consultaron {len(filas)} productos (ordenados por % stock).")
            return filas
        
        except mysql.connector.Error as err:
            logger.exception("Error de MySQL al consultar productos por porcentaje de stock:")
            return None
        except Exception as e:
            # 4. Manejo de excepciones
            logger.exception(f"Error inesperado al consultar productos por porcentaje de stock: {e}")
            return None

        finally:
            # 5. Asegura que la conexión se cierre
            if cursor:
                cursor.close()
                logger.debug("Cursor cerrado.")
            if 'conexión' in locals() and conexión and conexión.is_connected():
                conexión.close()
                logger.info("Conexión a la base de datos cerrada.")

    def consultarDatosProductos(self):
        """
        Consulta y devuelve todos los productos de la tabla PRODUCTO.

        Los datos se devuelven en el orden esperado por el Treeview de la UI:
        (codigo, nombre, precio_venta, stock_actual, stock_minimo, descripcion)

        Returns:
            list: Una lista de tuplas, donde cada tupla es un producto.
                  Retorna None si ocurre un error.
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None
        
        try:
            # 1. Abre la conexión a la base de datos
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            # 2. Base de la consulta SQL
            # Seleccionamos las columnas en el orden que espera la tabla (Treeview)
            # (Según tu función crearTablaConProductos, el precio va antes del stock)
            consulta = """SELECT codigo, 
                                 nombre, 
                                 precio_venta, 
                                 stock_actual, 
                                 stock_minimo, 
                                 descripcion,
                                 id_producto
                          FROM PRODUCTO
                          ORDER BY nombre; 
                       """
            
            # 3. Ejecución de la consulta
            cursor.execute(consulta)
            filas = cursor.fetchall()
            logger.info(f"Se consultaron {len(filas)} productos de la base de datos.")
            return filas
        
        except mysql.connector.Error as err:
            logger.exception("Error de MySQL al consultar los productos:")
            return None
        except Exception as e:
            # 4. Manejo de excepciones
            logger.exception(f"Error inesperado al consultar productos: {e}")
            return None

        finally:
            # 5. Asegura que la conexión se cierre
            if cursor:
                cursor.close()
                logger.debug("Cursor cerrado.")
            if 'conexión' in locals() and conexión and conexión.is_connected():
                conexión.close()
                logger.info("Conexión a la base de datos cerrada.")

    def modificarUnProducto(self, datos, intentos=MÁX_INTENTOS):
        """
        Modifica un producto existente en la tabla PRODUCTO.
        Maneja reintentos en caso de deadlock.

        Args:
            datos (list): Una lista con los datos del producto en el orden:
                          [nuevo_codigo, nombre, descripcion, precio_venta, 
                           stock_actual, stock_minimo, id_producto (para el WHERE)]
            intentos (int): Número máximo de reintentos en caso de deadlock.
        """
        intento = 0
        logger = logging.getLogger(__name__)  # Obtener el logger
        reintentar = True
        
        conexión = None
        cursor = None

        while intento < intentos and reintentar:
            try:
                conexión = self.abrir()  # Abrir la conexión
                cursor = conexión.cursor()
                
                # Consulta adaptada a la tabla PRODUCTO
                # Los primeros 6 %s son para SET
                # El último %s (id_producto) es para WHERE
                consulta = """UPDATE PRODUCTO
                              SET codigo = %s,
                                  nombre = %s,
                                  descripcion = %s,
                                  precio_venta = %s,
                                  stock_actual = %s,
                                  stock_minimo = %s
                              WHERE id_producto = %s;
                           """
                
                cursor.execute(consulta, datos)
                conexión.commit()  # Confirmar la transacción
                reintentar = False
                logger.info(f"Producto ID: {datos[6]} (Código: {datos[0]}) modificado exitosamente.")

            except mysql.connector.errors.InternalError as err:
                intento += 1
                if err.errno == 1213:  # Deadlock
                    logger.warning(f"Deadlock detectado al modificar producto. Intento {intento}/{intentos}.")
                    if intento < intentos:
                        time.sleep(1)  # espera antes de reintentar
                        continue
                    else:
                        logger.error("No se pudo resolver el deadlock al modificar producto.")
                        raise
                else:
                    raise # Relanzar otros InternalError

            # --- BLOQUE MODIFICADO ---
            except mysql.connector.Error as err:
                # Error 1062: Violación de restricción UNIQUE (código duplicado)
                if err.errno == 1062: 
                    mensaje_error = f"Error: Ya existe un producto con ese código. (Detalle: {err.msg})"
                    logger.warning(mensaje_error)
                    
                    # Lanza un error simple que la UI pueda capturar
                    raise ValueError(f"Ya existe un producto con ese código.")
                else:
                    # Registra cualquier otro error de MySQL
                    logger.exception("Error de MySQL durante la modificación del producto:")
                    raise # Relanza la excepción original si no es la 1062
            # --- FIN DEL BLOQUE MODIFICADO ---

            except Exception as e:
                # Registra cualquier otro error inesperado
                logger.exception("Error inesperado durante la modificación del producto:")
                raise

            finally:
                # Este bloque se ejecuta siempre
                if cursor:
                    cursor.close()
                    logger.debug("Cursor cerrado.")
                if conexión and conexión.is_connected():
                    # Cierra la conexión
                    conexión.close()
                    logger.info("Conexión a la base de datos cerrada.")

    def actualizarStockProducto(self, datos, intentos=MÁX_INTENTOS):
        """
        Actualiza (resta) el stock de un producto en la tabla PRODUCTO
        usando su 'codigo'.

        La actualización es atómica: solo se ejecuta si el stock_actual
        es mayor o igual a la cantidad vendida.

        Args:
            datos (list): Una lista con los datos en el orden:
                          [cantidad_vendida, codigo_producto]
            intentos (int): Número máximo de reintentos en caso de deadlock.
        
        Raises:
            ValueError: Si el stock es insuficiente o el código no existe.
        """
        intento = 0
        logger = logging.getLogger(__name__)  # Obtener el logger
        reintentar = True
        
        conexión = None
        cursor = None
        
        # Preparamos los parámetros para la consulta SQL
        # [cantidad_vendida, codigo_producto, cantidad_vendida_para_check]
        parámetros_sql = (datos[0], datos[1], datos[0])
        código_producto = datos[1]

        while intento < intentos and reintentar:
            try:
                conexión = self.abrir()  # Abrir la conexión
                cursor = conexión.cursor()
                
                # --- CONSULTA ATÓMICA ---
                # Solo actualiza si el stock_actual es >= a la cantidad vendida
                consulta = """UPDATE PRODUCTO
                              SET stock_actual = stock_actual - %s
                              WHERE codigo = %s AND stock_actual >= %s;
                           """
                
                cursor.execute(consulta, parámetros_sql)
                
                # --- VERIFICACIÓN DE STOCK ---
                # Si rowcount es 0, la condición WHERE falló (no hay stock o no existe el código)
                if cursor.rowcount == 0:
                    reintentar = False # No es un deadlock, es un error lógico
                    logger.warning(f"No se pudo actualizar stock para el código: {código_producto}. Stock insuficiente o código no encontrado.")
                    # Lanza un error que la UI pueda capturar
                    raise ValueError(f"Stock insuficiente para el producto (Código: {código_producto}) o el código no existe.")
                
                conexión.commit()  # Confirmar la transacción
                reintentar = False
                logger.info(f"Stock actualizado para el producto (Código: {código_producto}). Cantidad restada: {datos[0]}")

            except mysql.connector.errors.InternalError as err:
                intento += 1
                if err.errno == 1213:  # Deadlock
                    logger.warning(f"Deadlock detectado al actualizar stock. Intento {intento}/{intentos}.")
                    if intento < intentos:
                        time.sleep(1)  # espera antes de reintentar
                        continue
                    else:
                        logger.error("No se pudo resolver el deadlock al actualizar stock.")
                        raise
                else:
                    raise # Relanzar otros InternalError

            except mysql.connector.Error as err:
                # Registra un error específico de MySQL
                logger.exception("Error de MySQL durante la actualización del stock:")
                raise

            except Exception as e:
                # Registra cualquier otro error inesperado
                # (incluyendo el ValueError que lanzamos manualmente)
                logger.exception("Error inesperado durante la actualización del stock:")
                raise

            finally:
                # Este bloque se ejecuta siempre
                if cursor:
                    cursor.close()
                    logger.debug("Cursor cerrado.")
                if conexión and conexión.is_connected():
                    # Cierra la conexión
                    conexión.close()
                    logger.info("Conexión a la base de datos cerrada.")

    def ingresarDetalleVenta(self, datos, intentos=MÁX_INTENTOS):
        """
        Inserta un registro (un producto) en la tabla DETALLE_VENTA.
        Utiliza el 'código_producto' para buscar el 'id_producto' internamente.
        Maneja reintentos en caso de deadlock.

        Args:
            datos (list): Una lista con los datos del detalle en el orden:
                          [id_venta, código_producto, cantidad, precio_unitario]
            intentos (int): Número máximo de reintentos en caso de deadlock.
        """
        intento = 0
        logger = logging.getLogger(__name__)  # Obtener el logger para este módulo
        reintentar = True
        
        # Declarar cursor y conexión fuera del try
        conexión = None
        cursor = None

        while intento < intentos and reintentar:
            try:
                conexión = self.abrir()  # Abrir la conexión
                cursor = conexión.cursor()
                
                # --- CONSULTA MODIFICADA ---
                # Ahora usa una subconsulta para encontrar el id_producto
                # a partir del código_producto (datos[1])
                consulta = """INSERT INTO DETALLE_VENTA(id_venta, id_producto, cantidad, precio_unitario)
                              VALUES (%s, (SELECT id_producto FROM PRODUCTO WHERE codigo = %s), %s, %s);
                           """
                
                cursor.execute(consulta, datos)
                conexión.commit()  # Confirmar la transacción
                reintentar = False
                logger.info(f"Detalle de Venta (Venta ID: {datos[0]}, Producto Código: {datos[1]}) ingresado.")

            except mysql.connector.errors.InternalError as err:
                intento += 1
                if err.errno == 1213:  # Deadlock
                    logger.warning(f"Deadlock detectado al ingresar detalle de venta. Intento {intento}/{intentos}.")
                    if intento < intentos:
                        time.sleep(1)  # espera antes de reintentar
                        continue
                    else:
                        logger.error("No se pudo resolver el deadlock al ingresar detalle de venta.")
                        raise
                else:
                    raise  # Relanzar otros InternalError

            except mysql.connector.Error as err:
                # Error 1062: PRIMARY KEY (id_venta, id_producto) duplicada
                if err.errno == 1062: 
                    mensaje_error = f"Error: El producto (Código: {datos[1]}) ya existe en esta venta (ID: {datos[0]})."
                    logger.warning(mensaje_error)
                    # Lanza un error simple que la UI pueda capturar
                    raise ValueError(f"Este producto (Código: {datos[1]}) ya está en el carrito.")
                
                # Error 1452: Foreign Key constraint fails (id_venta o id_producto no existen)
                elif err.errno == 1452:
                    mensaje_error = f"Error de FK: No se encontró la Venta (ID: {datos[0]}) o el Producto (Código: {datos[1]})."
                    logger.error(mensaje_error)
                    raise ValueError(f"Error: El producto con código '{datos[1]}' o la venta no son válidos.")

                else:
                    # Registra cualquier otro error de MySQL
                    logger.exception("Error de MySQL durante el ingreso del detalle de venta:")
                    raise # Relanza la excepción original

            except Exception as e:
                # Registra cualquier otro error inesperado
                logger.exception("Error inesperado durante el ingreso del detalle de venta:")
                raise

            finally:
                # Este bloque se ejecuta siempre
                if cursor:
                    cursor.close()
                    logger.debug("Cursor cerrado.")
                if conexión and conexión.is_connected():
                    conexión.close()
                    logger.info("Conexión a la base de datos cerrada.")
    
    # (Después de la función eliminarProductoPorID)

    def eliminarVentaPorID(self, datos, intentos=MÁX_INTENTOS):
        """
        Elimina una VENTA existente de la tabla VENTA usando su ID.
        Gracias a 'ON DELETE CASCADE', los detalles en DETALLE_VENTA
        se eliminan automáticamente.

        Args:
            datos (list): Una lista que contiene el id_venta: 
                          [id_venta (para el WHERE)]
            intentos (int): Número máximo de reintentos en caso de deadlock.
        """
        intento = 0
        logger = logging.getLogger(__name__)  # Obtener el logger
        reintentar = True
        
        conexión = None
        cursor = None
        
        id_venta_a_eliminar = datos[0] 

        while intento < intentos and reintentar:
            try:
                conexión = self.abrir()
                cursor = conexión.cursor()
                
                consulta = """DELETE FROM VENTA WHERE id_venta = %s;"""
                
                cursor.execute(consulta, datos)
                conexión.commit()
                reintentar = False
                logger.info(f"Venta ID: {id_venta_a_eliminar} eliminada exitosamente (con CASCADE).")

            except mysql.connector.errors.InternalError as err:
                intento += 1
                if err.errno == 1213:  # Deadlock
                    logger.warning(f"Deadlock detectado al eliminar Venta ID: {id_venta_a_eliminar}. Intento {intento}/{intentos}.")
                    if intento < intentos:
                        time.sleep(1)
                        continue
                    else:
                        logger.error("No se pudo resolver el deadlock al eliminar Venta.")
                        raise
                else:
                    raise

            except mysql.connector.Error as err:
                logger.exception(f"Error de MySQL durante la eliminación de Venta ID: {id_venta_a_eliminar}:")
                raise

            except Exception as e:
                logger.exception(f"Error inesperado durante la eliminación de Venta ID: {id_venta_a_eliminar}:")
                raise

            finally:
                if cursor:
                    cursor.close()
                if conexión and conexión.is_connected():
                    conexión.close()
    
    # (Línea 609, después de actualizarStockProducto)

    def reponerStockProducto(self, datos, intentos=MÁX_INTENTOS):
        """
        Actualiza (suma/repone) el stock de un producto en la tabla PRODUCTO
        usando su 'codigo'. (Usado para cancelar/eliminar ventas).

        Args:
            datos (list): Una lista con los datos en el orden:
                          [cantidad_repuesta, codigo_producto]
            intentos (int): Número máximo de reintentos en caso de deadlock.
        """
        intento = 0
        logger = logging.getLogger(__name__)
        reintentar = True
        
        conexión = None
        cursor = None
        
        # [cantidad_repuesta, codigo_producto]
        parámetros_sql = (datos[0], datos[1])
        código_producto = datos[1]

        while intento < intentos and reintentar:
            try:
                conexión = self.abrir()
                cursor = conexión.cursor()
                
                # Consulta para SUMAR stock
                consulta = """UPDATE PRODUCTO
                              SET stock_actual = stock_actual + %s
                              WHERE codigo = %s;
                           """
                
                cursor.execute(consulta, parámetros_sql)
                
                if cursor.rowcount == 0:
                    reintentar = False
                    logger.warning(f"No se pudo reponer stock. Código no encontrado: {código_producto}.")
                    # No lanzamos un error grave, solo advertimos, ya que la venta se eliminará igualmente.
                
                conexión.commit()
                reintentar = False
                logger.info(f"Stock repuesto para (Código: {código_producto}). Cantidad sumada: {datos[0]}")

            except mysql.connector.errors.InternalError as err:
                intento += 1
                if err.errno == 1213: # Deadlock
                    logger.warning(f"Deadlock detectado al reponer stock. Intento {intento}/{intentos}.")
                    if intento < intentos:
                        time.sleep(1)
                        continue
                    else:
                        logger.error("No se pudo resolver el deadlock al reponer stock.")
                        raise
                else:
                    raise

            except mysql.connector.Error as err:
                logger.exception("Error de MySQL durante la reposición del stock:")
                raise

            except Exception as e:
                logger.exception("Error inesperado durante la reposición del stock:")
                raise

            finally:
                if cursor:
                    cursor.close()
                if conexión and conexión.is_connected():
                    conexión.close()
                    
    def registrarVenta(self, datos, intentos=MÁX_INTENTOS):
        """
        Registra una nueva venta en la tabla VENTA.
        Maneja reintentos en caso de deadlock.

        Args:
            datos (list): Una lista que contiene la fecha y hora: 
                          [fecha_hora]
            intentos (int): Número máximo de reintentos en caso de deadlock.
        
        Returns:
            int: El id_venta (AUTO_INCREMENT) de la venta recién registrada.
            None: Si la inserción falla.
        """
        intento = 0
        logger = logging.getLogger(__name__)  # Obtener el logger para este módulo
        reintentar = True
        
        # Declarar cursor y conexión fuera del try
        conexión = None
        cursor = None
        id_venta_generado = None  # Variable para almacenar el ID

        while intento < intentos and reintentar:
            try:
                conexión = self.abrir()  # Abrir la conexión
                cursor = conexión.cursor()
                
                # Consulta adaptada a la tabla VENTA
                consulta = """INSERT INTO VENTA(fecha_hora) VALUES (%s);"""
                
                cursor.execute(consulta, datos)
                
                # --- OBTENER EL ID GENERADO ---
                id_venta_generado = cursor.lastrowid
                
                conexión.commit()  # Confirmar la transacción
                reintentar = False
                logger.info(f"Venta registrada exitosamente con ID: {id_venta_generado}.")

            except mysql.connector.errors.InternalError as err:
                intento += 1
                id_venta_generado = None # Asegurarse de que no devuelva un ID en caso de error
                if err.errno == 1213:  # Deadlock
                    logger.warning(f"Deadlock detectado al registrar la venta. Intento {intento}/{intentos}.")
                    if intento < intentos:
                        time.sleep(1)  # espera antes de reintentar
                        continue
                    else:
                        logger.error("No se pudo resolver el deadlock al registrar la venta.")
                        raise
                else:
                    raise  # Relanzar otros InternalError

            except mysql.connector.Error as err:
                id_venta_generado = None
                # Registra un error específico de MySQL si ocurre
                logger.exception("Error de MySQL durante el registro de la venta:")
                raise

            except Exception as e:
                id_venta_generado = None
                # Registra cualquier otro error inesperado
                logger.exception("Error inesperado durante el registro de la venta:")
                raise

            finally:
                # Este bloque se ejecuta siempre, haya habido error o no
                if cursor:
                    cursor.close()
                    logger.debug("Cursor cerrado.")
                if conexión and conexión.is_connected():
                    conexión.close()
                    logger.info("Conexión a la base de datos cerrada.")
        
        return id_venta_generado
    
    def consultarVentasConTotal(self):
        """
        Consulta todas las ventas de la tabla VENTA y calcula el total
        para cada una sumando los subtotales (cantidad * precio_unitario)
        de la tabla DETALLE_VENTA.

        Devuelve:
            list: Una lista de tuplas, donde cada tupla es una venta:
                  (id_venta, fecha_hora, total_venta)
                  Ordenadas de la más reciente a la más antigua.
            None: Si ocurre un error.
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None
        
        try:
            # 1. Abre la conexión a la base de datos
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            # 2. Consulta SQL con subconsulta correlacionada
            consulta = """
                SELECT
                    V.id_venta,
                    V.fecha_hora,
                    (SELECT ROUND(COALESCE(SUM(DV.cantidad * DV.precio_unitario), 0), 2)
                     FROM DETALLE_VENTA AS DV
                     WHERE DV.id_venta = V.id_venta) AS total_venta
                FROM
                    VENTA AS V
                ORDER BY
                    V.fecha_hora DESC;
            """
            
            # 3. Ejecución de la consulta
            cursor.execute(consulta)
            filas = cursor.fetchall()
            logger.info(f"Se consultaron {len(filas)} ventas con su total.")
            return filas
        
        except mysql.connector.Error as err:
            logger.exception("Error de MySQL al consultar ventas con total:")
            return None
        except Exception as e:
            # 4. Manejo de excepciones
            logger.exception(f"Error inesperado al consultar ventas con total: {e}")
            return None

        finally:
            # 5. Asegura que la conexión se cierre
            if cursor:
                cursor.close()
                logger.debug("Cursor cerrado.")
            if 'conexión' in locals() and conexión and conexión.is_connected():
                conexión.close()
                logger.info("Conexión a la base de datos cerrada.")
    
    def eliminarProductoPorID(self, datos, intentos=MÁX_INTENTOS):
        """
        Elimina un producto existente de la tabla PRODUCTO usando su ID.
        Maneja reintentos en caso de deadlock.

        Args:
            datos (list): Una lista que contiene el id_producto: 
                          [id_producto (para el WHERE)]
            intentos (int): Número máximo de reintentos en caso de deadlock.
        """
        intento = 0
        logger = logging.getLogger(__name__)  # Obtener el logger
        reintentar = True
        
        conexión = None
        cursor = None
        
        # El id_producto está en la primera posición de la lista 'datos'
        id_del_producto = datos[0] 

        while intento < intentos and reintentar:
            try:
                conexión = self.abrir()  # Abrir la conexión
                cursor = conexión.cursor()
                
                # Consulta adaptada para eliminar el producto
                consulta = """DELETE FROM PRODUCTO
                              WHERE id_producto = %s;
                           """
                
                cursor.execute(consulta, datos)
                conexión.commit()  # Confirmar la transacción
                reintentar = False
                logger.info(f"Producto ID: {id_del_producto} eliminado exitosamente.")

            except mysql.connector.errors.InternalError as err:
                intento += 1
                if err.errno == 1213:  # Deadlock
                    logger.warning(f"Deadlock detectado al eliminar producto. Intento {intento}/{intentos}.")
                    if intento < intentos:
                        time.sleep(1)  # espera antes de reintentar
                        continue
                    else:
                        logger.error("No se pudo resolver el deadlock al eliminar producto.")
                        raise
                else:
                    raise # Relanzar otros InternalError

            except mysql.connector.Error as err:
                # Registra un error específico de MySQL
                logger.exception("Error de MySQL durante la eliminación del producto:")
                raise

            except Exception as e:
                # Registra cualquier otro error inesperado
                logger.exception("Error inesperado durante la eliminación del producto:")
                raise

            finally:
                # Este bloque se ejecuta siempre
                if cursor:
                    cursor.close()
                    logger.debug("Cursor cerrado.")
                if conexión and conexión.is_connected():
                    # Cierra la conexión
                    conexión.close()
                    logger.info("Conexión a la base de datos cerrada.")

    # Respaldar una base de datos MySQL usando Python
    def respaldarBaseDeDatos(self, ubicación_respaldo):
        config = self.obtener_configuración()
        base_de_datos = config['database']['database']
        #Obtenemos la fecha actual
        fecha = datetime.today().strftime('%H_%M_%S_del_%d_%m_%Y')
        #Nombre del archivo de respaldo
        respaldo = r'Respaldo_a_las_' + str(fecha) + '.sql'
        with open(ubicación_respaldo + '/' + respaldo, 'w') as out:
            """
            comando = [
                r'C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysqldump.exe',
                f'-h{host}',
                f'-u{usuario}',
                f'-p{contraseña}',
                '--ssl-mode=DISABLED',
                base_de_datos
            ]

            subprocess.run(
                comando,
                stdout=out,
                text=True  # Para manejar texto correctamente
            )
            """
            comando = [
                        r'C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysqldump.exe',
                        "--defaults-extra-file=C:\\Users\\Gabriel\\.mydumps.cnf",
                        "--databases",
                        base_de_datos,
                        # ↓↓↓ Opciones añadidas para incluir la lógica de negocio ↓↓↓
                        "--routines",  # Incluye Procedimientos Almacenados y Funciones
                        "--events",    # Incluye Eventos
                        "--triggers"   # Asegura la inclusión de Triggers (opcional pero recomendado)
                      ]  

            subprocess.run(
                            comando,
                            stdout=out,
                            creationflags=subprocess.CREATE_NO_WINDOW,  # Evita mostrar la ventana de la consola,
                            text=True  # Recomendado para manejar la salida correctamente
                          )