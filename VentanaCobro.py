import tkinter as tk
from tkinter import ttk
import os
import sys
import funciones_útiles
from MensajeModerno import MensajeModerno

NOMBRE_ICONO = "librería.ico"
COLOR_FONDO_APP = "#F4F6F9"
COLOR_BLANCO = "#FFFFFF"
COLOR_ACENTO = "#0078D4"

class VentanaCobro(tk.Toplevel):
    def __init__(self, parent, total_venta, base_de_datos, callback_finalizar):
        super().__init__(parent)
        
        self.total_venta = total_venta
        self.base_de_datos = base_de_datos
        self.callback_finalizar = callback_finalizar # Función a llamar al terminar
        
        # 1. Configuración de Ventana (Oculta al nacer)
        self.withdraw()
        self.overrideredirect(True)
        self.title("Finalizar Venta")
        self.configure(bg=COLOR_BLANCO)
        self.resizable(False, False)

        # --- Icono ---
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

        # --- INTERFAZ ---
        # Frame Principal con borde
        frame_borde = tk.Frame(self, bg=COLOR_ACENTO, padx=2, pady=2)
        frame_borde.pack(fill="both", expand=True)
        
        frame_contenido = tk.Frame(frame_borde, bg=COLOR_BLANCO, padx=20, pady=20)
        frame_contenido.pack(fill="both", expand=True)

        # Título y Total
        lbl_titulo = tk.Label(frame_contenido, text="Finalización de Venta", 
                              font=('Segoe UI', 14, 'bold'), bg=COLOR_BLANCO, fg="#333")
        lbl_titulo.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        lbl_total = tk.Label(frame_contenido, text=f"Total a Pagar: $ {self.total_venta:.2f}", 
                             font=('Segoe UI', 16, 'bold'), bg=COLOR_BLANCO, fg=COLOR_ACENTO)
        lbl_total.grid(row=0, column=2, sticky="e", pady=(0, 15))

        # --- COLUMNA IZQUIERDA: MEDIOS DE PAGO ---
        lbl_medios = tk.Label(frame_contenido, text="Seleccionar medio de pago:", 
                              font=('Segoe UI', 10), bg=COLOR_BLANCO)
        lbl_medios.grid(row=1, column=0, sticky="w", pady=(0, 5))

        self.listbox_medios = tk.Listbox(frame_contenido, height=6, width=25, 
                                         font=('Segoe UI', 10), exportselection=False)
        self.listbox_medios.grid(row=2, column=0, rowspan=4, sticky="ns")
        
        self.listbox_medios.bind("<<ListboxSelect>>", self.manejarSeleccion)

        # Cargar Medios
        self.cargar_medios()

        # --- COLUMNA DERECHA: DATOS DE PAGO ---
        
        # Dinero Recibido
        lbl_recibido = tk.Label(frame_contenido, text="Dinero recibido:", 
                                font=('Segoe UI', 10), bg=COLOR_BLANCO)
        lbl_recibido.grid(row=2, column=2, sticky="w", padx=(20, 0))

        self.var_dinero = tk.StringVar()
        self.entry_dinero = ttk.Entry(frame_contenido, textvariable=self.var_dinero, 
                                      font=('Segoe UI', 11), justify="right", state="disabled")
        self.entry_dinero.grid(row=3, column=2, sticky="ew", padx=(20, 0), pady=(0, 10))

        # Validación
        self.entry_dinero.bind("<Key>", 
                         lambda event: funciones_útiles.controlar_caracteres_precio(
                             self.var_dinero, self.entry_dinero, 10, 2, event
                         ))
        self.entry_dinero.bind("<Return>", lambda e: self.btn_finalizar())

        # Botones
        frame_botones = tk.Frame(frame_contenido, bg=COLOR_BLANCO)
        frame_botones.grid(row=6, column=0, columnspan=3, sticky="e", pady=(20, 0))

        btn_cancelar = ttk.Button(frame_botones, text="Cancelar", command=self.cancelar)
        btn_cancelar.pack(side="left", padx=(0, 10))

        self.btn_cobrar = ttk.Button(frame_botones, text="Finalizar y Facturar", 
                                     command=self.btn_finalizar, state="disabled")
        self.btn_cobrar.pack(side="left")

        # --- LÓGICA DE CENTRADO ---
        self.centrar_en_ventana_padre(parent)
        self.overrideredirect(False) 
        self.deiconify() 
        self.transient(parent)
        self.grab_set()
        # parent.wait_window(self) # No bloqueamos aquí para permitir eventos, controlamos flujo con callback

    def cargar_medios(self):
        medios = self.base_de_datos.consultarMediosPago()
        if medios:
            for m in medios:
                self.listbox_medios.insert(tk.END, m[0])

    def manejarSeleccion(self, event):
        seleccion = self.listbox_medios.curselection()
        if not seleccion:
            self.entry_dinero.config(state="disabled")
            self.btn_cobrar.config(state="disabled")
            return

        nombre = self.listbox_medios.get(seleccion[0])
        self.btn_cobrar.config(state="normal")

        if nombre.lower() == "efectivo":
            self.entry_dinero.config(state="normal")
            self.entry_dinero.focus()
        else:
            self.entry_dinero.config(state="disabled")
            self.var_dinero.set("")

    def btn_finalizar(self):
        seleccion = self.listbox_medios.curselection()
        if not seleccion:
            return

        nombre_medio = self.listbox_medios.get(seleccion[0])

        # Lógica Efectivo
        if nombre_medio.lower() == "efectivo":
            try:
                dinero_str = self.var_dinero.get().strip()
                if not dinero_str:
                    MensajeModerno(self, "Atención", "Ingrese el dinero recibido.", "advertencia")
                    self.entry_dinero.focus()
                    return
                
                recibido = float(dinero_str)
                if recibido < self.total_venta:
                    MensajeModerno(self, "Insuficiente", f"Faltan $ {self.total_venta - recibido:.2f}", "error")
                    return
                
                cambio = recibido - self.total_venta
                if cambio > 0:
                    MensajeModerno(self, "Vuelto", f"Entregar cambio: $ {cambio:.2f}", "éxito")
            
            except ValueError:
                return

        # Cerrar ventana y llamar al proceso principal
        self.destroy()
        self.callback_finalizar(nombre_medio)

    def cancelar(self):
        self.destroy()

    def centrar_en_ventana_padre(self, parent):
        self.update_idletasks()
        ancho = self.winfo_reqwidth()
        alto = self.winfo_reqheight()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (ancho // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")