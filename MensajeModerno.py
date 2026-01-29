import tkinter as tk
from tkinter import ttk
import os
import sys

NOMBRE_ICONO = "librería.ico"


class MensajeModerno(tk.Toplevel):
    def __init__(self, parent, título, mensaje, tipo="advertencia"):
        super().__init__(parent)

        # 1. OCULTAR AL NACER (Anti-parpadeo)
        # Esto es vital: ocultamos la ventana mientras calculamos su tamaño real
        self.withdraw()

        # Quitamos bordes temporalmente para cálculos más limpios (opcional)
        self.overrideredirect(True)

        self.resultado = False

        # --- Configurar Ícono (Igual que antes) ---
        try:
            if getattr(sys, 'frozen', False):
                base_dir = sys._MEIPASS
            else:
                base_dir = os.path.dirname(os.path.abspath(__file__))
            ruta_icono = os.path.join(base_dir, NOMBRE_ICONO)
            if os.path.exists(ruta_icono):
                self.iconbitmap(ruta_icono)
        except Exception:
            pass
        # ------------------------------------------

        # Configuración básica
        self.title(título)
        self.configure(bg="white")
        self.resizable(False, False)

        # Selección de íconos y colores
        if tipo == "error":
            icono = "❌"
            color_icono = "red"
        elif tipo in ["éxito", "exito"]:
            icono = "✅"
            color_icono = "#008000"
        elif tipo == "pregunta":
            icono = "❓"
            color_icono = "#0078D4"
        else:  # advertencia
            icono = "⚠️"
            color_icono = "#FFC107"

        # --- INTERFAZ (WIDGETS) ---
        frame_principal = tk.Frame(self, bg="white", padx=20, pady=20)
        frame_principal.pack(expand=True, fill="both")

        # Icono
        lbl_icono = tk.Label(frame_principal, text=icono, font=("Segoe UI", 30),
                             bg="white", fg=color_icono)
        lbl_icono.pack(side="left", padx=(0, 15), anchor="n")

        # Mensaje
        # wraplength controla el ancho máximo del texto antes de saltar de línea
        lbl_mensaje = tk.Label(frame_principal, text=mensaje, font=("Segoe UI", 11),
                               bg="white", fg="#333333", justify="left", wraplength=400)
        lbl_mensaje.pack(side="top", fill="x", pady=(5, 15))

        # Botones
        if tipo == "pregunta":
            frame_botones = tk.Frame(frame_principal, bg="white")
            frame_botones.pack(side="bottom", anchor="e")

            btn_no = ttk.Button(frame_botones, text="No",
                                command=self.btn_cancelar, style="TButton")
            btn_no.pack(side="right", padx=(5, 0))

            btn_si = ttk.Button(frame_botones, text="Sí",
                                command=self.btn_aceptar, style="TButton")
            btn_si.pack(side="right")
            btn_si.focus_set()
        else:
            btn_aceptar = ttk.Button(
                frame_principal, text="Aceptar", command=self.btn_aceptar, style="TButton")
            btn_aceptar.pack(side="bottom", anchor="e")
            btn_aceptar.focus_set()

        # --- LÓGICA DE CENTRADO AUTOMÁTICO ---
        self.centrar_en_ventana_padre(parent)

        # Restaurar bordes y mostrar
        self.overrideredirect(False)
        self.deiconify()

        # Hacer modal (bloquea la ventana de atrás)
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def centrar_en_ventana_padre(self, parent):
        """
        Calcula la geometría exacta basada en el contenido interno (reqwidth)
        y posiciona la ventana en el centro absoluto del padre.
        """
        # 1. Forzar a Tkinter a calcular el tamaño de los widgets internos AHORA
        self.update_idletasks()

        # 2. Obtener las dimensiones que Tkinter determinó necesarias (reqwidth/reqheight)
        # Esto funciona aunque la ventana esté oculta (withdraw)
        ancho_ventana = self.winfo_reqwidth()
        alto_ventana = self.winfo_reqheight()

        # 3. Obtener coordenadas absolutas y tamaño del padre
        # winfo_rootx/y nos da la posición real en la pantalla del monitor
        padre_x = parent.winfo_rootx()
        padre_y = parent.winfo_rooty()
        padre_ancho = parent.winfo_width()
        padre_alto = parent.winfo_height()

        # 4. Calcular el centro matemático
        x = padre_x + (padre_ancho // 2) - (ancho_ventana // 2)
        y = padre_y + (padre_alto // 2) - (alto_ventana // 2)

        # 5. Aplicar la geometría
        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    def btn_aceptar(self):
        self.resultado = True
        self.destroy()

    def btn_cancelar(self):
        self.resultado = False
        self.destroy()
