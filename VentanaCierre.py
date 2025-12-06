from tkinter import ttk
import tkinter as tk

class VentanaCierre(tk.Toplevel):
    
    def __init__(self, parent, mensaje="Cerrando la aplicación. Por favor, espere..."):
        super().__init__(parent)
        
        # 1. Configuración básica de la ventana (Oculta al inicio)
        self.withdraw() 
        self.title("Procesando...")
        self.protocol("WM_DELETE_WINDOW", self.do_nothing) # Evitar cierre manual
        self.resizable(False, False)
        self.configure(bg="white")

        # 2. Layout
        frame_main = tk.Frame(self, bg="white", padx=20, pady=20)
        frame_main.pack(expand=True, fill="both")

        # 3. Etiqueta de Mensaje
        self.label = tk.Label(frame_main, text=mensaje, 
                              font=("Segoe UI", 10), bg="white", wraplength=280)
        self.label.pack(pady=(0, 15))

        # 4. Barra de Progreso (Animación)
        self.progress = ttk.Progressbar(frame_main, mode="indeterminate", length=250)
        self.progress.pack(pady=(0, 10))
        self.progress.start(10) # Velocidad de la animación (ms)

        # 5. Centrar la ventana respecto a la aplicación principal
        self.update_idletasks()
        ancho = self.winfo_reqwidth()
        alto = self.winfo_reqheight()
        
        x_padre = parent.winfo_rootx()
        y_padre = parent.winfo_rooty()
        ancho_padre = parent.winfo_width()
        alto_padre = parent.winfo_height()
        
        x = x_padre + (ancho_padre // 2) - (ancho // 2)
        y = y_padre + (alto_padre // 2) - (alto // 2)
        
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

        # 6. Mostrar y bloquear
        self.deiconify()
        self.transient(parent)
        self.grab_set()

    def do_nothing(self):
        # No permite cerrar la ventana con la X
        pass

    def cerrar(self):
        self.progress.stop() # Detener animación
        self.destroy()