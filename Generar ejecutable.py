import subprocess
import os
import datetime
import shutil
import tempfile # <--- 1. AÑADIR ESTO

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
    
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_icono = os.path.join(directorio_actual, NOMBRE_ICONO)
    ruta_script = os.path.join(directorio_actual, NOMBRE_SCRIPT_PRINCIPAL)

    # --- 2. DEFINIR RUTA TEMPORAL ---
    # Esto crea una ruta en C:\Users\TuUsuario\AppData\Local\Temp\build_libreria
    # OneDrive no toca esta carpeta, por lo que no habrá errores de permisos.
    directorio_temporal = os.path.join(tempfile.gettempdir(), "build_libreria")

    print("="*60)
    print(f"Iniciando generación del ejecutable...")
    print(f"Directorio de trabajo temporal: {directorio_temporal}")
    print("="*60)

    comando = [
        "pyinstaller",
        "--noconsole",
        "--onefile",
        "--windowed",
        f"--name={NOMBRE_EJECUTABLE}",
        f"--icon={ruta_icono}",
        f"--add-data={ruta_icono};.",
        
        # --- 3. AÑADIR EL ARGUMENTO WORKPATH ---
        f"--workpath={directorio_temporal}", 
        
        "--hidden-import=mysql.connector",
        "--hidden-import=mysql.connector.locales.eng.client_error",
        "--hidden-import=babel.numbers",
        "--hidden-import=tkinter",
        
        "--clean",
        ruta_script
    ]

    inicio = datetime.datetime.now()
    print(f"Hora de inicio: {inicio.strftime('%H:%M:%S')}")
    
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True)
        fin = datetime.datetime.now()
        
        if resultado.returncode == 0:
            print("\n" + "="*60)
            print("¡ÉXITO! El ejecutable se creó correctamente.")
            print(f"Tiempo total: {obtener_diferencia_tiempo(fin, inicio)}")
            print(f"Ubicación: {os.path.join(directorio_actual, 'dist', NOMBRE_EJECUTABLE + '.exe')}")
            print("="*60)
            
            if os.path.exists(NOMBRE_CONFIG):
                ruta_destino_config = os.path.join(directorio_actual, 'dist', NOMBRE_CONFIG)
                shutil.copy2(NOMBRE_CONFIG, ruta_destino_config)
                print(f"Nota: Se copió '{NOMBRE_CONFIG}'.")
        else:
            print("\n" + "="*60)
            print("ERROR: Falló la creación.")
            print("="*60)
            print(resultado.stderr)

    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")

if __name__ == "__main__":
    generar_ejecutable()
    input("\nPresiona ENTER para salir...")