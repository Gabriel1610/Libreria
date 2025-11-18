import subprocess
import os
import datetime
import shutil
import sys

# Configuración de nombres
NOMBRE_SCRIPT_PRINCIPAL = "Programa.py"
NOMBRE_ICONO = "librería.ico"
NOMBRE_EJECUTABLE = "Sistema gestión de librería"
NOMBRE_CONFIG = "config.ini"

def obtener_diferencia_tiempo(fin, inicio):
    diferencia = fin - inicio
    segundos = diferencia.total_seconds()
    return f"{segundos:.2f} segundos"

def generar_ejecutable():
    """
    Genera el ejecutable .exe para el sistema de librería.
    """
    
    # Obtener directorio actual
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_icono = os.path.join(directorio_actual, NOMBRE_ICONO)
    ruta_script = os.path.join(directorio_actual, NOMBRE_SCRIPT_PRINCIPAL)

    print("="*60)
    print(f"Iniciando generación del ejecutable para: {NOMBRE_SCRIPT_PRINCIPAL}")
    print("="*60)

    # --- Construcción del comando PyInstaller ---
    comando = [
        "pyinstaller",
        "--noconsole",              # No mostrar la ventana negra de consola
        "--onefile",                # Crear un solo archivo .exe
        "--windowed",               # Asegurar modo ventana (GUI)
        f"--name={NOMBRE_EJECUTABLE}", # Nombre del archivo de salida
        f"--icon={ruta_icono}",     # Ícono del archivo .exe
        
        # IMPORTANTE: Añadir el ícono DENTRO del ejecutable para que Tkinter lo encuentre
        # Formato Windows: "origen;destino" (el destino '.' es la raíz temporal del exe)
        f"--add-data={ruta_icono};.", 
        
        # Imports ocultos necesarios
        "--hidden-import=mysql.connector",      # Driver de base de datos
        "--hidden-import=mysql.connector.locales.eng.client_error", # A veces necesario
        "--hidden-import=babel.numbers",        # Por si usas formatos de moneda
        "--hidden-import=tkinter",
        
        "--clean",                  # Limpiar caché de compilaciones previas
        ruta_script                 # El script a convertir
    ]

    inicio = datetime.datetime.now()
    print(f"Hora de inicio: {inicio.strftime('%H:%M:%S')}")
    print("Ejecutando PyInstaller... esto puede tardar unos minutos.")

    try:
        # Ejecutar el comando
        resultado = subprocess.run(comando, capture_output=True, text=True)

        fin = datetime.datetime.now()
        
        if resultado.returncode == 0:
            print("\n" + "="*60)
            print("¡ÉXITO! El ejecutable se creó correctamente.")
            print(f"Tiempo total: {obtener_diferencia_tiempo(fin, inicio)}")
            print(f"Ubicación: {os.path.join(directorio_actual, 'dist', NOMBRE_EJECUTABLE + '.exe')}")
            print("="*60)
            
            # --- Paso Extra: Copiar config.ini ---
            # Como tu base_de_datos.py lee config.ini del disco, necesitamos copiarlo 
            # a la carpeta 'dist' para que el exe funcione al probarlo.
            if os.path.exists(NOMBRE_CONFIG):
                ruta_destino_config = os.path.join(directorio_actual, 'dist', NOMBRE_CONFIG)
                shutil.copy2(NOMBRE_CONFIG, ruta_destino_config)
                print(f"Nota: Se copió '{NOMBRE_CONFIG}' a la carpeta 'dist'.")
            else:
                print(f"ADVERTENCIA: No se encontró '{NOMBRE_CONFIG}'. Recuerda ponerlo junto al .exe.")

        else:
            print("\n" + "="*60)
            print("ERROR: Falló la creación del ejecutable.")
            print("="*60)
            print("Detalles del error:")
            print(resultado.stderr)

    except FileNotFoundError:
        print("Error: No se encontró el comando 'pyinstaller'. Asegúrate de tenerlo instalado (pip install pyinstaller).")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")

if __name__ == "__main__":
    generar_ejecutable()
    input("\nPresiona ENTER para salir...")