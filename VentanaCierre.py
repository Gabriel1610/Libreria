from tkinter import ttk
import tkinter as tk

class VentanaCierre(tk.Toplevel):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.withdraw()  # Ocultar ventana al crearla
        self.title("Cerrando...")
        self.geometry("300x100")  # Tamaño de la ventana
        self.protocol("WM_DELETE_WINDOW", self.do_nothing) #Evitar que se cierre

        self.label = ttk.Label(self, text="Cerrando la aplicación.  Por favor, espere...", wraplength=280)
        self.label.pack(pady=20)

        self.progress = ttk.Progressbar(self, mode="indeterminate")  # Barra de progreso indeterminada
        self.progress.pack(pady=10)
        self.progress.start(5)  # Inicia la animación (10 ms entre actualizaciones)

        # --- CÓDIGO NUEVO PARA CENTRAR ---
        self.update_idletasks()  # Actualiza cálculos geométricos
        
        # Calcular posición central
        x = (self.winfo_screenwidth() // 2) - (300 // 2)
        y = (self.winfo_screenheight() // 2) - (100 // 2)
        
        # Aplicar geometría (centrado)
        self.geometry(f"+{x}+{y}")
        # ---------------------------------
        self.resizable(0,0)
        self.grab_set()
        self.deiconify()  # Mostrar la ventana ya centrada

    def do_nothing(self):
        #No permite que se cierre la ventana de díalogo
        pass

    def cerrar(self):
        self.progress.stop()  # Detiene la animación
        self.destroy()