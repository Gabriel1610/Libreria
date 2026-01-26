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
                          [codigo, nombre, descripcion, precio_venta, ventas_acumuladas, umbral_ventas]
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
                consulta = """INSERT INTO PRODUCTO(codigo, nombre, descripcion, precio_venta, ventas_acumuladas, umbral_ventas)
                              VALUES(%s, CONCAT(UCASE(LEFT(%s, 1)), SUBSTRING(%s, 2)), CONCAT(UCASE(LEFT(%s, 1)), SUBSTRING(%s, 2)), %s, %s, %s);
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
                # Error 1062: Código duplicado
                if err.errno == 1062: 
                    mensaje_error = f"Error: Ya existe un producto con ese código. (Detalle: {err.msg})"
                    logger.warning(mensaje_error)
                    raise ValueError(f"Ya existe un producto con ese código.")
                
                # --- CAPTURA DE ERROR DE RANGO ACTUALIZADA ---
                # Error 1264: Valor fuera de rango (número muy grande)
                elif err.errno == 1264:
                    columna = "desconocida"
                    mensaje_error_str = str(err).lower() # Convertimos a minúsculas para buscar mejor

                    if "precio_venta" in mensaje_error_str:
                        columna = "Precio"
                    elif "ventas_acumuladas" in mensaje_error_str:
                        columna = "Ventas Acumuladas"
                    elif "umbral_ventas" in mensaje_error_str:
                        columna = "Umbral de Ventas"
                    
                    mensaje_usuario = f"El valor ingresado en '{columna}' es demasiado grande para el sistema."
                    logger.warning(f"Error de rango en BD: {err.msg}")
                    raise ValueError(mensaje_usuario)
                # ---------------------------------------------

                else:
                    # Registra cualquier otro error de MySQL
                    logger.exception("Error de MySQL durante el ingreso del producto:")
                    raise

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

    def consultarDatosParaExcel(self):
        """
        Obtiene una lista plana con todos los detalles de todas las ventas
        para exportar a Excel.
        
        Retorna: (id_venta, fecha, total_venta, nombre_prod, precio_unit, cantidad, subtotal)
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None
        
        try:
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            # Consulta optimizada:
            # 1. Calcula el total de la venta en una subconsulta
            # 2. Une Venta con Detalle y Producto
            # 3. Ordena por Fecha Descendente
            consulta = """
                SELECT 
                    V.id_venta,
                    V.fecha_hora,
                    (SELECT ROUND(COALESCE(SUM(d.cantidad * d.precio_unitario), 0), 2) 
                     FROM DETALLE_VENTA d WHERE d.id_venta = V.id_venta) as total_venta,
                    P.nombre,
                    DV.precio_unitario,
                    DV.cantidad,
                    ROUND((DV.cantidad * DV.precio_unitario), 2) as subtotal
                FROM VENTA V
                JOIN DETALLE_VENTA DV ON V.id_venta = DV.id_venta
                JOIN PRODUCTO P ON DV.id_producto = P.id_producto
                ORDER BY V.fecha_hora DESC, V.id_venta DESC;
            """
            
            cursor.execute(consulta)
            filas = cursor.fetchall()
            return filas

        except mysql.connector.Error as err:
            logger.exception("Error MySQL al exportar Excel:")
            return None
        finally:
            if cursor: cursor.close()
            if 'conexión' in locals() and conexión and conexión.is_connected():
                conexión.close()

    def obtenerProductoPorID(self, id_producto):
        """
        Busca un producto en la tabla PRODUCTO usando su 'id_producto'.

        Args:
            id_producto (int): El ID del producto a buscar.

        Returns:
            tuple: Una tupla con los datos del producto si se encuentra:
                   (codigo, nombre, precio_venta, ventas_acumuladas, 
                    umbral_ventas, descripcion, id_producto, id_alternativa)
            None: Si no se encuentra el producto o si ocurre un error.
        """
        logger = logging.getLogger(__name__)  # Obtener el logger
        conexión = None
        cursor = None

        try:
            conexión = self.abrir()  # Abrir la conexión
            cursor = conexión.cursor()
            
            # Consulta adaptada para buscar por ID y devolver las mismas columnas 
            # que buscarProductoPorCódigo para mantener consistencia.
            consulta = """SELECT codigo, nombre, 
                                 precio_venta, ventas_acumuladas, umbral_ventas, 
                                 descripcion, id_producto, id_alternativa
                          FROM PRODUCTO
                          WHERE id_producto = %s;
                       """
            
            # Ejecutar la consulta pasando el 'id_producto' como una tupla
            cursor.execute(consulta, (id_producto,))
            
            # Obtener el único resultado (o None si no se encontró)
            producto = cursor.fetchone() 
            
            if producto:
                logger.info(f"Producto encontrado con ID: {id_producto}.")
            else:
                logger.warning(f"No se encontró ningún producto con ID: {id_producto}.")
                
            return producto # Devuelve la tupla del producto o None

        except mysql.connector.Error as err:
            # Registra un error específico de MySQL
            logger.exception(f"Error de MySQL durante la búsqueda del producto con ID {id_producto}:")
            return None

        except Exception as e:
            # Registra cualquier otro error inesperado
            logger.exception(f"Error inesperado durante la búsqueda del producto con ID {id_producto}:")
            return None

        finally:
            # Este bloque se ejecuta siempre
            if cursor:
                cursor.close()
                logger.debug("Cursor cerrado.")
            if 'conexión' in locals() and conexión and conexión.is_connected():
                conexión.close()
                logger.info("Conexión a la base de datos cerrada.")
    
    def buscarProductoPorCódigo(self, código):
        """
        Busca un producto en la tabla PRODUCTO usando su 'código' único.

        Args:
            código (str): El código del producto a buscar.

        Returns:
            tuple: Una tupla con los datos del producto si se encuentra:
                   (codigo, nombre, precio_venta, ventas_acumuladas, 
                    umbral_ventas, descripcion, id_producto, id_alternativa)
            None: Si no se encuentra el producto o si ocurre un error.
        """
        logger = logging.getLogger(__name__)  # Obtener el logger
        conexión = None
        cursor = None

        try:
            conexión = self.abrir()  # Abrir la conexión
            cursor = conexión.cursor()
            
            # Consulta actualizada a las nuevas columnas de la BD
            # Se agrega id_alternativa al final
            consulta = """SELECT codigo, nombre, 
                                 precio_venta, ventas_acumuladas, umbral_ventas, 
                                 descripcion, id_producto, id_alternativa
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
            if 'conexión' in locals() and conexión and conexión.is_connected():
                conexión.close()
                logger.info("Conexión a la base de datos cerrada.")

    def buscarProductoPorNombre(self, nombre):
        """
        Busca productos en la tabla PRODUCTO cuyo nombre contenga el término de búsqueda.
        La búsqueda ignora mayúsculas y minúsculas.
        
        Returns:
            list: Tuplas con (codigo, nombre, precio, ventas_acum, umbral, desc, id_prod, id_alt)
        """
        logger = logging.getLogger(__name__)  # Obtener el logger
        conexión = None
        cursor = None

        try:
            conexión = self.abrir()  # Abrir la conexión
            cursor = conexión.cursor()
            
            término_búsqueda = f"%{nombre.lower()}%"

            # Consulta actualizada con nuevas columnas
            # Filtramos eliminados para no mostrar basura
            consulta = """SELECT codigo, 
                                 nombre, 
                                 precio_venta, 
                                 ventas_acumuladas, 
                                 umbral_ventas, 
                                 descripcion, 
                                 id_producto,
                                 id_alternativa
                          FROM PRODUCTO
                          WHERE eliminado = 0 
                            AND LOWER(nombre COLLATE utf8mb4_bin) LIKE %s
                          ORDER BY nombre; 
                       """
            
            cursor.execute(consulta, (término_búsqueda,))
            productos = cursor.fetchall() 
            
            if productos:
                logger.info(f"Se encontraron {len(productos)} productos con el nombre '{nombre}'.")
            else:
                logger.info(f"No se encontró ningún producto que contenga '{nombre}'.")
                
            return productos 

        except mysql.connector.Error as err:
            logger.exception(f"Error de MySQL durante la búsqueda por nombre '{nombre}':")
            return None

        except Exception as e:
            logger.exception(f"Error inesperado durante la búsqueda por nombre '{nombre}':")
            return None

        finally:
            if cursor: cursor.close()
            if 'conexión' in locals() and conexión and conexión.is_connected():
                conexión.close()
                logger.info("Conexión a la base de datos cerrada.")

    def buscarProductoPorDescripción(self, descripción):
        """
        Busca productos en la tabla PRODUCTO cuya descripción contenga el término de búsqueda.
        La búsqueda ignora mayúsculas y minúsculas.

        Args:
            descripción (str): El término de búsqueda para la descripción del producto.

        Returns:
            list: Tuplas con (codigo, nombre, precio, ventas_acum, umbral, desc, id_prod, id_alt)
            None: Si ocurre un error.
        """
        logger = logging.getLogger(__name__)  # Obtener el logger
        conexión = None
        cursor = None

        try:
            conexión = self.abrir()  # Abrir la conexión
            cursor = conexión.cursor()
            
            # Prepara el término de búsqueda para SQL LIKE (case-insensitive)
            término_búsqueda = f"%{descripción.lower()}%"

            # Consulta actualizada con nuevas columnas
            # Filtramos eliminados para no mostrar basura
            consulta = """SELECT codigo, 
                                 nombre, 
                                 precio_venta, 
                                 ventas_acumuladas, 
                                 umbral_ventas, 
                                 descripcion, 
                                 id_producto,
                                 id_alternativa
                          FROM PRODUCTO
                          WHERE eliminado = 0
                            AND LOWER(descripcion COLLATE utf8mb4_bin) LIKE %s
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
            if 'conexión' in locals() and conexión and conexión.is_connected():
                conexión.close()
                logger.info("Conexión a la base de datos cerrada.")
    
    def consultarProductosPorAlertaVentas(self):
        """
        Devuelve una lista de productos (Código, Nombre) que han superado 
        o igualado su umbral de ventas.
        Ignora productos con umbral nulo o cero.
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None
        
        try:
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            # Consulta ajustada:
            # 1. Filtra 'eliminado = 0'.
            # 2. Filtra 'umbral_ventas IS NOT NULL' y mayor a 0.
            # 3. Usa COALESCE para tratar ventas_acumuladas NULL como 0.
            consulta = """SELECT 
                             codigo,
                             nombre
                          FROM 
                             PRODUCTO
                          WHERE 
                             eliminado = 0 
                             AND umbral_ventas IS NOT NULL
                             AND umbral_ventas > 0
                             AND COALESCE(ventas_acumuladas, 0) >= umbral_ventas
                          ORDER BY
                             (COALESCE(ventas_acumuladas, 0) / umbral_ventas) DESC;
                       """
            
            cursor.execute(consulta)
            filas = cursor.fetchall()
            
            logger.info(f"Se consultaron {len(filas)} productos en alerta de ventas.")
            return filas
        
        except mysql.connector.Error as err:
            logger.exception("Error de MySQL al consultar alertas:")
            return None
        except Exception as e:
            logger.exception(f"Error inesperado al consultar alertas: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if 'conexión' in locals() and conexión and conexión.is_connected():
                conexión.close()
                logger.info("Conexión a la base de datos cerrada.")

    def consultarDatosProductos(self):
        """
        Consulta y devuelve todos los productos ACTIVOS.
        Incluye el CÓDIGO del producto alternativo y la LONGITUD de la descripción.

        Devuelve: (codigo, nombre, precio, ventas, umbral, desc, COD_ALTERNATIVA, id_producto, LARGO_DESC)
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None
        
        try:
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            # Consulta actualizada:
            # 1. Agregamos CHAR_LENGTH para obtener la cantidad de caracteres de la descripción.
            # 2. Usamos COALESCE para evitar problemas si la descripción es NULL (devuelve 0).
            consulta = """
                SELECT 
                    P1.codigo, 
                    P1.nombre, 
                    P1.precio_venta, 
                    P1.ventas_acumuladas, 
                    P1.umbral_ventas, 
                    P1.descripcion,
                    P2.codigo AS codigo_alternativa,
                    P1.id_producto,
                    CHAR_LENGTH(COALESCE(P1.descripcion, '')) AS largo_descripcion
                FROM PRODUCTO AS P1
                LEFT JOIN PRODUCTO AS P2 ON P1.id_alternativa = P2.id_producto
                WHERE P1.eliminado = 0
                ORDER BY P1.nombre; 
            """
            
            cursor.execute(consulta)
            filas = cursor.fetchall()
            logger.info(f"Se consultaron {len(filas)} productos activos.")
            return filas
            
        except mysql.connector.Error as err:
            logger.exception("Error de MySQL al consultar los productos:")
            return None
        except Exception as e:
            logger.exception(f"Error inesperado al consultar productos: {e}")
            return None

        finally:
            if cursor: cursor.close()
            if 'conexión' in locals() and conexión and conexión.is_connected():
                conexión.close()

    def resetearVentasProducto(self, codigo):
        """
        Pone en 0 las ventas acumuladas de un producto dado su código.
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None

        try:
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            consulta = "UPDATE PRODUCTO SET ventas_acumuladas = 0 WHERE codigo = %s"
            cursor.execute(consulta, (codigo,))
            conexión.commit()
            
            logger.info(f"Ventas acumuladas reseteadas para producto: {codigo}")

        except mysql.connector.Error as err:
            logger.exception("Error de MySQL al resetear ventas:")
            raise
        finally:
            if cursor: cursor.close()
            if conexión and conexión.is_connected(): conexión.close()

    def modificarUnProducto(self, datos, intentos=MÁX_INTENTOS):
        """
        Modifica un producto existente en la tabla PRODUCTO.
        Incluye la actualización de la alternativa mediante subconsulta.

        Args:
            datos (list): [codigo, nombre, descripcion, precio, ventas, umbral, cod_alternativa, id_producto]
        """
        intento = 0
        logger = logging.getLogger(__name__)
        reintentar = True
        conexión = None
        cursor = None
        
        # El código de la alternativa está en la posición 6
        # Si está vacío, pasamos None para que la subconsulta no falle o lo manejamos en SQL
        codigo_alternativa = datos[6] if datos[6] else None

        while intento < intentos and reintentar:
            try:
                conexión = self.abrir()
                cursor = conexión.cursor()
                
                # Consulta actualizada con subconsulta para id_alternativa
                # Si el código de alternativa es NULL, id_alternativa será NULL
                consulta = """UPDATE PRODUCTO
                              SET codigo = %s,
                                  nombre = %s,
                                  descripcion = %s,
                                  precio_venta = %s,
                                  ventas_acumuladas = %s,
                                  umbral_ventas = %s,
                                  id_alternativa = (SELECT id_producto FROM (SELECT id_producto FROM PRODUCTO WHERE codigo = %s) AS sub)
                              WHERE id_producto = %s;
                           """
                
                # Nota sobre la subconsulta anidada (SELECT ... FROM (SELECT ...)):
                # En MySQL no puedes seleccionar de la misma tabla que estás actualizando en una subconsulta directa.
                # El truco "FROM (SELECT ...) AS sub" evita el error 1093.
                
                # Ajustamos los parámetros para la consulta
                params = (
                    datos[0], # codigo
                    datos[1], # nombre
                    datos[2], # descripcion
                    datos[3], # precio
                    datos[4], # ventas
                    datos[5], # umbral
                    codigo_alternativa, # codigo alternativa (para la subconsulta)
                    datos[7]  # id_producto (WHERE)
                )
                
                cursor.execute(consulta, params)
                conexión.commit()
                reintentar = False
                logger.info(f"Producto ID: {datos[7]} modificado exitosamente.")

            except mysql.connector.Error as err:
                # (Mismo manejo de errores que tenías antes...)
                if err.errno == 1062: 
                    raise ValueError(f"Ya existe un producto con ese código.")
                elif err.errno == 1264:
                     # ... (lógica de rango) ...
                     raise ValueError("Valor fuera de rango.")
                else:
                    logger.exception("Error MySQL al modificar:")
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
    
    def buscarVentaPorID(self, id_venta):
        """
        Busca una venta específica por su ID y calcula su total.
        Retorna una lista con una única tupla (o vacía):
        [(id_venta, fecha_hora, nombre_medio_pago, total_venta)]
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None
        
        try:
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            # Consulta filtrada por ID
            consulta = """
                SELECT
                    V.id_venta,
                    V.fecha_hora,
                    MP.nombre AS medio_pago,
                    (SELECT ROUND(COALESCE(SUM(DV.cantidad * DV.precio_unitario), 0), 2)
                     FROM DETALLE_VENTA AS DV
                     WHERE DV.id_venta = V.id_venta) AS total_venta
                FROM
                    VENTA AS V
                JOIN
                    MEDIO_PAGO AS MP ON V.id_medio_pago = MP.id_medio_pago
                WHERE
                    V.id_venta = %s;
            """
            
            cursor.execute(consulta, (id_venta,))
            filas = cursor.fetchall()
            return filas
        
        except mysql.connector.Error as err:
            logger.exception(f"Error de MySQL al buscar venta ID {id_venta}:")
            return None
        except Exception as e:
            logger.exception(f"Error inesperado al buscar venta ID {id_venta}: {e}")
            return None

        finally:
            if cursor: cursor.close()
            if conexión and conexión.is_connected(): conexión.close()

    def modificarMedioPago(self, nombre_original, nuevo_nombre, nuevo_facturar):
        """
        Modifica el nombre y/o estado de facturación de un medio de pago.
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None

        try:
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            # Obtener ID del medio original
            cursor.execute("SELECT id_medio_pago FROM MEDIO_PAGO WHERE nombre = %s", (nombre_original,))
            resultado = cursor.fetchone()
            
            if not resultado:
                raise ValueError(f"No se encontró el medio de pago '{nombre_original}'.")
            
            id_medio = resultado[0]

            # Actualizar
            consulta = """UPDATE MEDIO_PAGO 
                          SET nombre = %s, facturar = %s 
                          WHERE id_medio_pago = %s"""
            
            cursor.execute(consulta, (nuevo_nombre, nuevo_facturar, id_medio))
            conexión.commit()
            logger.info(f"Medio de pago '{nombre_original}' actualizado a '{nuevo_nombre}'.")

        except mysql.connector.Error as err:
            if err.errno == 1062: # Duplicado
                raise ValueError(f"Ya existe otro medio de pago con el nombre '{nuevo_nombre}'.")
            else:
                logger.exception("Error de MySQL al modificar medio de pago:")
                raise
        finally:
            if cursor: cursor.close()
            if conexión and conexión.is_connected(): conexión.close()

    def consultarDetalleVenta(self, id_venta):
        """
        Consulta todos los detalles (productos, cantidades, precios)
        asociados con un id_venta específico.

        Args:
            id_venta (int): El ID de la venta a consultar.

        Devuelve:
            list: Una lista de tuplas con los datos:
                  (codigo, nombre, precio_unitario, cantidad, subtotal)
            None: Si ocurre un error.
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None
        
        try:
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            # Consulta con JOIN para obtener código y nombre del producto
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
            
            cursor.execute(consulta, (id_venta,))
            filas = cursor.fetchall()
            
            logger.info(f"Se consultaron {len(filas)} detalles para la Venta ID: {id_venta}.")
            return filas
        
        except mysql.connector.Error as err:
            logger.exception(f"Error de MySQL al consultar detalles de Venta ID: {id_venta}:")
            return None
        
        except Exception as e:
            logger.exception(f"Error inesperado al consultar detalles de Venta ID: {id_venta}: {e}")
            return None

        finally:
            if cursor: cursor.close()
            if 'conexión' in locals() and conexión and conexión.is_connected():
                conexión.close()

    def actualizarVentasProducto(self, datos, intentos=MÁX_INTENTOS):
        """
        Actualiza (SUMA) las ventas acumuladas de un producto.

        Args:
            datos: [cantidad_vendida, codigo_producto]
        """
        intento = 0
        logger = logging.getLogger(__name__)
        reintentar = True
        conexión = None
        cursor = None
        
        # [cantidad_vendida, codigo_producto]
        cantidad_vendida = datos[0]
        código_producto = datos[1]

        while intento < intentos and reintentar:
            try:
                conexión = self.abrir()
                cursor = conexión.cursor()
                
                # SUMAMOS la cantidad vendida al acumulador
                consulta = """UPDATE PRODUCTO
                              SET ventas_acumuladas = ventas_acumuladas + %s
                              WHERE codigo = %s;
                           """
                
                cursor.execute(consulta, (cantidad_vendida, código_producto))
                
                if cursor.rowcount == 0:
                    reintentar = False
                    logger.warning(f"No se encontró código: {código_producto}.")
                    raise ValueError(f"El producto (Código: {código_producto}) no existe.")
                
                conexión.commit()
                reintentar = False
                logger.info(f"Ventas acumuladas actualizadas para {código_producto}. +{cantidad_vendida}")

            # ... (Mismos excepts de Deadlock y Error MySQL que tenías antes) ...
            except mysql.connector.errors.InternalError as err:
                # Copiar lógica de deadlock existente...
                pass # (Usa tu código anterior aquí)
            except Exception as e:
                logger.exception("Error actualizando ventas:")
                raise
            finally:
                if cursor: cursor.close()
                if conexión and conexión.is_connected(): conexión.close()

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
    
    def verificarEstadoMedioPago(self, nombre):
        """
        Busca si existe un medio de pago por nombre y devuelve su estado.
        
        Returns:
            tuple: (id_medio_pago, eliminado) si existe.
            None: si no existe.
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None

        try:
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            consulta = "SELECT id_medio_pago, eliminado FROM MEDIO_PAGO WHERE nombre = %s"
            cursor.execute(consulta, (nombre,))
            resultado = cursor.fetchone()
            
            return resultado

        except mysql.connector.Error as err:
            logger.exception("Error al verificar medio de pago:")
            raise
        finally:
            if cursor: cursor.close()
            if conexión and conexión.is_connected(): conexión.close()

    def restaurarMedioPago(self, id_medio, facturar):
        """
        Restaura un medio de pago eliminado (pone eliminado=0) y actualiza si factura.
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None

        try:
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            consulta = "UPDATE MEDIO_PAGO SET eliminado = 0, facturar = %s WHERE id_medio_pago = %s"
            cursor.execute(consulta, (facturar, id_medio))
            conexión.commit()
            
            logger.info(f"Medio de pago ID {id_medio} restaurado exitosamente.")

        except mysql.connector.Error as err:
            logger.exception("Error al restaurar medio de pago:")
            raise
        finally:
            if cursor: cursor.close()
            if conexión and conexión.is_connected(): conexión.close()

    def ingresarNuevoMedioPago(self, nombre, facturar):
        """
        Realiza la inserción de un nuevo medio de pago.
        Asume que ya se verificó que no existe.
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None

        try:
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            consulta = "INSERT INTO MEDIO_PAGO(nombre, facturar) VALUES (%s, %s)"
            cursor.execute(consulta, (nombre, facturar))
            conexión.commit()
            
            logger.info(f"Medio de pago '{nombre}' creado exitosamente.")

        except mysql.connector.Error as err:
            logger.exception("Error al crear medio de pago:")
            raise
        finally:
            if cursor: cursor.close()
            if conexión and conexión.is_connected(): conexión.close()
    
    def eliminarMedioPagoLogico(self, nombre):
        """
        Marca un medio de pago como eliminado (eliminado = 1) en la base de datos.
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None

        try:
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            # Actualización lógica por nombre
            consulta = "UPDATE MEDIO_PAGO SET eliminado = 1 WHERE nombre = %s"
            cursor.execute(consulta, (nombre,))
            
            if cursor.rowcount == 0:
                # Si no afectó ninguna fila, algo raro pasó (quizás ya estaba borrado)
                logger.warning(f"No se encontró o no se pudo eliminar el medio: {nombre}")
            
            conexión.commit()
            logger.info(f"Medio de pago '{nombre}' eliminado lógicamente.")

        except mysql.connector.Error as err:
            logger.exception("Error de MySQL al eliminar medio de pago:")
            raise
        finally:
            if cursor: cursor.close()
            if conexión and conexión.is_connected(): conexión.close()
    
    def consultarMediosPago(self):
        """
        Consulta todos los medios de pago registrados en la tabla MEDIO_PAGO.

        Devuelve:
            list: Una lista de tuplas con los datos:
                  (nombre, facturar)
                  Ordenados alfabéticamente por nombre.
            None: Si ocurre un error de conexión o consulta.
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None
        
        try:
            # 1. Abre la conexión a la base de datos
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            # 2. Consulta SQL
            consulta = """
                SELECT nombre, facturar 
                FROM MEDIO_PAGO
                WHERE eliminado = 0
                ORDER BY nombre;
            """
            
            # 3. Ejecución de la consulta
            cursor.execute(consulta)
            filas = cursor.fetchall()
            
            logger.info(f"Se consultaron {len(filas)} medios de pago.")
            return filas
        
        except mysql.connector.Error as err:
            logger.exception("Error de MySQL al consultar medios de pago:")
            return None
        
        except Exception as e:
            # 4. Manejo de excepciones genéricas
            logger.exception(f"Error inesperado al consultar medios de pago: {e}")
            return None

        finally:
            # 5. Asegura que la conexión se cierre siempre
            if cursor:
                cursor.close()
                logger.debug("Cursor cerrado.")
            if 'conexión' in locals() and conexión and conexión.is_connected():
                conexión.close()
                logger.info("Conexión a la base de datos cerrada.")
    
    def consultarReporteProductos(self):
        """
        Consulta el reporte de productos: Nombre, Unidades vendidas y Recaudación.
        Ordenado por recaudación descendente.
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None
        
        try:
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            # Consulta de Agregación
            # Usamos COALESCE para que muestre 0 en vez de NULL si no hay ventas
            consulta = """
                SELECT 
                    P.nombre,
                    COALESCE(SUM(DV.cantidad), 0) AS unidades_vendidas,
                    ROUND(COALESCE(SUM(DV.cantidad * DV.precio_unitario), 0), 2) AS recaudacion
                FROM 
                    PRODUCTO AS P
                LEFT JOIN 
                    DETALLE_VENTA AS DV ON P.id_producto = DV.id_producto
                WHERE 
                    P.eliminado = 0
                GROUP BY 
                    P.id_producto, P.nombre
                ORDER BY 
                    recaudacion DESC;
            """
            
            cursor.execute(consulta)
            filas = cursor.fetchall()
            return filas

        except mysql.connector.Error as err:
            logger.exception("Error MySQL al consultar reporte productos:")
            return None
        finally:
            if cursor: cursor.close()
            if 'conexión' in locals() and conexión and conexión.is_connected():
                conexión.close()
    
    def eliminar_clase(self, id_clase):
        """Elimina una clase por su código (ID)."""
        conexión = None
        cursor = None
        try:
            conexión = self.abrir()
            cursor = conexión.cursor()
            sql = "DELETE FROM clases_dadas WHERE código = %s"
            cursor.execute(sql, (id_clase,))
            conexión.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conexión and conexión.is_connected(): conexión.close()
            
    def obtenerDetalleMedioPago(self, nombre):
        """
        Obtiene los detalles (facturar) de un medio de pago por su nombre.
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None

        try:
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            consulta = "SELECT facturar FROM MEDIO_PAGO WHERE nombre = %s"
            cursor.execute(consulta, (nombre,))
            resultado = cursor.fetchone()
            
            return resultado # Devuelve (1,) o (0,) o None

        except mysql.connector.Error as err:
            logger.exception("Error al obtener detalle de medio de pago:")
            return None
        finally:
            if cursor: cursor.close()
            if conexión and conexión.is_connected(): conexión.close()

    def registrarVenta(self, datos, intentos=MÁX_INTENTOS):
        """
        Registra una nueva venta en la tabla VENTA.
        Busca automáticamente el id_medio_pago usando el nombre provisto.

        Args:
            datos (list): [nombre_medio_pago, fecha_hora]
            intentos (int): Número máximo de reintentos.
        
        Returns:
            int: El id_venta generado.
        """
        intento = 0
        logger = logging.getLogger(__name__)
        reintentar = True
        conexión = None
        cursor = None
        id_venta_generado = None

        while intento < intentos and reintentar:
            try:
                conexión = self.abrir()
                cursor = conexión.cursor()
                
                # --- CONSULTA CON SUBCONSULTA ---
                # Insertamos buscando el ID directamente en la misma sentencia
                consulta = """INSERT INTO VENTA(id_medio_pago, fecha_hora) 
                              VALUES ((SELECT id_medio_pago FROM MEDIO_PAGO WHERE nombre = %s), %s);"""
                
                cursor.execute(consulta, datos)
                id_venta_generado = cursor.lastrowid
                
                conexión.commit()
                reintentar = False
                logger.info(f"Venta registrada exitosamente con ID: {id_venta_generado}.")

            except mysql.connector.errors.InternalError as err:
                intento += 1
                id_venta_generado = None
                if err.errno == 1213: # Deadlock
                    logger.warning(f"Deadlock detectado. Intento {intento}/{intentos}.")
                    if intento < intentos:
                        time.sleep(1)
                        continue
                    else:
                        logger.error("No se pudo resolver el deadlock.")
                        raise
                else:
                    raise

            except mysql.connector.Error as err:
                # Capturar error si el nombre del medio de pago no existe (Column 'id_medio_pago' cannot be null)
                if err.errno == 1048: 
                    logger.error(f"Error: El medio de pago '{datos[0]}' no existe o no es válido.")
                    raise ValueError(f"El medio de pago '{datos[0]}' no es válido.")
                else:
                    logger.exception("Error de MySQL durante el registro de la venta:")
                    raise

            except Exception as e:
                id_venta_generado = None
                logger.exception("Error inesperado durante el registro de la venta:")
                raise

            finally:
                if cursor: cursor.close()
                if conexión and conexión.is_connected(): conexión.close()
        
        return id_venta_generado
    
    def consultarVentasConTotal(self):
        """
        Consulta todas las ventas de la tabla VENTA.
        Obtiene el nombre del Medio de Pago y calcula el total de la venta.

        Devuelve:
            list: (id_venta, fecha_hora, nombre_medio_pago, total_venta)
        """
        logger = logging.getLogger(__name__)
        conexión = None
        cursor = None
        
        try:
            conexión = self.abrir()
            cursor = conexión.cursor()
            
            # Consulta actualizada con JOIN
            consulta = """
                SELECT
                    V.id_venta,
                    V.fecha_hora,
                    MP.nombre AS medio_pago,
                    (SELECT ROUND(COALESCE(SUM(DV.cantidad * DV.precio_unitario), 0), 2)
                     FROM DETALLE_VENTA AS DV
                     WHERE DV.id_venta = V.id_venta) AS total_venta
                FROM
                    VENTA AS V
                JOIN
                    MEDIO_PAGO AS MP ON V.id_medio_pago = MP.id_medio_pago
                ORDER BY
                    V.fecha_hora DESC;
            """
            
            cursor.execute(consulta)
            filas = cursor.fetchall()
            logger.info(f"Se consultaron {len(filas)} ventas con medio de pago y total.")
            return filas
        
        except mysql.connector.Error as err:
            logger.exception("Error de MySQL al consultar ventas:")
            return None
        except Exception as e:
            logger.exception(f"Error inesperado al consultar ventas: {e}")
            return None

        finally:
            if cursor: cursor.close()
            if conexión and conexión.is_connected(): conexión.close()
    
    def eliminarProductoPorID(self, datos, intentos=MÁX_INTENTOS):
        """
        Elimina LÓGICAMENTE un producto existente de la tabla PRODUCTO usando su ID.
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
                
                # Consulta ADAPTADA para la eliminación LÓGICA (UPDATE)
                consulta = """UPDATE PRODUCTO
                              SET eliminado = 1
                              WHERE id_producto = %s;
                           """
                
                cursor.execute(consulta, datos)
                
                # Se verifica si realmente se afectó una fila (el producto existía y no estaba ya eliminado)
                if cursor.rowcount == 0:
                    logger.warning(f"Producto ID: {id_del_producto} no encontrado o ya estaba eliminado.")
                    # Aún si no se encontró, la operación es exitosa desde el punto de vista lógico (el producto no está activo)
                
                conexión.commit()  # Confirmar la transacción
                reintentar = False
                logger.info(f"Producto ID: {id_del_producto} eliminado LÓGICAMENTE.")

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
                logger.exception("Error de MySQL durante la eliminación lógica del producto:")
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