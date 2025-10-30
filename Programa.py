import tkinter as tk
import os
from tkinter import messagebox
import sys

NOMBRE_ICONO = "librería.ico"

class Aplicación(tk.Tk):
    def __init__(self):
        # 1. Llama al constructor de la clase padre (tk.Tk)
        super().__init__() 

        try:
            # 2. Configura 'self' (que ES la ventana)
            self.title("Venta de productos") 
            self.state('zoomed') 
            
            # --- Código para el ícono ---
            # (Tu lógica de ruta es buena, pero aplícala a 'self')
            
            # Esta lógica ayuda si congelas la app con PyInstaller
            if getattr(sys, 'frozen', False):
                base_dir = sys._MEIPASS
            else:
                base_dir = os.path.dirname(__file__)
            
            ruta_icono = os.path.join(base_dir, NOMBRE_ICONO)

            if os.path.exists(ruta_icono):
                # 3. Aplica el ícono a 'self'
                self.iconbitmap(ruta_icono) 
            else:
                print(f"Advertencia: No se encontró el archivo de ícono en {ruta_icono}")
            # --- Fin del código para el ícono ---

        except Exception as e:
            messagebox.showerror("Error crítico", f"Fallo en inicialización: {str(e)}")
            sys.exit(1)

# --- Necesitas esta parte para ejecutar la aplicación ---
if __name__ == "__main__":
    app = Aplicación()
    app.mainloop()