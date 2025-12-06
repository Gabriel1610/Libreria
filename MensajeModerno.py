import tkinter as tk
from tkinter import ttk
import os
import sys

NOMBRE_ICONO = "librería.ico"

class MensajeModerno(tk.Toplevel):
    def __init__(self, parent, título, mensaje, tipo="advertencia"):
        
        super().__init__(parent)
        self.overrideredirect(True)  # Quitar bordes ANTES de que Windows pinte nada
        # --- NUEVO: Configurar el Ícono de la ventana ---
        try:
            
            # Detectar si es ejecutable (.exe) o script (.py)
            if getattr(sys, 'frozen', False):
                base_dir = sys._MEIPASS
            else:
                base_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Asumiendo que el icono está en la misma carpeta que este archivo
            ruta_icono = os.path.join(base_dir, NOMBRE_ICONO)
            
            if os.path.exists(ruta_icono):
                self.iconbitmap(ruta_icono)
        except Exception:
            pass # Si falla, se muestra el icono por defecto
        # ------------------------------------------------
        
        # --- ANTI PARPADEO REAL ---
        self.withdraw()   # La ventana NO aparece aún
        
        self.resultado = False 

        # 1. Configuración de la ventana
        self.title(título)
        self.configure(bg="white")
        self.resizable(False, False)
        
        # 2. Configurar Icono y Colores
        if tipo == "error":
            icono = "❌"
            color_icono = "red"
        elif tipo == "éxito": 
            icono = "✅"
            color_icono = "#008000"
        elif tipo == "exito": 
            icono = "✅"
            color_icono = "#008000"
        elif tipo == "pregunta":
            icono = "❓"
            color_icono = "#0078D4" # Azul
        else: # advertencia
            icono = "⚠️"
            color_icono = "#FFC107"

        # 3. Layout Principal
        frame_principal = tk.Frame(self, bg="white", padx=20, pady=20)
        frame_principal.pack(expand=True, fill="both")

        # 4. Icono
        lbl_icono = tk.Label(frame_principal, text=icono, font=("Segoe UI", 30), 
                             bg="white", fg=color_icono)
        lbl_icono.pack(side="left", padx=(0, 15), anchor="n")

        # 5. Mensaje
        lbl_mensaje = tk.Label(frame_principal, text=mensaje, font=("Segoe UI", 11), 
                               bg="white", fg="#333333", justify="left", wraplength=350)
        lbl_mensaje.pack(side="top", fill="x", pady=(5, 15))

        # 6. Botones
        if tipo == "pregunta":
            frame_botones = tk.Frame(frame_principal, bg="white")
            frame_botones.pack(side="bottom", anchor="e")
            
            btn_no = ttk.Button(frame_botones, text="No", command=self.btn_cancelar, style="TButton")
            btn_no.pack(side="right", padx=(5, 0))
            
            btn_si = ttk.Button(frame_botones, text="Sí", command=self.btn_aceptar, style="TButton")
            btn_si.pack(side="right")
            btn_si.focus_set()
            
        else:
            btn_aceptar = ttk.Button(frame_principal, text="Aceptar", command=self.btn_aceptar, style="TButton")
            btn_aceptar.pack(side="bottom", anchor="e")
            btn_aceptar.focus_set()

        # 7. Centrar ventana
        self.update_idletasks() # Calcula tamaños necesarios
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x_padre = parent.winfo_x()
        y_padre = parent.winfo_y()
        ancho_padre = parent.winfo_width()
        alto_padre = parent.winfo_height()
        
        x = x_padre + (ancho_padre // 2) - (ancho // 2)
        y = y_padre + (alto_padre // 2) - (alto // 2)
        
        self.geometry(f"+{x}+{y}")

        self.deiconify()  # Ahora sí, mostrar la ventana
        self.overrideredirect(False)

        # 8. Hacer modal
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def btn_aceptar(self):
        self.resultado = True
        self.destroy()

    def btn_cancelar(self):
        self.resultado = False
        self.destroy()