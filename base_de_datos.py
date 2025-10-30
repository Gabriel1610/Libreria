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