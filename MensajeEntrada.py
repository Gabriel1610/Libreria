class MensajeEntrada(tk.Toplevel):
    """
    Ventana modal moderna para solicitar un texto al usuario (Reemplazo de simpledialog).
    """
    def __init__(self, parent, título, mensaje):
        super().__init__(parent)
        
        # 1. OCULTAR AL NACER
        self.withdraw()
        self.overrideredirect(True)
        
        self.resultado = None # Aquí se guardará lo que escriba el usuario

        # --- Icono de la ventana ---
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

        # Configuración básica
        self.title(título)
        self.configure(bg="white")
        self.resizable(False, False)

        # --- INTERFAZ ---
        frame_principal = tk.Frame(self, bg="white", padx=20, pady=20)
        frame_principal.pack(expand=True, fill="both")

        # Icono visual (Lápiz o Edición)
        lbl_icono = tk.Label(frame_principal, text="📝", font=("Segoe UI", 30), 
                             bg="white", fg="#0078D4")
        lbl_icono.pack(side="left", padx=(0, 15), anchor="n")

        # Contenedor derecho (Mensaje + Entry)
        frame_derecho = tk.Frame(frame_principal, bg="white")
        frame_derecho.pack(side="left", fill="both", expand=True)

        # Mensaje
        lbl_mensaje = tk.Label(frame_derecho, text=mensaje, font=("Segoe UI", 11), 
                               bg="white", fg="#333333", justify="left", wraplength=400)
        lbl_mensaje.pack(side="top", anchor="w", pady=(5, 10))

        # --- CUADRO DE TEXTO (ENTRY) ---
        self.entrada_texto = ttk.Entry(frame_derecho, width=40, font=('Segoe UI', 10))
        self.entrada_texto.pack(side="top", anchor="w", fill="x", pady=(0, 10))
        self.entrada_texto.focus_set() # Poner el foco para escribir directo
        
        # Permitir confirmar con ENTER
        self.entrada_texto.bind("<Return>", lambda event: self.btn_aceptar())
        # Permitir cancelar con ESCAPE
        self.bind("<Escape>", lambda event: self.btn_cancelar())

        # Botones
        frame_botones = tk.Frame(frame_derecho, bg="white")
        frame_botones.pack(side="bottom", anchor="e")
        
        btn_cancelar = ttk.Button(frame_botones, text="Cancelar", command=self.btn_cancelar, style="TButton")
        btn_cancelar.pack(side="right", padx=(5, 0))
        
        btn_aceptar = ttk.Button(frame_botones, text="Aceptar", command=self.btn_aceptar, style="TButton")
        btn_aceptar.pack(side="right")

        # --- LÓGICA DE CENTRADO ---
        self.centrar_en_ventana_padre(parent)

        # Mostrar
        self.overrideredirect(False) 
        self.deiconify() 

        # Hacer modal
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def centrar_en_ventana_padre(self, parent):
        self.update_idletasks()
        ancho_ventana = self.winfo_reqwidth()
        alto_ventana = self.winfo_reqheight()
        
        padre_x = parent.winfo_rootx()
        padre_y = parent.winfo_rooty()
        padre_ancho = parent.winfo_width()
        padre_alto = parent.winfo_height()

        x = padre_x + (padre_ancho // 2) - (ancho_ventana // 2)
        y = padre_y + (padre_alto // 2) - (alto_ventana // 2)

        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    def btn_aceptar(self):
        valor = self.entrada_texto.get().strip()
        if valor:
            self.resultado = valor
            self.destroy()
        else:
            # Opcional: Si quieres que sea obligatorio, no cierras y muestras error, 
            # o simplemente no haces nada. Aquí permitimos vacío = cancelar o retornamos ""
            self.entrada_texto.focus() # Mantener foco

    def btn_cancelar(self):
        self.resultado = None
        self.destroy()