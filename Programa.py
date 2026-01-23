import tkinter as tk
import os
from tkinter import messagebox
import sys
import base_de_datos
from tkinter import ttk
from tkinter import scrolledtext as st
from tkinter import messagebox
from VentanaCierre import VentanaCierre
import threading
import functools
import facturación
import sys
from datetime import datetime
import funciones_útiles
import validación_tipo_de_datos
from MensajeModerno import MensajeModerno
from tkinter import filedialog # Para elegir dónde guardar
import pandas as pd # Para crear el Excel

NOMBRE_ICONO = "librería.ico"
TAMAÑO_MÍNIMO_COLUMNA1_CPM = 620
TIEMPO_A_ESPERAR_MÁXIMO = 5

# --- Constantes para la UI de Productos ---

# Textos de etiquetas
TÍTULO_LABELFRAME_PRODUCTOS = 'Agregación, edición, control, eliminación y búsqueda de productos'
ETIQUETA_NOMBRE_TEXTO_PRODUCTOS = "Nombre:"
ETIQUETA_PRECIO_TEXTO_PRODUCTOS = "Precio: $ "
ETIQUETA_TOTAL_PRODUCTOS = "Total: $ "
ETIQUETA_VALOR_TOTAL_PRODUCTOS = '0.00'

# Fuentes
FUENTE_TÍTULO_PRODUCTOS = ('Segoe UI', 15, 'bold')
FUENTE_PRECIO_PRODUCTO = ('Segoe UI', 15, 'normal')
FUENTE_TOTAL_PRODUCTO = ('Segoe UI', 15, 'normal')
ESTILO_PRECIO_ENCONTRADO_VENTA = "precio_encontrado.TLabel"

# Parámetros de layout (Grid)
STICKY_LABELFRAME_PRODUCTOS = "nw"
STICKY_WIDGET_OESTE_PRODUCTOS = "w"

PADX_ETIQUETA_NOMBRE_PRODUCTOS = 0
PADY_ETIQUETA_NOMBRE_PRODUCTOS = 0  # Padding específico para la etiqueta nombre
PADX_ENTRADA_IZQUIERDA_NOMBRE_PRODUCTOS = (80, 0)
ANCHO_COLUMNA_NOMBRE_PRODUCTOS = 380
MÁX_CARACTERES_NOMBRE_PRODUCTO = 100
MENSAJE_LÍMITE_NOMBRE_PRODUCTO = f"El nombre del producto no puede superar los {MÁX_CARACTERES_NOMBRE_PRODUCTO} caracteres."

PADX_ETIQUETA_PRECIO_PRODUCTOS = 0
PADY_ETIQUETA_PRECIO_PRODUCTOS = 0  # Padding específico para la etiqueta precio
PADX_ENTRADA_IZQUIERDA_PRECIO_PRODUCTOS = (80, 0)
MÁX_DÍGITOS_PRECIO = 10
MÁX_DECIMALES_PRECIO = 2

PADX_ETIQUETA_UMBRAL_VENTAS_PRODUCTOS = 0
PADY_ETIQUETA_UMBRAL_VENTAS_PRODUCTOS = 0  # Padding específico para la etiqueta umbral de ventas

PADX_ENTRADA_IZQUIERDA_UMBRAL_VENTAS_PRODUCTOS = (110, 0)
PADY_WIDGETS_GENERAL_PRODUCTOS = 5   # Padding vertical para la mayoría de widgets

ANCHO_ENTRADA_NOMBRE_PRODUCTOS = 40
ANCHO_ENTRADA_PRECIO_PRODUCTOS = 20

ETIQUETA_UMBRAL_VENTAS_TEXTO_PRODUCTOS = "Umbral ventas:"
ANCHO_ENTRADA_UMBRAL_VENTAS_PRODUCTOS = 11 # Puedes ajustar este valor según sea necesario
MÁX_UMBRAL_VENTAS_PRODUCTO = 4294967295  # Define el valor máximo permitido para el umbral de ventas
ETIQUETA_VENTAS_ACUM_TEXTO = "Ventas acum.:"
ANCHO_ENTRADA_VENTAS_ACUM_PRODUCTOS = 11 # Puedes ajustar este valor según sea necesario
MÁX_VENTAS_ACUM_PRODUCTO = 4294967295  # Define el valor máximo permitido para el ventas acumuladas
IDX_VENTAS_ACUM = 3
IDX_UMBRAL = 4

PADX_ETIQUETA_VENTAS_ACUM_PRODUCTOS = 0
PADY_ETIQUETA_VENTAS_ACUM_PRODUCTOS = 0  # Padding específico para la etiqueta ventas acumuladas
PADX_ENTRADA_IZQUIERDA_VENTAS_ACUM_PRODUCTOS = (110, 0)

ETIQUETA_DESCRIPCIÓN_TEXTO_PRODUCTOS = "Descripción:"

ANCHO_TEXTO_DESCRIPCIÓN_PRODUCTOS = 30
ALTO_TEXTO_DESCRIPCIÓN_PRODUCTOS = 7
WRAP_TEXTO_DESCRIPCIÓN_PRODUCTOS = tk.WORD
FILASPAN_TEXTO_DESCRIPCIÓN_PRODUCTOS = 4 # Para abarcar filas 1, 2, 3 y 4

PADX_WIDGETS_DESCRIPCIÓN_PRODUCTOS = (10, 0) # Un padding para separarlo de la Col 0
PADY_ETIQUETA_DESCRIPCIÓN_PRODUCTOS = 0
PADY_TEXTO_DESCRIPCIÓN_PRODUCTOS = 5
STICKY_TEXTO_DESCRIPCIÓN_PRODUCTOS = "nsew" # Que se expanda en su celda
MÁX_CAR_DESCRIP = 300
# Máxima cantidad de caracteres permitidos para la descripción de un producto.
# Se utiliza para limitar la longitud de las descripciones en la interfaz de usuario y en la base de datos.

ADVERTENCIA_CANT_CAR_DESCRIP = 10
# Cantidad de caracteres restantes en la descripción a partir de la cual se muestra una advertencia al usuario.
# Sirve para indicar al usuario que está cerca del límite máximo de caracteres permitidos.

ETIQUETA_CÓDIGO_TEXTO_PRODUCTOS = "Código:"
ANCHO_ENTRADA_CÓDIGO_PRODUCTOS = 30  # Puedes ajustar este ancho
PADX_ETIQUETA_CÓDIGO_PRODUCTOS = 0
# Reutilizamos el padding izquierdo de "Nombre" para que se alinee
PADX_ENTRADA_IZQUIERDA_CÓDIGO_PRODUCTOS = PADX_ENTRADA_IZQUIERDA_NOMBRE_PRODUCTOS

# --- Paleta de Colores Moderna ---
COLOR_FONDO_APP = "#F4F6F9"       # Gris muy suave, moderno
COLOR_BLANCO = "#FFFFFF"          # Para contenedores y tablas
COLOR_ACENTO = "#0078D4"          # Azul estilo Windows 11 / VS Code
COLOR_PRESIONADO = "#005A9E"
COLOR_TEXTO = "#2C3E50"           # Gris oscuro, más elegante que el negro
COLOR_TEXTO_SECUNDARIO = "#5F6368"
COLOR_HOVER_BOTON = "#E0E0E0"

# --- Constantes para Botones de Productos ---
TEXTO_BOTÓN_AÑADIR_PRODUCTOS = "Añadir"
TEXTO_BOTÓN_EDITAR_PRODUCTOS = "Editar"
TEXTO_BOTÓN_ELIMINAR_PRODUCTOS = "Eliminar"
TEXTO_BOTÓN_LIMPIAR_PRODUCTOS = "Limpiar"
TEXTO_BOTÓN_BUSCAR_PRODUCTOS = "Buscar"
TEXTO_BOTÓN_MOSTRAR_TODOS_LOS_PRODUCTOS = "Todo"

# --- Constantes para la UI de Ajustes (Medios de Pago) ---
TÍTULO_LABELFRAME_MEDIOS_PAGO = "Medios de pago"
ETIQUETA_EXISTENTES_MEDIOS = "Existentes:"
ETIQUETA_NUEVO_MEDIO = "Nuevo medio de pago:"
BOTÓN_AGREGAR_MEDIO = "Agregar"
BOTÓN_ELIMINAR_MEDIO = "Eliminar"
BOTÓN_EDITAR_MEDIO = "Editar"
MÁX_CARACTERES_NOMBRE_MEDIO_PAGO = 30
BOTÓN_LIMPIAR_MEDIO = "Limpiar"

PADX_BOTÓN_AÑADIR_PRODUCTOS = (0, 0)
PADX_BOTÓN_EDITAR_PRODUCTOS = (100, 0)
PADX_BOTÓN_ELIMINAR_PRODUCTOS = (200, 0)
PADX_BOTÓN_AGREGAR_ALTER_PRODUCTOS = (300, 0)
PADX_BOTÓN_LIMPIAR_PRODUCTOS = (210, 0)
PADX_BOTÓN_BUSCAR_PRODUCTOS = (10, 0)
PADX_BOTÓN_MOSTRAR_TODOS_LOS_PRODUCTOS = (110, 0)

COLUMNA_TOTAL_PRODUCTOS=2
FILA_TOTAL_PRODUCTO = 4
PADX_TOTAL_PRODUCTO = 0
PADY_TOTAL_PRODUCTO = 0
STICKY_TOTAL_PRODUCTO = 'en'

COLUMNA_VALOR_TOTAL_PRODUCTOS = COLUMNA_TOTAL_PRODUCTOS + 1

# --- Constantes para la UI de venta de productos ---
TÍTULO_LABELFRAME_VENTA = "Venta de producto"
ETIQUETA_CÓDIGO_PRODUCTO_VENTA = "Código producto:"
ETIQUETA_CANTIDAD_VENTA = "Cantidad:"
BOTÓN_VER_PRECIO_VENTA = "Ver precio"
BOTÓN_AGREGAR_CARRITO_VENTA = "Agregar al carrito"
BOTÓN_QUITAR_CARRITO_VENTA = "Quitar del carrito"
BOTÓN_LIMPIAR_VENTA = "Limpiar"
BOTÓN_VACIAR_CARRITO_VENTA = "Vaciar carrito"
ETIQUETA_PRECIO_VENTA = ""
MÁX_CARACTERES_CÓDIGO_PRODUCTO = 50
MENSAJE_LÍMITE_CÓDIGO_PRODUCTO = f"El código no puede tener más de {MÁX_CARACTERES_CÓDIGO_PRODUCTO} caracteres."
BOTÓN_FINALIZAR_VENTA = 'Finalizar venta'
BOTÓN_ELIMINAR_VENTA_VENTA = "Eliminar venta"
COLUMNA_BOTÓN_FINALIZAR_VENTA = 6
FILA_BOTÓN_FINALIZAR_VENTA = 1
ANCHO_ENTRADA_CANTIDAD_VENTA = 11
MÁX_CANTIDAD_VENTA = 4294967295  # Define el valor máximo permitido para la cantidad en venta
PADX_GENERAL_VENTA = 5
PADY_GENERAL_VENTA = 5
STICKY_WIDGET_OESTE_VENTA = "w"
STICKY_WIDGET_CENTRO_PRECIO_VENTA = "wens"
UMBRAL_VENTAS_TABLA_ALERTA = 1
VENTAS_ACUM_TABLA_ALERTA = 2

# Constante genérica de evento
EVENTO_TECLA_PRESIONADA = '<Key>'

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

            self.datos = []  # Lista para almacenar los datos que se mostrarán en la tabla.

            self.estado_orden = {
                'productos': (None, False),      # (Columna, Descendente?)
                'ventas': ('fecha_hora', True),  # Por defecto: Fecha descendente
                'stock': (None, False),
                'carrito': (None, False)
            }

        # --- Inicialización de variables y objetos ---
            self.base_de_datos = base_de_datos.BaseDeDatos()  # Crea una instancia de la clase BaseDeDatos.
            self.datos = self.base_de_datos.consultarDatosProductos()  # Lista para almacenar los datos que se mostrarán en la tabla.
            self.hilos = []  # Lista para almacenar los hilos que se creen.
            self.evento_cancelar = threading.Event()  # Evento para cancelar hilos.
            
        #Crea un widget Notebook, que permite tener varias pestañas
            self.cuaderno = ttk.Notebook(self)  
            
            #Crea la primera página del cuaderno (pestaña "Productos").
            self.página_cuaderno_productos = ttk.Frame(self.cuaderno)

            self.página_cuaderno_productos.grid_columnconfigure(0, weight=0)
            self.página_cuaderno_productos.grid_columnconfigure(1, weight=1)

            self.página_cuaderno_productos.grid_rowconfigure(1, weight=1)
            self.página_cuaderno_productos.grid_rowconfigure(4, weight=0)
            self.página_cuaderno_productos.grid_rowconfigure(3, weight=0)

            # Establece un ancho mínimo para la segunda columna (índice 1) de la grilla
            # dentro de la página de productos. Esto asegura que la columna tenga
            # suficiente espacio para mostrar su contenido.
            self.página_cuaderno_productos.grid_columnconfigure(1, minsize=TAMAÑO_MÍNIMO_COLUMNA1_CPM)

            # Añade la página de productos al cuaderno.
            self.cuaderno.add(self.página_cuaderno_productos, text="Productos")

            # Configura la geometría de la ventana principal para que se expanda
            # y ocupe todo el espacio disponible.
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)

            self.configure(bg=COLOR_FONDO_APP) # Fondo de la ventana principal
            self.estilo_apariencia = ttk.Style()
            self.estilo_apariencia.theme_use('clam') # 'clam' permite cambiar colores de fondo más fácilmente que 'vista'
            # Configurar fondo general para Frames y Labels
            self.estilo_apariencia.configure(".", background=COLOR_FONDO_APP, foreground=COLOR_TEXTO)
            self.estilo_apariencia.configure("TFrame", background=COLOR_FONDO_APP)
            self.estilo_apariencia.configure("TLabel", background=COLOR_FONDO_APP, font=('Segoe UI', 11))
            self.estilo_apariencia.configure("TLabelframe", background=COLOR_FONDO_APP)
            self.estilo_apariencia.configure("TLabelframe.Label", background=COLOR_FONDO_APP, foreground=COLOR_ACENTO, font=('Segoe UI', 12, 'bold'))

            # --- Configuración de estilos ---
            self.estilo_apariencia = ttk.Style()
            self.estilo_apariencia.configure("TLabel", font=('Segoe UI', 11))
            self.estilo_apariencia = ttk.Style()  # Crea un objeto de estilo para personalizar la apariencia.
            self.estilo_apariencia.configure("rojo.TLabel", foreground="red")  # Estilo para texto rojo.
            self.estilo_apariencia.configure("verde.TLabel", foreground="#37C11E")  # Estilo para texto verde.
            self.estilo_apariencia.configure("negro.TLabel", foreground="black")  # Estilo para texto negro.
            self.estilo_apariencia.configure("Treeview", rowheight=25)
            self.estilo_apariencia.configure("Treeview.Heading", font=('Segoe UI', 9, 'bold'))
            self.estilo_apariencia.configure("TButton", 
                                font=('Segoe UI', 10, 'bold'),
                                background=COLOR_BLANCO, 
                                foreground=COLOR_TEXTO,
                                borderwidth=1,
                                focusthickness=3,
                                focuscolor=COLOR_ACENTO,
                                padding=6)

            self.estilo_apariencia.map('TButton',
                background=[('pressed', COLOR_PRESIONADO), ('active', COLOR_ACENTO), ('disabled', '#D9D9D9')],
                foreground=[('pressed', 'white'), ('active', 'white'), ('disabled', '#A0A0A0')]
            )

            # Estilo Moderno para la Tabla
            self.estilo_apariencia.configure("Treeview", 
                                            background=COLOR_BLANCO,
                                            fieldbackground=COLOR_FONDO_APP, # Fondo vacío igual a la app
                                            foreground=COLOR_TEXTO,
                                            font=('Segoe UI', 10), # Fuente moderna en las filas
                                            borderwidth=0,
                                            rowheight=30)

            # Estilo Moderno para Encabezados (Header)
            # Usamos un gris azulado suave que combina con tu fondo #F4F6F9
            self.estilo_apariencia.configure("Treeview.Heading", 
                                            background="#E1E5EA", 
                                            foreground=COLOR_TEXTO,
                                            font=('Segoe UI', 10, 'bold'),
                                            relief="flat") # Elimina bordes 3D antiguos
                                            
            # Color de selección (Tu azul de acento)
            self.estilo_apariencia.map('Treeview', 
                background=[('selected', COLOR_ACENTO)],
                foreground=[('selected', 'white')]
            )

            # Estilo para "$1100.50" (encontrado)
            self.estilo_apariencia.configure(ESTILO_PRECIO_ENCONTRADO_VENTA, 
                                            foreground="#008000", 
                                            font=FUENTE_PRECIO_PRODUCTO)

            # Crea la página de "Ventas" dentro del cuaderno de productos.
            self.página_cuaderno_ventas = ttk.Frame(self.cuaderno)
            
            # DESPUÉS (Corregido):
            self.página_cuaderno_ventas.grid_columnconfigure(0, weight=0) # Col 0 (tabla_ventas)
            self.página_cuaderno_ventas.grid_columnconfigure(1, weight=0) # Col 1 (scrollbar_v_ventas)
            self.página_cuaderno_ventas.grid_columnconfigure(2, weight=1) # Col 2 (LF_venta + Carrito) - SÍ SE ESTIRA H
            self.página_cuaderno_ventas.grid_columnconfigure(4, weight=0) # Col 3 (scrollbar_v_carrito)
            
            self.página_cuaderno_ventas.grid_rowconfigure(0, weight=0) # Fila 0 (Etiqueta Ventas / LF Venta)
            self.página_cuaderno_ventas.grid_rowconfigure(1, weight=1) # Fila 1 (Tabla Ventas / LF Venta) - SÍ SE ESTIRA V
            self.página_cuaderno_ventas.grid_rowconfigure(2, weight=0) # Fila 2 (Tabla Ventas / Carrito) - SÍ SE ESTIRA V
            self.página_cuaderno_ventas.grid_rowconfigure(3, weight=0) # Fila 3 (Scrollbar H Ventas / Carrito)
            
            self.cuaderno.add(self.página_cuaderno_ventas, text="Ventas")

            # Guarda los índices de las pestañas de "Productos" y "Ventas" para usarlos luego.
            self.índice_productos = self.cuaderno.index(self.página_cuaderno_productos)
            self.índice_ventas = self.cuaderno.index(self.página_cuaderno_ventas)

            # --- NUEVA PESTAÑA: AJUSTES ---
            self.página_cuaderno_ajustes = ttk.Frame(self.cuaderno)
            
            # Configuración básica de la grilla para que sea flexible
            self.página_cuaderno_ajustes.grid_columnconfigure(0, weight=1)
            self.página_cuaderno_ajustes.grid_rowconfigure(0, weight=1)
            
            # Añadir la pestaña al cuaderno
            self.cuaderno.add(self.página_cuaderno_ajustes, text="Ajustes")
            
            # Guardar el índice (útil si quieres detectar cuándo se abre esta pestaña)
            self.índice_ajustes = self.cuaderno.index(self.página_cuaderno_ajustes)

            # Posiciona el cuaderno (con las pestañas) en la ventana principal.
            self.cuaderno.grid(column=0, row=0, sticky="nsew")

            # Llama a los métodos para crear los diferentes elementos de la interfaz:
            self.crearTablaConProductos()  # Crea la tabla principal.
            self.crearTablaStockAlerta()
            self.crearLabelFrameProductos() # Crea el LabelFrame para agregar productos.
            self.crearTablaConVentas()
            self.crearLabelFrameAdministrarVentas()
            self.crearLabelFrameVentaProducto()
            self.crearTablaCarrito()
            self.actualizarTablaVentasEnHilo()
            self.actualizarListaMediosEnHilo()
            self.crear_label_frame_medios_pago()

            self.etiqueta_total_producto = ttk.Label(self.página_cuaderno_ventas, 
                                                      text=ETIQUETA_TOTAL_PRODUCTOS,
                                                      font=FUENTE_TOTAL_PRODUCTO)
            self.etiqueta_total_producto.grid(column=COLUMNA_TOTAL_PRODUCTOS, row=FILA_TOTAL_PRODUCTO, 
                                    padx=PADX_TOTAL_PRODUCTO, 
                                    pady=PADY_TOTAL_PRODUCTO, 
                                    sticky=STICKY_TOTAL_PRODUCTO)

            self.etiqueta_valor_total_producto = ttk.Label(self.página_cuaderno_ventas, 
                                                      text=ETIQUETA_VALOR_TOTAL_PRODUCTOS,
                                                      font=FUENTE_TOTAL_PRODUCTO)
            self.etiqueta_valor_total_producto.grid(column=COLUMNA_VALOR_TOTAL_PRODUCTOS, row=FILA_TOTAL_PRODUCTO, 
                                    padx=PADX_TOTAL_PRODUCTO, 
                                    pady=PADY_TOTAL_PRODUCTO, 
                                    sticky=STICKY_TOTAL_PRODUCTO)
            
            # Configura la función que se ejecutará cuando se cierre la ventana.
            self.protocol("WM_DELETE_WINDOW", self.cerrarVentana)
            self.cuaderno.bind("<<NotebookTabChanged>>", self.alCambiarPestaña)
            # Carga los datos en la tabla productos (en un hilo separado).
            self.cargarDatosEnTablaEnHilo()

        except Exception as e:
            MensajeModerno(self, "Error crítico", f"Fallo en inicialización: {str(e)}", tipo="error")
            sys.exit(1)
    
    def alCambiarPestaña(self, event):
        """
        Detecta cuando el usuario cambia de pestaña.
        Si la pestaña seleccionada es "Ventas", pone el foco en la entrada de código.
        """
        try:
            # Verificar si la ventana principal aún existe
            if not self.winfo_exists():
                return

            # Obtener el índice de la pestaña actual
            pestaña_actual = self.cuaderno.index("current")
            
            def poner_foco_seguro(widget):
                # Verificar si el widget específico aún existe antes de enfocar
                if widget.winfo_exists():
                    widget.focus()

            # Verificar si es la pestaña de Ventas
            if pestaña_actual == self.índice_ventas:
                # Usamos after_idle con la función segura
                self.after_idle(lambda: poner_foco_seguro(self.entrada_código_producto_venta))
            else:
                self.after_idle(lambda: poner_foco_seguro(self.entrada_código))
                
        except (tk.TclError, Exception):
            pass # Ignorar errores si la app se está cerrando

    def crearTablaConProductos(self):

        # --- 1. Crear la Etiqueta ---
        self.etiqueta_título_labelframe_productos = ttk.Label(self.página_cuaderno_productos, 
                                               text="Productos", 
                                               font=FUENTE_TÍTULO_PRODUCTOS) # Re-usamos la fuente
        
        # Posicionar la etiqueta (Fila 4, debajo del formulario)
        self.etiqueta_título_labelframe_productos.grid(column=0, row=0, columnspan=2, 
                                        padx=5, pady=(2, 2), sticky="w")
        
        columnas = (
            'código',
            'nombre',
            'precio',
            'ventas_acum',
            'umbral_ventas',
            'descripción',
            'alternativa',
            'id'
        )

        self.tabla_productos = ttk.Treeview(
            self.página_cuaderno_productos,
            columns=columnas,
            show='headings',
            height=5
        )

        # Configuración de Encabezados Visibles
        self.tabla_productos.heading('código', text='Código')
        self.tabla_productos.heading('nombre', text='Nombre')
        self.tabla_productos.heading('precio', text='Precio')
        self.tabla_productos.heading('ventas_acum', text='Ventas Acum.')
        self.tabla_productos.heading('umbral_ventas', text='Umbral Objetivo')
        self.tabla_productos.heading('descripción', text='Descripción', anchor='w')
        
        # (No configuramos heading para alternativa/id para que no se vean títulos extraños)

        # Habilitar ordenamiento (solo para las columnas visibles)
        columnas_visibles = ('código', 'nombre', 'precio', 'ventas_acum', 'umbral_ventas', 'descripción')
        for col in columnas_visibles:
            self.tabla_productos.heading(col, command=lambda c=col: self.ordenarColumna(self.tabla_productos, c, False, 'productos'))
        self.tabla_productos.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky='ns'
        )

        self.tabla_productos.column(
            "código",
            anchor='w',
            width=205,
            minwidth=205,
            stretch=tk.NO
        )
        self.tabla_productos.column(
            "nombre",
            anchor='w',
            width=ANCHO_COLUMNA_NOMBRE_PRODUCTOS,
            minwidth=ANCHO_COLUMNA_NOMBRE_PRODUCTOS,
            stretch=tk.NO
        )
        self.tabla_productos.column(
            "precio",
            anchor='center',
            width=90,
            minwidth=90,
            stretch=tk.NO
        )
        
        self.tabla_productos.column(
            "ventas_acum",
            anchor='center',
            width=110,
            minwidth=110,
            stretch=tk.NO
        )
        
        self.tabla_productos.column(
            "umbral_ventas",
            anchor='center',
            width=120,
            minwidth=120,
            stretch=tk.NO
        )
        self.tabla_productos.column(
            "descripción",
            width=1000,
            minwidth=1000,
            stretch=tk.NO
        )

        self.tabla_productos.column(
            "alternativa",
            width=0,
            stretch=tk.NO
        )

        self.tabla_productos.column(
            "id", 
            width=0, 
            stretch=tk.NO
        )

        self.barra_desplazamiento_vertical = ttk.Scrollbar(
            self.página_cuaderno_productos,
            orient=tk.VERTICAL,
            command=self.tabla_productos.yview
        )
        self.barra_desplazamiento_horizontal = ttk.Scrollbar(
            self.página_cuaderno_productos,
            orient=tk.HORIZONTAL,
            command=self.tabla_productos.xview
        )

        self.tabla_productos.configure(xscrollcommand=self.barra_desplazamiento_horizontal.set)
        self.tabla_productos.configure(yscrollcommand=self.barra_desplazamiento_vertical.set)

        self.barra_desplazamiento_vertical.grid(row=1, column=3, sticky='ns')
        self.barra_desplazamiento_horizontal.grid(row=2, column=0, columnspan=2, sticky='we')

        self.tabla_productos.bind("<<TreeviewSelect>>", self.cargarRegistros)

    def crearTablaStockAlerta(self):
        """
        Crea la etiqueta y la tabla (Treeview) para mostrar los productos
        con bajo stock (o alerta de ventas) en la pestaña de productos.
        """
        # --- 1. Crear la Etiqueta ---
        self.etiqueta_stock_alerta = ttk.Label(self.página_cuaderno_productos, 
                                               text="Stock en alerta", 
                                               font=FUENTE_TÍTULO_PRODUCTOS)
        
        self.etiqueta_stock_alerta.grid(column=1, row=3, columnspan=2, 
                                        padx=10, pady=(0, 0), sticky="w")

        # --- 2. Definir Columnas ---
        columnas_stock = ('código', 'nombre')

        self.tabla_stock_alerta = ttk.Treeview(
            self.página_cuaderno_productos,
            columns=columnas_stock,
            show='headings',
            height=11,  # REDUCIDO DE 12 A 11
            selectmode='extended'  # CAMBIADO DE 'none' A 'extended'
        )

        # 3. Configurar tags de estilo
        self.tabla_stock_alerta.tag_configure('alerta', foreground='red', background='#FFF0F0')
        self.tabla_stock_alerta.tag_configure('impar', background=COLOR_BLANCO)
        self.tabla_stock_alerta.tag_configure('par', background=COLOR_FONDO_APP)

        # --- 4. Definir Encabezados ---
        self.tabla_stock_alerta.heading('código', text='Código', anchor='w')
        self.tabla_stock_alerta.heading('nombre', text='Nombre', anchor='w')
        
        for col in columnas_stock:
            self.tabla_stock_alerta.heading(col, command=lambda c=col: self.ordenarColumna(self.tabla_stock_alerta, c, False, 'stock'))

        # --- 5. Posicionar la Tabla ---
        self.tabla_stock_alerta.grid(
            row=4,
            column=1,
            padx=(10, 0),
            columnspan=2,
            sticky='nsew'
        )

        # --- 6. Definir Anchos de Columna ---
        self.tabla_stock_alerta.column("código", anchor='w', width=150, stretch=tk.NO)
        self.tabla_stock_alerta.column("nombre", anchor='w', width=300, stretch=tk.YES)
        
        # --- 7. Scrollbars ---
        self.barra_desplazamiento_vertical_stock = ttk.Scrollbar(
            self.página_cuaderno_productos,
            orient=tk.VERTICAL,
            command=self.tabla_stock_alerta.yview
        )
        self.barra_desplazamiento_horizontal_stock = ttk.Scrollbar(
            self.página_cuaderno_productos,
            orient=tk.HORIZONTAL,
            command=self.tabla_stock_alerta.xview
        )

        self.tabla_stock_alerta.configure(xscrollcommand=self.barra_desplazamiento_horizontal_stock.set)
        self.tabla_stock_alerta.configure(yscrollcommand=self.barra_desplazamiento_vertical_stock.set)

        self.barra_desplazamiento_vertical_stock.grid(row=4, column=3, sticky='ns')
        self.barra_desplazamiento_horizontal_stock.grid(row=5, column=1, columnspan=2, sticky='we')

        # --- 8. NUEVO: Botón Eliminar Alerta ---
        self.btn_eliminar_alerta = ttk.Button(self.página_cuaderno_productos, 
                                              text="Eliminar", 
                                              state='disabled', 
                                              command=self.resetearVentasAcumuladas)
        
        # Lo ponemos en la fila 6, alineado a la derecha
        self.btn_eliminar_alerta.grid(row=6, column=2, padx=0, pady=(5, 0), sticky="e")

        # --- 9. NUEVO: Lógica de Habilitación ---
        def habilitar_btn_alerta(event):
            if self.tabla_stock_alerta.selection():
                self.btn_eliminar_alerta.config(state='normal')
            else:
                self.btn_eliminar_alerta.config(state='disabled')

        self.tabla_stock_alerta.bind("<<TreeviewSelect>>", habilitar_btn_alerta)
    
    def resetearVentasAcumuladas(self):
        """
        Resetea las ventas acumuladas a 0 para los productos seleccionados en la tabla de alertas.
        Esto los saca de la lista de alertas.
        """
        # 1. Obtener selección
        selección = self.tabla_stock_alerta.selection()
        if not selección:
            return

        # 2. Confirmar
        confirmacion = MensajeModerno(self, "Resetear Ventas", 
                                      "¿Está seguro de eliminar la alerta para los productos seleccionados?\n\n"
                                      "Esto pondrá sus ventas acumuladas en 0.", tipo="pregunta")
        
        if confirmacion.resultado:
            try:
                codigos_procesados = 0
                
                # 3. Iterar y actualizar
                for item_id in selección:
                    item = self.tabla_stock_alerta.item(item_id)
                    código = item['values'][0] # El código es la primera columna
                    
                    # Llamada a la base de datos
                    self.base_de_datos.resetearVentasProducto(código)
                    codigos_procesados += 1

                # 4. Actualizar interfaz
                self.datos = self.base_de_datos.consultarDatosProductos() # Recargar datos generales
                self.cargarDatosEnTablaEnHilo()
                
                # Deshabilitar botón
                self.btn_eliminar_alerta.config(state='disabled')
                
                MensajeModerno(self, "Éxito", f"Se resetearon las ventas de {codigos_procesados} productos.", tipo="éxito")

            except Exception as e:
                MensajeModerno(self, "Error", f"Error al resetear ventas: {e}", tipo="error")

    def quitarDelCarrito(self):
        """
        Verifica si hay una fila seleccionada en self.tabla_carrito. 
        Si la hay, elimina la fila y actualiza el total de la venta. 
        Si no la hay, muestra un mensaje de advertencia.
        """
        
        # 1. Obtener los ítems seleccionados
        ítems_seleccionados = self.tabla_carrito.selection()
        
        # 2. Verificar la selección
        if not ítems_seleccionados:
            MensajeModerno(self,"Atención", "Debe seleccionar una fila del carrito para poder quitarla.", tipo="advertencia")
            return

        # 3. Procesar el ítem seleccionado (solo tomamos el primero)
        item_id = ítems_seleccionados[0]
        
        # 4. Obtener el subtotal de la fila a eliminar
        datos_fila = self.tabla_carrito.item(item_id, 'values')
        
        # El subtotal es el último valor en la tupla de la tabla
        subtotal_str = datos_fila[-1]

        subtotal_a_restar = float(subtotal_str)
        
        # 5. Eliminar la fila de la tabla
        self.tabla_carrito.delete(item_id)
        
        # 6. Actualizar el total de la venta

        # Obtener el total actual de la etiqueta
        total_actual_str = self.etiqueta_valor_total_producto.cget('text')
        total_actual_float = float(total_actual_str)
        nuevo_total_float = total_actual_float - subtotal_a_restar

        self.etiqueta_valor_total_producto.config(text=f"{nuevo_total_float:.2f}")

    def crearTablaConVentas(self):
        """
        Crea la etiqueta y la tabla (Treeview) para mostrar el listado de ventas.
        """
        
        # --- 1. Etiqueta ---
        self.etiqueta_título_ventas = ttk.Label(self.página_cuaderno_ventas, 
                                               text="Ventas", 
                                               font=FUENTE_TÍTULO_PRODUCTOS)
        self.etiqueta_título_ventas.grid(column=0, row=0, padx=5, pady=(2, 2), sticky="w")

        # --- 2. Definir Columnas (AGREGADO 'medio') ---
        columnas_ventas = ('id', 'fecha_hora', 'medio', 'total')

        self.tabla_ventas = ttk.Treeview(
            self.página_cuaderno_ventas,
            columns=columnas_ventas,
            show='headings',
            height=15
        )

        # --- 3. Encabezados ---
        self.tabla_ventas.heading('id', text='ID', anchor='center')
        self.tabla_ventas.heading('fecha_hora', text='Fecha y hora', anchor='center')
        self.tabla_ventas.heading('medio', text='Medio Pago', anchor='center') # <-- NUEVO
        self.tabla_ventas.heading('total', text='Total', anchor='center')

        # Ordenamiento
        for col in columnas_ventas:
            self.tabla_ventas.heading(col, command=lambda c=col: self.ordenarColumna(self.tabla_ventas, c, False, 'ventas'))

        # --- 4. Posición ---
        self.tabla_ventas.grid(row=1, column=0, rowspan=2, sticky='nsw')

        # --- 5. Anchos de Columna (Ajustados) ---
        self.tabla_ventas.column("id", anchor='center', width=50, stretch=tk.NO)
        self.tabla_ventas.column("fecha_hora", anchor='center', width=130, stretch=tk.NO)
        self.tabla_ventas.column("medio", anchor='center', width=100, stretch=tk.YES) # <-- NUEVO (Se estira)
        self.tabla_ventas.column("total", anchor='e', width=100, stretch=tk.NO)
        
        # --- 6. Scrollbars ---
        self.barra_desplazamiento_vertical_ventas = ttk.Scrollbar(
            self.página_cuaderno_ventas, orient=tk.VERTICAL, command=self.tabla_ventas.yview)
        self.barra_desplazamiento_horizontal_ventas = ttk.Scrollbar(
            self.página_cuaderno_ventas, orient=tk.HORIZONTAL, command=self.tabla_ventas.xview)

        self.tabla_ventas.configure(xscrollcommand=self.barra_desplazamiento_horizontal_ventas.set)
        self.tabla_ventas.configure(yscrollcommand=self.barra_desplazamiento_vertical_ventas.set)

        # Posicionar scrollbars
        self.barra_desplazamiento_vertical_ventas.grid(row=1, column=1, rowspan=2, sticky='ns')
        self.barra_desplazamiento_horizontal_ventas.grid(row=3, column=0, sticky='nwe')
        
        # Bind del click
        self.tabla_ventas.bind("<<TreeviewSelect>>", self.cargarDetalleVentaEnCarrito)

    def crearLabelFrameProductos(self):
        # --- Creación de Widgets ---

        self.etiqueta_título_labelframe_productos = ttk.Label(self.página_cuaderno_productos, 
                                                        text=TÍTULO_LABELFRAME_PRODUCTOS, 
                                                        font=FUENTE_TÍTULO_PRODUCTOS)
        self.labelframe_productos = ttk.LabelFrame(self.página_cuaderno_productos, 
                                                labelwidget=self.etiqueta_título_labelframe_productos)

        self.labelframe_productos.grid(column=0, row=3, rowspan=3, 
                                    padx=PADX_ETIQUETA_NOMBRE_PRODUCTOS, 
                                    pady=PADY_ETIQUETA_NOMBRE_PRODUCTOS,
                                    sticky=STICKY_LABELFRAME_PRODUCTOS)

        self.etiqueta_código = ttk.Label(self.labelframe_productos, text=ETIQUETA_CÓDIGO_TEXTO_PRODUCTOS)
        self.etiqueta_código.grid(column=0, row=0, 
                                padx=PADX_ETIQUETA_CÓDIGO_PRODUCTOS, 
                                pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        self.código = tk.StringVar()
        self.entrada_código = ttk.Entry(self.labelframe_productos, 
                                    width=ANCHO_ENTRADA_CÓDIGO_PRODUCTOS, 
                                    textvariable=self.código)
        self.entrada_código.grid(column=0, row=0, 
                                padx=PADX_ENTRADA_IZQUIERDA_CÓDIGO_PRODUCTOS, 
                                pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        self.entrada_código.bind(EVENTO_TECLA_PRESIONADA, 
            lambda event: self.limitar_longitud_entrada(
                event, 
                self.entrada_código, 
                self.código, 
                MÁX_CARACTERES_CÓDIGO_PRODUCTO, 
                MENSAJE_LÍMITE_CÓDIGO_PRODUCTO
            )
        )

        # --- Nombre ---
        self.etiqueta_nombre = ttk.Label(self.labelframe_productos, text=ETIQUETA_NOMBRE_TEXTO_PRODUCTOS)
        self.etiqueta_nombre.grid(column=0, row=1, 
                                padx=PADX_ETIQUETA_NOMBRE_PRODUCTOS, 
                                pady=PADY_ETIQUETA_NOMBRE_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        self.nombre = tk.StringVar()
        self.entrada_nombre = ttk.Entry(self.labelframe_productos, 
                                    width=ANCHO_ENTRADA_NOMBRE_PRODUCTOS, 
                                    textvariable=self.nombre)
        self.entrada_nombre.grid(column=0, row=1, 
                                padx=PADX_ENTRADA_IZQUIERDA_NOMBRE_PRODUCTOS, 
                                pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        self.entrada_nombre.bind(EVENTO_TECLA_PRESIONADA, 
            lambda event: self.limitar_longitud_entrada(
                event, 
                self.entrada_nombre, 
                self.nombre, 
                MÁX_CARACTERES_NOMBRE_PRODUCTO,  # Límite máximo
                MENSAJE_LÍMITE_NOMBRE_PRODUCTO # Mensaje
            )
        )

        # --- Precio ---
        self.etiqueta_precio = ttk.Label(self.labelframe_productos, text=ETIQUETA_PRECIO_TEXTO_PRODUCTOS)
        self.etiqueta_precio.grid(column=0, row=2, 
                                padx=PADX_ETIQUETA_PRECIO_PRODUCTOS, 
                                pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        self.precio = tk.StringVar()
        self.entrada_precio = ttk.Entry(self.labelframe_productos, 
                                    width=ANCHO_ENTRADA_PRECIO_PRODUCTOS, 
                                    textvariable=self.precio)
        self.entrada_precio.grid(column=0, row=2, 
                                padx=PADX_ENTRADA_IZQUIERDA_PRECIO_PRODUCTOS, 
                                pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)

        # Bindeo con la constante de evento
        self.entrada_precio.bind(EVENTO_TECLA_PRESIONADA, 
                                lambda event: funciones_útiles.controlar_caracteres_precio(
                                    self.precio, 
                                    self.entrada_precio, 
                                    máx_dígitos=MÁX_DÍGITOS_PRECIO, 
                                    máx_decimales=MÁX_DECIMALES_PRECIO, 
                                    event=event))
        self.etiqueta_umbral = ttk.Label(self.labelframe_productos, text=ETIQUETA_UMBRAL_VENTAS_TEXTO_PRODUCTOS)
        self.etiqueta_umbral.grid(column=0, row=3,
                                padx=PADX_ETIQUETA_UMBRAL_VENTAS_PRODUCTOS, 
                                pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        self.umbral = tk.StringVar()
        self.entrada_umbral = ttk.Entry(self.labelframe_productos, 
                                    width=ANCHO_ENTRADA_UMBRAL_VENTAS_PRODUCTOS, 
                                    textvariable=self.umbral)
        self.entrada_umbral.grid(column=0, row=3,
                                padx=PADX_ENTRADA_IZQUIERDA_UMBRAL_VENTAS_PRODUCTOS, 
                                pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        
        self.entrada_umbral.bind(EVENTO_TECLA_PRESIONADA, 
                                lambda event, widget=self.entrada_umbral, var=self.umbral: 
                                self.controlar_caracteres_solo_enteros(event, widget, var, max_valor=MÁX_UMBRAL_VENTAS_PRODUCTO))
        
        self.entrada_umbral.bind("<KeyRelease>", self.manejarCambioUmbral)

        self.etiqueta_ventas_acumuladas = ttk.Label(self.labelframe_productos, text=ETIQUETA_VENTAS_ACUM_TEXTO)
        self.etiqueta_ventas_acumuladas.grid(column=0, row=4,
                                        padx=PADX_ETIQUETA_VENTAS_ACUM_PRODUCTOS, 
                                        pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                        sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        self.ventas_acumuladas = tk.StringVar()
        
        self.entrada_ventas_acumuladas = ttk.Entry(self.labelframe_productos, 
                                            width=ANCHO_ENTRADA_VENTAS_ACUM_PRODUCTOS, 
                                            textvariable=self.ventas_acumuladas,
                                            state='disabled') 
        
        self.entrada_ventas_acumuladas.grid(column=0, row=4,
                                        padx=PADX_ENTRADA_IZQUIERDA_VENTAS_ACUM_PRODUCTOS, 
                                        pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                        sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        
        self.entrada_ventas_acumuladas.bind(EVENTO_TECLA_PRESIONADA, 
                                       lambda event, widget=self.entrada_ventas_acumuladas, var=self.ventas_acumuladas: 
                                       self.controlar_caracteres_solo_enteros(event, widget, var, max_valor=MÁX_VENTAS_ACUM_PRODUCTO))

        self.etiqueta_alternativa = ttk.Label(self.labelframe_productos, text="Alternativa:")
        self.etiqueta_alternativa.grid(column=0, row=5, # Fila 5
                                        padx=PADX_ETIQUETA_VENTAS_ACUM_PRODUCTOS, 
                                        pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                        sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        
        self.alternativa = tk.StringVar()
        self.entrada_alternativa = ttk.Entry(self.labelframe_productos, 
                                            width=ANCHO_ENTRADA_CÓDIGO_PRODUCTOS,
                                            textvariable=self.alternativa)
        
        self.entrada_alternativa.grid(column=0, row=5,
                                        padx=PADX_ENTRADA_IZQUIERDA_VENTAS_ACUM_PRODUCTOS, 
                                        pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                        sticky=STICKY_WIDGET_OESTE_PRODUCTOS)

        self.entrada_alternativa.bind(EVENTO_TECLA_PRESIONADA, 
            lambda event: self.limitar_longitud_entrada(
                event, 
                self.entrada_alternativa, 
                self.alternativa, 
                MÁX_CARACTERES_CÓDIGO_PRODUCTO, 
                "El código del producto alternativo es muy largo."
            )
        )

        # --- Descripción (Ajuste de Rowspan) ---
        self.etiqueta_descripción = ttk.Label(self.labelframe_productos, 
                                            text=ETIQUETA_DESCRIPCIÓN_TEXTO_PRODUCTOS)
        self.etiqueta_descripción.grid(column=1, row=0, 
                                    padx=PADX_WIDGETS_DESCRIPCIÓN_PRODUCTOS, 
                                    pady=PADY_ETIQUETA_DESCRIPCIÓN_PRODUCTOS, 
                                    sticky=STICKY_WIDGET_OESTE_PRODUCTOS)

        self.texto_desplazado = st.ScrolledText(self.labelframe_productos, 
                                                width=ANCHO_TEXTO_DESCRIPCIÓN_PRODUCTOS, 
                                                height=ALTO_TEXTO_DESCRIPCIÓN_PRODUCTOS, 
                                                wrap=WRAP_TEXTO_DESCRIPCIÓN_PRODUCTOS,
                                                font=('Segoe UI', 10),
                                                relief="solid", borderwidth=1,
                                                padx=10, pady=10,
                                                bg=COLOR_BLANCO, fg=COLOR_TEXTO,
                                                selectbackground=COLOR_ACENTO, selectforeground="white")

        self.texto_desplazado.grid(column=1, row=1, 
                                rowspan=5, # <-- AUMENTADO DE 4 A 5
                                padx=PADX_WIDGETS_DESCRIPCIÓN_PRODUCTOS, 
                                pady=PADY_TEXTO_DESCRIPCIÓN_PRODUCTOS, 
                                sticky=STICKY_TEXTO_DESCRIPCIÓN_PRODUCTOS)

        self.texto_desplazado.bind(EVENTO_TECLA_PRESIONADA, self.limitar_caracteres_descripción)

        # Contador de caracteres
        self.etiqueta_contador_caracteres = ttk.Label(self.labelframe_productos, text=str(MÁX_CAR_DESCRIP))
        self.etiqueta_contador_caracteres.grid(column=1, row=6, padx=(300, 0), pady=(0, 0), sticky="w") # <-- Fila 6
        self.etiqueta_contador_caracteres.configure(style="verde.TLabel")

        # --- Botones ---

        # 1. Añadir
        self.botón_añadir_productos = ttk.Button(self.labelframe_productos, 
                                                 text=TEXTO_BOTÓN_AÑADIR_PRODUCTOS, 
                                                 #image=self.ico_add, 
                                                 compound="left",
                                                 command=self.añadirProducto)
        self.botón_añadir_productos.grid(column=0, row=7, padx=PADX_BOTÓN_AÑADIR_PRODUCTOS, pady=PADY_WIDGETS_GENERAL_PRODUCTOS, sticky=STICKY_WIDGET_OESTE_PRODUCTOS)

        # 2. Editar
        self.botón_editar_productos = ttk.Button(self.labelframe_productos, 
                                                 text=TEXTO_BOTÓN_EDITAR_PRODUCTOS, 
                                                 #image=self.ico_edit, 
                                                 compound="left",
                                                 command=self.editarProducto)
        self.botón_editar_productos.grid(column=0, row=7, padx=PADX_BOTÓN_EDITAR_PRODUCTOS, pady=PADY_WIDGETS_GENERAL_PRODUCTOS, sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        
        # 3. Eliminar
        self.botón_eliminar_productos = ttk.Button(self.labelframe_productos, 
                                                   text=TEXTO_BOTÓN_ELIMINAR_PRODUCTOS, 
                                                   #image=self.ico_del, 
                                                   compound="left",
                                                   command=self.eliminarProducto)
        self.botón_eliminar_productos.grid(column=0, row=7, padx=PADX_BOTÓN_ELIMINAR_PRODUCTOS, pady=PADY_WIDGETS_GENERAL_PRODUCTOS, sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        
        # 4. Elegir Alternativa
        # Nota: Asigna la función que desees en 'command'
        self.botón_alternativa = ttk.Button(self.labelframe_productos, 
                                                  text="Elegir Alt.", # O una constante
                                                  # image=self.ico_clean, # Opcional: Icono nuevo
                                                  compound="left",
                                                  command=self.elegirAlternativa) 
        self.botón_alternativa.grid(column=0, row=7, padx=PADX_BOTÓN_AGREGAR_ALTER_PRODUCTOS, pady=PADY_WIDGETS_GENERAL_PRODUCTOS, sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
    
        # 5. Buscar
        self.botón_buscar_productos = ttk.Button(self.labelframe_productos, 
                                                  text=TEXTO_BOTÓN_BUSCAR_PRODUCTOS, 
                                                  #image=self.ico_search, 
                                                  compound="left",
                                                  command=self.buscarProducto)
        self.botón_buscar_productos.grid(column=1, row=7, padx=PADX_BOTÓN_BUSCAR_PRODUCTOS, pady=PADY_WIDGETS_GENERAL_PRODUCTOS, sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        
        # 6. Todo
        self.botón_mostrar_todos_los_productos = ttk.Button(self.labelframe_productos, text=TEXTO_BOTÓN_MOSTRAR_TODOS_LOS_PRODUCTOS,
                                                            #image=self.ico_all, 
                                                            compound="left",
                                                            command=self.mostrarTodosLosProductos)
        self.botón_mostrar_todos_los_productos.grid(column=1, row=7, padx=PADX_BOTÓN_MOSTRAR_TODOS_LOS_PRODUCTOS, pady=PADY_WIDGETS_GENERAL_PRODUCTOS, sticky=STICKY_WIDGET_OESTE_PRODUCTOS)

        # 7. Limpiar (MOVIDO a la derecha de Todo)
        # Necesitarás ajustar el PADX o crear una nueva constante
        self.botón_limpiar_productos = ttk.Button(self.labelframe_productos, 
                                                  text=TEXTO_BOTÓN_LIMPIAR_PRODUCTOS, 
                                                  #image=self.ico_clean, 
                                                  compound="left",
                                                  command=self.limpiarCamposProductos)
        # Lo ponemos a la derecha de "Todo" (110 + ancho de todo aprox = 210)
        self.botón_limpiar_productos.grid(column=1, row=7, padx=PADX_BOTÓN_LIMPIAR_PRODUCTOS, pady=PADY_WIDGETS_GENERAL_PRODUCTOS, sticky=STICKY_WIDGET_OESTE_PRODUCTOS)

        self.botón_ver_alternativa = ttk.Button(self.labelframe_productos, 
                                                text="Ver Alternativa", 
                                                command=self.verAlternativa)
        
        self.botón_ver_alternativa.grid(column=0, row=8, 
                                        padx=PADX_BOTÓN_AÑADIR_PRODUCTOS, 
                                        pady=(0, 5), # Un poco de espacio abajo 
                                        sticky=STICKY_WIDGET_OESTE_PRODUCTOS)

    def verAlternativa(self):
        """
        Busca y muestra los detalles del producto alternativo indicado en el formulario.
        """
        # 1. Obtener el código del campo "Alternativa"
        código_alt = self.alternativa.get().strip()
        
        if not código_alt:
            MensajeModerno(self, "Atención", "El campo 'Alternativa' está vacío.", tipo="advertencia")
            self.entrada_alternativa.focus()
            return

        # 2. Consultar a la Base de Datos
        self.mostrarProductoAlternativo(código_alt)
    
    def verAlternativaVenta(self):
        """
        Busca el producto alternativo asociado al código ingresado en Ventas
        y muestra sus detalles.
        """
        # 1. Obtener código
        codigo_actual = self.código_venta.get().strip()
        
        if not codigo_actual:
            MensajeModerno(self, "Atención", "Ingrese un código de producto para ver su alternativa.", tipo="advertencia")
            self.entrada_código_producto_venta.focus()
            return
            
        prod_actual = self.base_de_datos.buscarProductoPorCódigo(codigo_actual)
            
        if not prod_actual:
            MensajeModerno(self, "No encontrado", "El producto ingresado no existe.", tipo="error")
            return

        id_alternativa = prod_actual[7] # El ID de la alternativa está al final

        if not id_alternativa:
            MensajeModerno(self, "Sin alternativa", "Este producto no tiene una alternativa configurada.", tipo="info")
            return
            
        prod_alt = self.base_de_datos.obtenerProductoPorID(id_alternativa)
        self.mostrarProductoAlternativo(prod_alt[0]) # El código está en el índice 0
    
    def mostrarProductoAlternativo(self, código_alt):
        try:
            producto = self.base_de_datos.buscarProductoPorCódigo(código_alt)
            
            if producto:
                # producto = (código, nombre, precio, ventas, umbral, desc, id, id_alt)
                # Indices: 0=Cod, 1=Nom, 2=Precio, 5=Desc
                
                info = f"Código: {producto[0]}\n" \
                       f"Nombre: {producto[1]}\n" \
                       f"Precio: $ {producto[2]}\n\n" \
                       f"Descripción:\n{producto[5]}"
                
                # Mostrar en ventana de información (tipo 'exito' usa el check verde, o usa 'info' si prefieres)
                MensajeModerno(self, "Detalles de Alternativa", info, tipo="exito")
            
            else:
                MensajeModerno(self, "No encontrado", f"No existe ningún producto con el código '{código_alt}'.", tipo="error")

        except Exception as e:
            MensajeModerno(self, "Error", f"Error al consultar alternativa: {e}", tipo="error")
            
    def mostrarTodosLosProductos(self):
        """
        Muestra todos los productos en la tabla, limpiando cualquier filtro o búsqueda previa.
        """
        # Limpia los campos antes de cargar los datos
        self.limpiarCamposProductos()

        # Borra todas las filas existentes en la tabla
        funciones_útiles.borrarTodasLasFilas(self.tabla_productos)

        # Actualiza 'self.datos' con todos los productos de la base de datos
        self.datos = self.base_de_datos.consultarDatosProductos()

        # Carga todos los datos en la tabla
        self.cargarTablaProducto()  # Llama a la función que SÍ usa self.datos

    def crearLabelFrameVentaProducto(self):
        """
        Crea el LabelFrame para agregar productos a una venta en la pestaña 'Ventas'.
        """

        # 1. Crear la ETIQUETA del título primero
        self.etiqueta_título_venta = ttk.Label(self.página_cuaderno_ventas, 
                                               text=TÍTULO_LABELFRAME_VENTA, 
                                               font=FUENTE_TÍTULO_PRODUCTOS)
        
        # 2. Crear el LabelFrame y pasar la etiqueta como 'labelwidget'
        self.labelframe_venta_producto = ttk.LabelFrame(self.página_cuaderno_ventas, 
                                                        labelwidget=self.etiqueta_título_venta)
        
        # 3. Posicionar el LabelFrame
        self.labelframe_venta_producto.grid(column=1, row=5, # <-- CAMBIO: Empieza en Columna 1
                                            columnspan=3,
                                            padx=PADX_GENERAL_VENTA, 
                                            pady=PADY_GENERAL_VENTA,
                                            sticky="wn") # Se pega arriba, no se expande

        # --- Fila 0 (Interior) ---
        
        # Etiqueta "Código producto"
        self.etiqueta_código_producto_venta = ttk.Label(self.labelframe_venta_producto, 
                                               text=ETIQUETA_CÓDIGO_PRODUCTO_VENTA)
        self.etiqueta_código_producto_venta.grid(column=0, row=0, 
                                      padx=PADX_GENERAL_VENTA, 
                                      pady=PADY_GENERAL_VENTA, 
                                      sticky=STICKY_WIDGET_OESTE_VENTA)
        
        # Caja de texto (Código)
        self.código_venta = tk.StringVar()
        self.entrada_código_producto_venta = ttk.Entry(self.labelframe_venta_producto, 
                                            width=ANCHO_ENTRADA_CÓDIGO_PRODUCTOS, 
                                            textvariable=self.código_venta)
        self.entrada_código_producto_venta.grid(column=1, row=0, 
                                      padx=PADX_GENERAL_VENTA, 
                                      pady=PADY_GENERAL_VENTA, 
                                      sticky=STICKY_WIDGET_OESTE_VENTA)
        self.entrada_código_producto_venta.bind(EVENTO_TECLA_PRESIONADA, 
            lambda event: self.limitar_longitud_entrada(
                event, 
                self.entrada_código_producto_venta, 
                self.código_venta, 
                MÁX_CARACTERES_CÓDIGO_PRODUCTO, 
                MENSAJE_LÍMITE_CÓDIGO_PRODUCTO
            )
        )
        # Botón "Ver precio"
        self.botón_ver_precio = ttk.Button(self.labelframe_venta_producto, 
                                           text=BOTÓN_VER_PRECIO_VENTA,
                                           command=self.verPrecioProducto)
        self.botón_ver_precio.grid(column=4, row=0, 
                                   padx=PADX_GENERAL_VENTA, 
                                   pady=PADY_GENERAL_VENTA, 
                                   sticky=STICKY_WIDGET_OESTE_VENTA)

        # botón "Ver Alternativa" ---
        self.botón_ver_alternativa_venta = ttk.Button(self.labelframe_venta_producto, 
                                           text="Ver alternativa",
                                           command=self.verAlternativaVenta)
        self.botón_ver_alternativa_venta.grid(column=5, row=0, # Columna 5
                                   padx=PADX_GENERAL_VENTA, 
                                   pady=PADY_GENERAL_VENTA, 
                                   sticky=STICKY_WIDGET_OESTE_VENTA)

        # --- Fila 1 (Interior) ---
        
        # Etiqueta "Cantidad"
        self.etiqueta_cantidad_venta = ttk.Label(self.labelframe_venta_producto, 
                                                 text=ETIQUETA_CANTIDAD_VENTA)
        self.etiqueta_cantidad_venta.grid(column=2, row=0, 
                                        padx=PADX_GENERAL_VENTA, 
                                        pady=PADY_GENERAL_VENTA, 
                                        sticky=STICKY_WIDGET_OESTE_VENTA)
        
        # Caja de texto (Cantidad)
        self.cantidad_venta = tk.StringVar()
        self.entrada_cantidad_venta = ttk.Entry(self.labelframe_venta_producto, 
                                              width=ANCHO_ENTRADA_CANTIDAD_VENTA, 
                                              textvariable=self.cantidad_venta)
        self.entrada_cantidad_venta.grid(column=3, row=0, 
                                        padx=PADX_GENERAL_VENTA, 
                                        pady=PADY_GENERAL_VENTA, 
                                        sticky=STICKY_WIDGET_OESTE_VENTA)

        self.precio_venta_var = tk.StringVar(value=ETIQUETA_PRECIO_VENTA)

        # Bindeo con la constante de evento
        self.entrada_cantidad_venta.bind(EVENTO_TECLA_PRESIONADA, 
                                       lambda event, widget=self.entrada_cantidad_venta, var=self.cantidad_venta: 
                                       self.controlar_caracteres_solo_enteros(event, widget, var, max_valor=MÁX_CANTIDAD_VENTA))  # Validación de entrada

        # Etiqueta "Precio" (ahora dinámica)
        
        self.etiqueta_precio_venta = ttk.Label(self.labelframe_venta_producto, 
                                                 textvariable=self.precio_venta_var, # Usar textvariable
                                                 style=ESTILO_PRECIO_ENCONTRADO_VENTA,
                                                 anchor='center')
        
        self.etiqueta_precio_venta.grid(column=0, row=1,
                                        columnspan=3, 
                                        padx=PADX_GENERAL_VENTA, 
                                        pady=PADY_GENERAL_VENTA, 
                                        sticky=STICKY_WIDGET_CENTRO_PRECIO_VENTA)
        
        # Botón "Agregar al carrito"
        self.botón_agregar_carrito = ttk.Button(self.labelframe_venta_producto, 
                                                text=BOTÓN_AGREGAR_CARRITO_VENTA,
                                                command=self.agregarAlCarrito)
        self.botón_agregar_carrito.grid(column=6, row=0, 
                                      padx=PADX_GENERAL_VENTA, 
                                      pady=PADY_GENERAL_VENTA, 
                                      sticky=STICKY_WIDGET_OESTE_VENTA)
        
        # Botón "Limpiar"
        self.botón_limpiar = ttk.Button(self.labelframe_venta_producto, 
                                           text=BOTÓN_LIMPIAR_VENTA,
                                           command=self.limpiarCamposVenta)
        self.botón_limpiar.grid(column=7, row=0, 
                                   padx=PADX_GENERAL_VENTA, 
                                   pady=PADY_GENERAL_VENTA, 
                                   sticky=STICKY_WIDGET_OESTE_VENTA)

        # --- Fila 2 (Interior) ---
        
        # Botón "Vaciar carrito"
        self.botón_vaciar_carrito = ttk.Button(self.labelframe_venta_producto, 
                                               text=BOTÓN_VACIAR_CARRITO_VENTA,
                                               command=self.vaciarCarrito) # Asignamos la nueva función
        self.botón_vaciar_carrito.grid(column=4, row=1, # Col 4, Fila 1
                                      padx=PADX_GENERAL_VENTA, 
                                      pady=PADY_GENERAL_VENTA, 
                                      sticky=STICKY_WIDGET_OESTE_VENTA)
        
        # Botón "Quitar del carrito"
        self.botón_quitar_carrito = ttk.Button(self.labelframe_venta_producto, 
                                               text=BOTÓN_QUITAR_CARRITO_VENTA,
                                               command=self.quitarDelCarrito)
        self.botón_quitar_carrito.grid(column=5, row=1, 
                                     padx=PADX_GENERAL_VENTA, 
                                     pady=PADY_GENERAL_VENTA, 
                                     sticky=STICKY_WIDGET_OESTE_VENTA)
        
        # Botón "Finalizar venta"
        self.botón_finalizar_venta = ttk.Button(self.labelframe_venta_producto, 
                                               text=BOTÓN_FINALIZAR_VENTA,
                                               command=self.finalizarVentaEnHilo)
        self.botón_finalizar_venta.grid(column=COLUMNA_BOTÓN_FINALIZAR_VENTA, row=FILA_BOTÓN_FINALIZAR_VENTA, 
                                     padx=PADX_GENERAL_VENTA, 
                                     pady=PADY_GENERAL_VENTA, 
                                     sticky=STICKY_WIDGET_OESTE_VENTA)
    
    def vaciarCarrito(self):
        """
        Verifica si el carrito tiene items. Si los tiene,
        pregunta al usuario si desea vaciar el carrito y, si confirma,
        borra todas las filas de la tabla_carrito y resetea el total.
        """
        
        # 1. Verificar si el carrito está vacío
        if not self.tabla_carrito.get_children():
            # No hay nada que vaciar, no hacer nada.
            return
        
        # 2. Preguntar al usuario (solo si no está vacío)
        confirmación = MensajeModerno(self, "Vaciar Carrito", 
                                        "¿Está seguro de que desea vaciar el carrito?\n"
                                        "Se eliminarán todos los ítems.", tipo="pregunta")
        respuesta = confirmación.resultado
        
        if respuesta: # Si el usuario dijo "Sí"
            # 3. Vaciar la tabla
            funciones_útiles.borrarTodasLasFilas(self.tabla_carrito)
            
            # 4. Resetear el total a 0.00
            self.etiqueta_valor_total_producto.config(text="0.00")
            self.botón_eliminar_venta.config(state='disabled')  # Desactivar el botón "Eliminar venta"
            
            # Deseleccionar filas en tabla_ventas
            self.tabla_ventas.selection_set(())

    def cargarDetalleVentaEnCarrito(self, event=None):
        """
        Se activa al seleccionar una fila de la tabla_ventas.
        
        Advierte al usuario, y si acepta, vacía el carrito actual
        y lo llena con los detalles de la venta histórica seleccionada.
        """
        
        # 1. Obtener la fila seleccionada de la tabla VENTAS
        items_seleccionados = self.tabla_ventas.selection()
        if not items_seleccionados:
            return  # No hacer nada si el clic no seleccionó nada (ej. clic en encabezado)
            
        item_id = items_seleccionados[0]
        datos_venta = self.tabla_ventas.item(item_id, 'values')
        
        # El id_venta es el primer valor (índice 0)
        id_venta_seleccionada = datos_venta[0]

        # 2. Advertir al usuario si el carrito actual NO está vacío
        if self.tabla_carrito.get_children(): # Si hay items en el carrito
            confirmación = MensajeModerno(self, "Sobrescribir Carrito",
                                            "¿Desea vaciar el carrito actual y cargar los detalles de la venta seleccionada?", tipo="pregunta")
            respuesta = confirmación.resultado
            if not respuesta:
                self.tabla_ventas.selection_set(()) # Deseleccionar la fila
                return # El usuario presionó "No"

        # 3. Vaciar el carrito actual
        funciones_útiles.borrarTodasLasFilas(self.tabla_carrito)
        
        try:
            # 4. Consultar los detalles de esa venta
            # (Devuelve: código, nombre, precio_unitario, cantidad, subtotal)
            detalles = self.base_de_datos.consultarDetalleVenta(id_venta_seleccionada)

            if detalles is None:
                MensajeModerno(self, "Error de BD", "No se pudieron consultar los detalles de la venta.", tipo="error")
                self.etiqueta_valor_total_producto.config(text="0.00") # Reset total
                return

            total_recuperado = 0.0

            self.tabla_carrito.tag_configure('impar', background=COLOR_BLANCO)
            self.tabla_carrito.tag_configure('par', background=COLOR_FONDO_APP)

            # 5. Cargar los detalles en la tabla del carrito
            for i, item in enumerate(detalles):
                tag_fila = 'par' if i % 2 == 0 else 'impar'
                self.tabla_carrito.insert('', tk.END, values=item, tags=(tag_fila,))
                
                total_recuperado += float(item[4])

            # 6. Actualizar la etiqueta del total
            self.etiqueta_valor_total_producto.config(text=f"{total_recuperado:.2f}")

            # Activar el botón "Eliminar venta"
            self.botón_eliminar_venta.config(state='normal')

        except Exception as e:
            MensajeModerno(self, "Error", f"Ocurrió un error al cargar los detalles: {str(e)}", tipo="error")
            self.etiqueta_valor_total_producto.config(text="0.00") # Reset total

    def finalizarVenta(self):
        """
        Inicia el proceso de finalización: Valida carrito, confirma monto
        y abre la ventana de selección de medio de pago.
        """
        # 1. Validar Carrito
        items_carrito_ids = self.tabla_carrito.get_children()
        if not items_carrito_ids:
            MensajeModerno(self,"Carrito vacío", "No hay productos en el carrito.", tipo="advertencia")
            return

        # 2. Confirmar Monto
        total_venta_str = self.etiqueta_valor_total_producto.cget('text')
        confirmacion = MensajeModerno(self, "Confirmar Venta", 
                                        f"¿Desea finalizar la venta por un total de $ {total_venta_str}?", tipo="pregunta")
        
        if confirmacion.resultado:
            # 3. Abrir Ventana de Medio de Pago
            self.abrirVentanaMedioPago()
    
    def abrirVentanaMedioPago(self):
        """Abre una ventana modal para seleccionar el medio de pago."""
        
        ventana_pago = tk.Toplevel(self)
        ventana_pago.title("Seleccionar Medio de Pago")
        ventana_pago.geometry("350x200")
        ventana_pago.resizable(False, False)
        ventana_pago.configure(bg="white")
        
        # Centrar
        x = self.winfo_x() + (self.winfo_width() // 2) - 175
        y = self.winfo_y() + (self.winfo_height() // 2) - 100
        ventana_pago.geometry(f"+{x}+{y}")

        # Etiqueta
        lbl = ttk.Label(ventana_pago, text="Seleccione el medio de pago:", background="white", font=('Segoe UI', 11))
        lbl.pack(pady=(20, 10))

        # Obtener medios de la BD (devuelve [(nombre, facturar), ...])
        medios_raw = self.base_de_datos.consultarMediosPago()
        nombres_medios = [m[0] for m in medios_raw] if medios_raw else []

        # Combobox
        combo_medios = ttk.Combobox(ventana_pago, values=nombres_medios, state="readonly", font=('Segoe UI', 10))
        combo_medios.pack(pady=5, padx=20, fill='x')

        # Botón Finalizar (Deshabilitado al inicio)
        botón_finalizar = ttk.Button(ventana_pago, text="Finalizar", state="disabled", style="TButton")
        botón_finalizar.pack(pady=20)

        # Función para habilitar botón
        def habilitar_boton(event):
            botón_finalizar.config(state="normal")
        
        combo_medios.bind("<<ComboboxSelected>>", habilitar_boton)

        # Función para procesar la venta al hacer clic
        def confirmar_pago():
            medio_seleccionado = combo_medios.get()
            ventana_pago.destroy() # Cerrar ventana
            # Llamar a la lógica de guardado pasando el medio
            self.procesarVentaFinal(medio_seleccionado)

        botón_finalizar.config(command=confirmar_pago)
        
        # Hacer modal
        ventana_pago.transient(self)
        ventana_pago.grab_set()
        self.wait_window(ventana_pago)

    def actualizarTablaVentas(self):
        """
        Consulta la base de datos y actualiza la 'tabla_ventas' en la interfaz.
        """
        try:
            self.tabla_ventas.tag_configure('impar', background=COLOR_BLANCO)
            self.tabla_ventas.tag_configure('par', background=COLOR_FONDO_APP)

            # 1. Consultar datos (Ahora trae 4 campos)
            lista_ventas = self.base_de_datos.consultarVentasConTotal()

            # 2. Borrar
            funciones_útiles.borrarTodasLasFilas(self.tabla_ventas)
            
            # 3. Cargar
            if lista_ventas:
                for i, venta in enumerate(lista_ventas):
                    # Desempaquetar tupla: (id, fecha, medio, total)
                    id_v = venta[0]
                    fecha_hora_dt = venta[1]
                    fecha_hora_str = fecha_hora_dt.strftime(funciones_útiles.FORMATO_PREFERIDO_HORA_Y_FECHA)
                    medio_pago = venta[2]     # <-- NUEVO DATO
                    total = f"{venta[3]:.2f}" # <-- AHORA ES ÍNDICE 3
                    
                    tag_fila = 'par' if i % 2 == 0 else 'impar'
                    
                    # Insertar con el nuevo campo
                    self.tabla_ventas.insert('', tk.END, 
                                           values=(id_v, fecha_hora_str, medio_pago, total), 
                                           tags=(tag_fila,))
            
            self.aplicarOrdenGuardado(self.tabla_ventas, 'ventas')
                    
        except Exception as e:
            MensajeModerno(self, "Error", f"No se pudieron cargar las ventas: {str(e)}", tipo="error")
    
    def elegirAlternativa(self):
        """
        Abre una ventana modal para buscar y seleccionar un producto alternativo.
        """
        
        # 1. Crear la ventana
        ventana_alt = tk.Toplevel(self)
        ventana_alt.title("Seleccionar Alternativa")
        ventana_alt.configure(bg="white")
        ventana_alt.resizable(False, False)

        try:
            # Reutilizamos la lógica de ruta segura
            if getattr(sys, 'frozen', False):
                base_dir = sys._MEIPASS
            else:
                base_dir = os.path.dirname(__file__)
            
            ruta_icono = os.path.join(base_dir, NOMBRE_ICONO) # Usamos la constante global
            
            if os.path.exists(ruta_icono):
                ventana_alt.iconbitmap(ruta_icono)
        except Exception:
            pass # Si falla el icono, la ventana abre igual con el default

        # 2. Centrar y definir tamaño (AUMENTADO ALTO a 400)
        ancho_v = 400
        alto_v = 400 # <--- CAMBIO AQUÍ (Más alto)
        x = self.winfo_x() + (self.winfo_width() // 2) - (ancho_v // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (alto_v // 2)
        ventana_alt.geometry(f"{ancho_v}x{alto_v}+{x}+{y}")

        # --- SECCIÓN DE BÚSQUEDA ---
        frame_top = tk.Frame(ventana_alt, bg="white", pady=10)
        frame_top.pack(fill="x", padx=20)

        lbl_buscar = ttk.Label(frame_top, text="Buscar por nombre:", background="white", font=('Segoe UI', 10))
        lbl_buscar.pack(anchor="w")

        entry_buscar = ttk.Entry(frame_top)
        entry_buscar.pack(fill="x", pady=(5, 0))
        entry_buscar.focus() 

        # --- SECCIÓN DE BOTONES (Primero, para asegurar espacio abajo) ---
        # Usamos pack(side="bottom") PRIMERO para que se reserve su espacio al fondo
        frame_botones = tk.Frame(ventana_alt, bg="white", pady=15)
        frame_botones.pack(side="bottom", fill="x", padx=20)

        # Definimos las funciones antes de crear los botones
        def habilitar_seleccion(event):
            if tree_alt.selection():
                btn_seleccionar.config(state="normal")
            else:
                btn_seleccionar.config(state="disabled")

        def realizar_busqueda(event=None):
            texto = entry_buscar.get().strip()
            for item in tree_alt.get_children():
                tree_alt.delete(item)
            btn_seleccionar.config(state="disabled")

            if not texto: return

            resultados = self.base_de_datos.buscarProductoPorNombre(texto)
            if resultados:
                for prod in resultados:
                    cod = prod[0]
                    nom = prod[1]
                    tree_alt.insert('', tk.END, values=(nom, cod))

        def limpiar_busqueda():
            entry_buscar.delete(0, tk.END)
            for item in tree_alt.get_children():
                tree_alt.delete(item)
            btn_seleccionar.config(state="disabled")
            entry_buscar.focus()

        def seleccionar_producto():
            selección = tree_alt.selection()
            if not selección: return
            
            item = tree_alt.item(selección[0])
            codigo_seleccionado = item['values'][1]
            
            codigo_actual = self.código.get().strip()
            if codigo_seleccionado == codigo_actual:
                MensajeModerno(ventana_alt, "Error", "No puede elegir el mismo producto.", tipo="error")
                return

            self.alternativa.set(codigo_seleccionado)
            ventana_alt.destroy()

        # Crear los botones
        btn_buscar = ttk.Button(frame_botones, text="Buscar", command=realizar_busqueda)
        btn_buscar.pack(side="left")

        btn_limpiar = ttk.Button(frame_botones, text="Limpiar", command=limpiar_busqueda)
        btn_limpiar.pack(side="left", padx=10)

        btn_seleccionar = ttk.Button(frame_botones, text="Seleccionar", command=seleccionar_producto, state="disabled")
        btn_seleccionar.pack(side="right")

        # --- TABLA DE RESULTADOS (En el medio) ---
        # Ahora que el top y el bottom están fijos, la tabla usa el espacio restante
        frame_tabla = tk.Frame(ventana_alt, bg="white")
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=5)

        cols = ('nombre', 'código')
        tree_alt = ttk.Treeview(frame_tabla, columns=cols, show='headings') # Sin altura fija, que se expanda
        
        tree_alt.heading('nombre', text='Nombre')
        tree_alt.column('nombre', width=330, anchor='w')
        
        tree_alt.heading('código', text='')
        tree_alt.column('código', width=0, stretch=tk.NO)

        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree_alt.yview)
        tree_alt.configure(yscrollcommand=scroll.set)
        
        tree_alt.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Bindings
        tree_alt.bind("<<TreeviewSelect>>", habilitar_seleccion)
        entry_buscar.bind("<Return>", realizar_busqueda)

        # Modalidad
        ventana_alt.transient(self)
        ventana_alt.grab_set()
        self.wait_window(ventana_alt)
            
    def agregarAlCarrito(self):
        """
        Agrega o actualiza un producto en el carrito de compras.

        1. Valida los campos de entrada.
        2. Consulta el producto en la base de datos.
        3. Verifica si el producto ya existe en el carrito.
        4. Si existe, suma la cantidad nueva a la existente.
        5. Inserta una nueva fila o actualiza la existente.
        6. Actualiza el valor total de la venta.
        """
        
        # 1. Validación de campos (Código y Cantidad no vacíos)
        if not self.esUnProductoVálidoParaElCarrito():
            return
        
        código = self.código_venta.get().strip()
        cantidad_deseada_str = self.cantidad_venta.get().strip()
        cantidad_deseada = int(cantidad_deseada_str) 

        # 2. Consultar producto
        try:
            producto_encontrado = self.base_de_datos.buscarProductoPorCódigo(código)
        except Exception as e:
            MensajeModerno(self, "Error de BD", f"Error al buscar el producto por código: {str(e)}", tipo="error")
            return

        # 3. Procesar resultado
        if producto_encontrado:
            # (Índices: 1:nombre, 2:precio_venta)
            nombre = producto_encontrado[1]
            precio_unitario = float(producto_encontrado[2])

            # 4. Verificar si el producto ya está en el carrito
            cantidad_en_carrito = 0
            item_id_en_carrito = None 

            for item_id in self.tabla_carrito.get_children():
                fila = self.tabla_carrito.item(item_id, 'values')
                if fila[0].lower() == código.lower(): # Si el código coincide
                    cantidad_en_carrito = int(fila[3])
                    item_id_en_carrito = item_id
                    break 
            
            # 5. Insertar o Actualizar
            
            # Subtotal de los items NUEVOS que se están agregando ahora
            subtotal_float_nuevo = precio_unitario * cantidad_deseada 
            
            # Calcular la nueva cantidad TOTAL para la fila
            nueva_cantidad_total_item = cantidad_deseada + cantidad_en_carrito
            nuevo_subtotal_item_fila = precio_unitario * nueva_cantidad_total_item
            
            # Preparar valores para la fila
            valores_fila = (
                código, 
                nombre, 
                str(precio_unitario), 
                nueva_cantidad_total_item, 
                f"{nuevo_subtotal_item_fila:.2f}" 
            )

            # Estilos de fila
            numero_filas_actuales = len(self.tabla_carrito.get_children())
            tag_fila = 'par' if numero_filas_actuales % 2 == 0 else 'impar'
            self.tabla_carrito.tag_configure('impar', background=COLOR_BLANCO)
            self.tabla_carrito.tag_configure('par', background=COLOR_FONDO_APP)
            
            if item_id_en_carrito:
                # ACTUALIZAR fila existente
                self.tabla_carrito.item(item_id_en_carrito, values=valores_fila)
            else:
                # INSERTAR nueva fila
                self.tabla_carrito.insert('', tk.END, values=valores_fila, tags=(tag_fila,))

            # 6. Actualizar el Valor total de la venta
            # Usamos la variable con el nombre original de tu __init__
            total_actual_str = self.etiqueta_valor_total_producto.cget('text')
            nuevo_total_float = float(total_actual_str) + subtotal_float_nuevo
            nuevo_total_formateado = f"{nuevo_total_float:.2f}"
            
            self.etiqueta_valor_total_producto.config(text=nuevo_total_formateado)
            
            # 7. Limpiar campos
            self.limpiarCamposVenta() 

        else:
            # Producto no encontrado
            MensajeModerno(self, "No encontrado", "No existe un producto con ese código.", tipo="info")
            self.entrada_código_producto_venta.focus()
    
    def agregarMedioPago(self):
        """
        Orquesta la lógica para agregar o restaurar un medio de pago.
        """
        # 1. Obtener datos
        nombre = self.var_nuevo_medio.get().strip()
        # LEER ESTADO ACTUAL
        valor_raw = self.var_facturar_medio.get()
        facturar = 1 if valor_raw else 0 
        
        print(f"DEBUG: Checkbox value: {valor_raw} -> Enviando a BD: {facturar}")

        # 2. Validaciones básicas de UI
        if not nombre:
            MensajeModerno(self, "Atención", "Debe escribir un nombre para el medio de pago.", tipo="advertencia")
            self.entry_nuevo_medio.focus()
            return

        try:
            # 3. Verificar existencia en BD
            resultado_existencia = self.base_de_datos.verificarEstadoMedioPago(nombre)
            
            if resultado_existencia:
                # Desempaquetar tupla (id, eliminado)
                id_medio, estado_eliminado = resultado_existencia
                
                if estado_eliminado == 0:
                    # CASO A: Existe y está activo -> Error
                    MensajeModerno(self, "Duplicado", f"El medio de pago '{nombre}' ya existe.", tipo="error")
                    self.entry_nuevo_medio.focus()
                    return # Cortamos la ejecución aquí
                
                else:
                    # CASO B: Existe pero estaba eliminado -> Restaurar
                    self.base_de_datos.restaurarMedioPago(id_medio, facturar)
                    mensaje_exito = f"El medio de pago '{nombre}' estaba eliminado y ha sido restaurado."
            
            else:
                # CASO C: No existe -> Insertar nuevo
                self.base_de_datos.ingresarNuevoMedioPago(nombre, facturar)
                mensaje_exito = f"Medio de pago '{nombre}' agregado correctamente."

            # 4. Finalización Exitosa (Común para Caso B y C)
            self.limpiarCamposMedioPago()
            self.actualizarListaMediosEnHilo() # Recargar lista
            MensajeModerno(self, "Éxito", mensaje_exito, tipo="éxito")

        except Exception as e:
            MensajeModerno(self, "Error Crítico", f"Ocurrió un error en la base de datos: {e}", tipo="error")

    def esUnProductoVálidoParaElCarrito(self):
        """
        Verifica si los campos de código de producto y cantidad de venta contienen
        cadenas de texto no vacías.

        Advierte al usuario si alguno de los campos está vacío.

        Returns:
            bool: True si ambos campos tienen una cadena no vacía, False en caso contrario.
        """
        código = self.código_venta.get().strip()
        cantidad = self.cantidad_venta.get().strip()
        
        producto_válido = True

        # 1. Verificar el Código
        if código == '':
            MensajeModerno(self,'Atención', 'Debe ingresar un código de producto.', tipo="advertencia")
            self.entrada_código_producto_venta.focus()
            producto_válido = False

        # 2. Verificar la Cantidad
        # Solo verificamos si el código fue válido para no mostrar dos advertencias a la vez
        if producto_válido and cantidad == '':
            MensajeModerno(self,'Atención', 'Debe ingresar la cantidad a vender.', tipo="advertencia")
            self.entrada_cantidad_venta.focus()
            producto_válido = False
            
        return producto_válido

    def limpiarCamposMedioPago(self):
        """
        Restablece el formulario de medios de pago a su estado inicial.
        """
        # 1. Borrar caja de texto
        self.var_nuevo_medio.set("")
        
        # 2. Destildar "Facturar" (Lógica y Visual)
        self.var_facturar_medio.set(False)
        # Restablecer el icono visualmente a "Caja vacía"
        self.lbl_icono_facturar.config(text="☐", foreground="#555", font=('Segoe UI', 14))
        
        # 3. Deseleccionar la lista
        self.listbox_medios.selection_clear(0, tk.END)
        
        # 4. Poner el foco en el campo de texto
        self.entry_nuevo_medio.focus()

        self.botón_agregar_medio.config(state='normal')

        self.botón_editar_medio.config(state='disabled')

        self.botón_eliminar_medio.config(state='disabled')

    def editarMedioPago(self):
        """
        Modifica el medio de pago seleccionado con los datos del formulario.
        """
        # 1. Obtener selección original (para saber QUÉ estamos editando)
        selección = self.listbox_medios.curselection()
        if not selección:
            MensajeModerno(self, "Atención", "Debe seleccionar un medio de pago de la lista para editarlo.", tipo="advertencia")
            return

        nombre_original = self.listbox_medios.get(selección[0])

        # 2. Obtener nuevos datos del formulario
        nuevo_nombre = self.var_nuevo_medio.get().strip()
        nuevo_facturar = 1 if self.var_facturar_medio.get() else 0

        # 3. Validaciones
        if not nuevo_nombre:
            MensajeModerno(self, "Atención", "El nombre no puede estar vacío.", tipo="advertencia")
            self.entry_nuevo_medio.focus()
            return

        # 4. Guardar cambios
        try:
            self.base_de_datos.modificarMedioPago(nombre_original, nuevo_nombre, nuevo_facturar)
            
            MensajeModerno(self, "Éxito", "Medio de pago actualizado correctamente.", tipo="éxito")
            
            # 5. Refrescar y Limpiar
            self.limpiarCamposMedioPago()
            self.actualizarListaMediosEnHilo()

        except ValueError as ve:
            MensajeModerno(self, "Error", str(ve), tipo="error")
        except Exception as e:
            MensajeModerno(self, "Error Crítico", f"No se pudo editar: {e}", tipo="error")

    def limpiarCamposVenta(self):
        """
        Limpia los campos del formulario 'Venta de producto' y restablece
        la etiqueta de precio a su estado original.
        """
        # 1. Limpia las cajas de texto
        self.código_venta.set("")
        self.cantidad_venta.set("")
        
        # 2. Restablece la etiqueta de precio al texto "Precio:"
        self.precio_venta_var.set(ETIQUETA_PRECIO_VENTA)
        
        # 3. Pone el foco (cursor) de nuevo en la entrada de código
        self.entrada_código_producto_venta.focus()

        # 4. Deseleccionar la fila de la tabla ventas
        self.tabla_carrito.selection_set(())

    def buscarProducto(self):
        código = self.código.get().strip()
        nombre = self.nombre.get().strip()
        descripción = self.texto_desplazado.get("1.0", tk.END).strip()

        # Usamos un 'set' para almacenar resultados únicos
        # (Las tuplas de productos se pueden añadir a un set)
        resultados_únicos = set()

        # 1. Buscar por Código
        if len(código) > 0:
            # Asumimos que .buscarProductoPorCódigo() devuelve una tupla (producto) o None
            producto_por_código = self.base_de_datos.buscarProductoPorCódigo(código)
            if producto_por_código:  # Si no es None
                resultados_únicos.add(producto_por_código)

        # 2. Buscar por Nombre
        if len(nombre) > 0:
            # Asumimos que .buscarProductoPorNombre() devuelve una LISTA de tuplas
            productos_por_nombre = self.base_de_datos.buscarProductoPorNombre(nombre)
            if productos_por_nombre:  # Si la lista no está vacía
                resultados_únicos.update(productos_por_nombre)

        # 3. Buscar por Descripción
        if len(descripción) > 0:
            # Asumimos que .buscarProductoPorDescripción() devuelve una LISTA de tuplas
            productos_por_descripción = self.base_de_datos.buscarProductoPorDescripción(descripción)
            if productos_por_descripción:
                resultados_únicos.update(productos_por_descripción)

        # 4. Comprobar si el set tiene algún resultado
        if resultados_únicos:
            # Limpia los campos antes de cargar los datos
            self.limpiarCamposProductos()

            # Borra todas las filas existentes en la tabla
            funciones_útiles.borrarTodasLasFilas(self.tabla_productos)
            
            # 5. Convertir el set de nuevo a una lista
            lista_resultados = list(resultados_únicos)
            
            # 6. Ordenar la lista por el nombre (posición 1), ignorando mayúsculas
            lista_resultados.sort(key=lambda producto: producto[1].lower())
            
            # 7. Asignar la lista ordenada y cargar la tabla
            self.datos = lista_resultados
            self.cargarTablaProducto() # Llama a la función que SÍ usa self.datos
        else:
            MensajeModerno(self, 'No encontrado', 'No se encontró ningún producto con esos datos.', tipo="info")

    def procesarVentaFinal(self, nombre_medio_pago):
        """
        Guarda la venta y emite factura si corresponde.
        Ejecuta la facturación en un hilo para no congelar la UI.
        """
        
        # 1. Obtener datos (rápido, en hilo principal)
        items_carrito_ids = self.tabla_carrito.get_children()
        total_venta_str = self.etiqueta_valor_total_producto.cget('text')
        total_float = float(total_venta_str)
        fecha_actual = datetime.now()

        # Verificar si se factura
        datos_medio = self.base_de_datos.obtenerDetalleMedioPago(nombre_medio_pago)
        se_factura = bool(datos_medio[0]) if datos_medio else False

        # --- CORRECCIÓN: Inicializar variable para evitar NameError ---
        ventana_espera = None 

        # --- FUNCIÓN INTERNA PARA EL HILO ---
        def tarea_facturacion():
            cae = "-"
            nro_factura = "-"
            error_afip = None

            # A. FACTURACIÓN (Lento)
            if se_factura:
                try:
                    resultado_afip = facturación.emitir_factura_b(total_float)
                    if not resultado_afip['exito']:
                        error_afip = resultado_afip['mensaje']
                    else:
                        cae = resultado_afip['cae']
                        nro_factura = resultado_afip['numero_factura']
                except Exception as e:
                    error_afip = f"Error inesperado al facturar: {e}"
            
            # B. VOLVER AL HILO PRINCIPAL
            self.after(0, lambda: finalizar_proceso(cae, nro_factura, error_afip))

        # --- FUNCIÓN DE FINALIZACIÓN (Hilo Principal) ---
        def finalizar_proceso(cae, nro_factura, error_afip):
            # --- CORRECCIÓN: Cerrar solo si existe ---
            if ventana_espera:
                ventana_espera.cerrar()

            # Si hubo error en AFIP, mostrar y cancelar
            if error_afip:
                MensajeModerno(self, "Error AFIP", error_afip, tipo="error")
                return

            try:
                # 2. Registrar VENTA (Rápido)
                id_venta_generado = self.base_de_datos.registrarVenta([nombre_medio_pago, fecha_actual])
                if id_venta_generado is None:
                    raise Exception("Fallo al registrar venta en BD.")

                # 3. Registrar DETALLES y actualizar VENTAS ACUMULADAS
                for item_id in items_carrito_ids:
                    valores = self.tabla_carrito.item(item_id, 'values')
                    código = valores[0]
                    precio = float(valores[2])
                    cantidad = int(valores[3])

                    self.base_de_datos.ingresarDetalleVenta([id_venta_generado, código, cantidad, precio])
                    self.base_de_datos.actualizarVentasProducto([cantidad, código])
                
                # 4. Limpieza y Refresco
                funciones_útiles.borrarTodasLasFilas(self.tabla_carrito)
                self.etiqueta_valor_total_producto.config(text="0.00")
                self.limpiarCamposVenta()

                self.actualizarTablaVentasEnHilo()
                self.datos = self.base_de_datos.consultarDatosProductos() 
                self.cargarDatosEnTablaEnHilo() 
                funciones_útiles.crearHiloRespaldarBaseDeDatos(self.base_de_datos)

                # 5. Mensaje Éxito
                msg = f"Venta registrada correctamente.\nMedio: {nombre_medio_pago}"
                if se_factura:
                    msg += f"\n\nFactura B N°: {nro_factura}\nCAE: {cae}"
                
                MensajeModerno(self, "Éxito", msg, tipo="éxito")

            except Exception as e:
                MensajeModerno(self, "Error Crítico", f"Error al guardar venta: {str(e)}", tipo="error")

        # --- INICIO DEL PROCESO ---
        if se_factura:
            # Mostrar ventana de espera personalizada
            ventana_espera = VentanaCierre(self, mensaje="Conectando con AFIP...\nPor favor espere, no cierre el programa.")
            
            # Lanzar hilo
            threading.Thread(target=tarea_facturacion, daemon=True).start()
        else:
            # Si no factura, llamar directo a finalizar (sin espera ni hilo)
            finalizar_proceso("-", "-", None)

    def añadirProducto(self):
        """
        Valida los campos de entrada y añade el nuevo producto a la base de datos.
        """
        if self.esUnProductoVálido():  
            # 1. Obtener datos básicos
            código = self.código.get().strip()
            nombre = self.nombre.get().strip()
            descripción = self.texto_desplazado.get("1.0", tk.END).strip()
            precio = float(self.precio.get().strip())
            
            # Obtener código de alternativa para validación
            código_alt = self.alternativa.get().strip()
            
            if código_alt and código == código_alt:
                MensajeModerno(self, "Error de Validación", 
                               "El código de Alternativa no puede ser el mismo que el código del propio producto.", 
                               tipo="error")
                self.entrada_alternativa.focus()
                return
            # -------------------------------------------

            # 2. Manejar campos opcionales (NULL si están vacíos)
            ventas_acum_str = self.ventas_acumuladas.get().strip()
            umbral_str = self.umbral.get().strip()

            ventas_acumuladas = int(ventas_acum_str) if ventas_acum_str else None
            umbral_ventas = int(umbral_str) if umbral_str else None

            # 3. Crear lista de datos (Nota: ingresarProducto actualmente solo acepta 6 campos)
            # Orden: [código, nombre, descripcion, precio, ventas_acum, umbral]
            producto = [
                código,
                nombre,
                descripción,
                precio,
                ventas_acumuladas,
                umbral_ventas
            ]
                
            try:
                self.base_de_datos.ingresarProducto(producto)
                
                # Actualizar UI
                self.limpiarCamposProductos()
                self.datos = self.base_de_datos.consultarDatosProductos()
                self.cargarDatosEnTablaEnHilo()

                funciones_útiles.crearHiloRespaldarBaseDeDatos(self.base_de_datos)
                
                MensajeModerno(self, "Éxito", "Producto añadido correctamente.", tipo="éxito")

            except ValueError as ve:
                MensajeModerno(self, "Error de datos", str(ve), tipo="error")
                self.entrada_código.focus()

            except Exception as e:
                MensajeModerno(self, "Error de Base de Datos", 
                              f"No se pudo añadir el producto: {str(e)}", tipo="error")

    def manejarCambioUmbral(self, event=None):
        """
        Habilita o deshabilita el campo 'Ventas Acumuladas' dependiendo 
        de si hay contenido en 'Umbral de Ventas'.
        """
        contenido_umbral = self.umbral.get().strip()
        
        if contenido_umbral:
            # Si hay texto, habilitamos ventas acumuladas
            self.entrada_ventas_acumuladas.config(state='normal')
        else:
            # Si está vacío, borramos el contenido y deshabilitamos
            self.ventas_acumuladas.set("")
            self.entrada_ventas_acumuladas.config(state='disabled')
            
    def esUnProductoVálido(self):
        producto_válido = True  # Asume inicialmente que los datos son válidos
        
        código = self.código.get().strip()
        nombre = self.nombre.get().strip()
        precio_str = self.precio.get().strip()

        # 1. Verifica que se haya ingresado un código
        if código == '':
            MensajeModerno(self,'¡Atención!', 'Debe ingresar un código para el producto.', tipo="advertencia")
            self.entrada_código.focus()
            producto_válido = False

        # 2. Verifica que se haya ingresado un nombre (solo si lo anterior es válido)
        if nombre == '':
            MensajeModerno(self,'¡Atención!', 'Debe ingresar un nombre para el producto.', tipo="advertencia")
            self.entrada_nombre.focus()
            producto_válido = False

        # 3. Verifica que se haya ingresado un precio (solo si lo anterior es válido)
        if precio_str == '':
            MensajeModerno(self,'¡Atención!', 'Debe ingresar un precio para el producto.', tipo="advertencia")
            self.entrada_precio.focus()
            producto_válido = False

        # Devuelve el resultado final de todas las validaciones
        return producto_válido
    
    def actualizarTablaProductos(self):
        """
        Actualiza la tabla de productos, eliminando las filas existentes y volviendo a cargar los datos.

        Este método borra todas las filas que estén actualmente en la tabla y luego
        vuelve a cargar los datos desde la variable 'self.datos', que se espera que
        haya sido previamente poblada (por ejemplo, mediante 'cargarDatosEnTablaEnHilo').
        Esencialmente, refresca la vista de la tabla con los datos más recientes.

        """
        funciones_útiles.borrarTodasLasFilas(self.tabla_productos)  # Elimina todas las filas existentes de la tabla.
        self.actualizarTablaStockAlerta() # Refresca también la tabla de alertas
        self.cargarTablaProducto()  # Carga los datos en la tabla (desde 'self.datos').

    def crearTablaCarrito(self):
        """
        Crea la tabla (Treeview) para mostrar los productos
        agregados al "carrito" de la venta actual.
        """

        # --- Crear la Etiqueta "Carrito" (Fila 0) ---
        self.etiqueta_título_ventas = ttk.Label(self.página_cuaderno_ventas, 
                                               text="Carrito de ventas", 
                                               font=FUENTE_TÍTULO_PRODUCTOS)
        
        # Posicionar la etiqueta (Fila 0, Col 2)
        self.etiqueta_título_ventas.grid(column=2, row=0, 
                                        padx=5, pady=(2, 2), sticky="w")
        
        # --- 1. Definir Columnas ---
        columnas_carrito = ('código', 'nombre', 'precio_unitario', 'cantidad', 'subtotal')

        self.tabla_carrito = ttk.Treeview(
            self.página_cuaderno_ventas,
            columns=columnas_carrito,
            show='headings',
            height=5  # Altura inicial (se expandirá)
        )

        # --- 2. Definir Encabezados ---
        self.tabla_carrito.heading('código', text='Código', anchor='center')
        self.tabla_carrito.heading('nombre', text='Nombre', anchor='center')
        self.tabla_carrito.heading('precio_unitario', text='Precio unitario', anchor='center')
        self.tabla_carrito.heading('cantidad', text='Cantidad', anchor='center')
        self.tabla_carrito.heading('subtotal', text='Subtotal', anchor='center')

        # Habilitar ordenamiento por clic en columnas
        for col in columnas_carrito:
            self.tabla_carrito.heading(col, command=lambda c=col: self.ordenarColumna(self.tabla_carrito, c, False))

        # --- 3. Posicionar la Tabla (Fila 1, Col 2, Colspan 2) ---
        self.tabla_carrito.grid(
            row=1, # Fila 1
            rowspan=1,
            column=2,
            columnspan=2, # Abarca la columnas 2 y 3
            sticky='nsew' # Se expande en todas las direcciones
        )

        # --- 4. Definir Anchos de Columna ---
        self.tabla_carrito.column("código", anchor='w', width=200, stretch=tk.NO)
        self.tabla_carrito.column("nombre", anchor='w', width=250) # Columna expandible
        self.tabla_carrito.column("precio_unitario", anchor='e', width=110, stretch=tk.NO)
        self.tabla_carrito.column("cantidad", anchor='center', width=90, stretch=tk.NO)
        self.tabla_carrito.column("subtotal", anchor='e', width=110, stretch=tk.NO)
        
        # --- 5. Scrollbars para la tabla de carrito ---
        self.barra_desplazamiento_vertical_carrito = ttk.Scrollbar(
            self.página_cuaderno_ventas,
            orient=tk.VERTICAL,
            command=self.tabla_carrito.yview
        )
        self.barra_desplazamiento_horizontal_carrito = ttk.Scrollbar(
            self.página_cuaderno_ventas,
            orient=tk.HORIZONTAL,
            command=self.tabla_carrito.xview
        )

        self.tabla_carrito.configure(xscrollcommand=self.barra_desplazamiento_horizontal_carrito.set)
        self.tabla_carrito.configure(yscrollcommand=self.barra_desplazamiento_vertical_carrito.set)

        # --- 6. Posicionar scrollbars ---
        self.barra_desplazamiento_vertical_carrito.grid(row=1, rowspan=1, column=4, sticky='ns')
        self.barra_desplazamiento_horizontal_carrito.grid(row=2, column=2, columnspan=2, sticky='we')

    def actualizarTablaStockAlerta(self):
        funciones_útiles.borrarTodasLasFilas(self.tabla_stock_alerta)
        
        # Tags
        self.tabla_stock_alerta.tag_configure('impar', background=COLOR_BLANCO)
        self.tabla_stock_alerta.tag_configure('par', background=COLOR_FONDO_APP)
        # Rojo si ventas >= umbral (Meta cumplida / Alerta)
        self.tabla_stock_alerta.tag_configure('alerta', foreground='red', background='#FFF0F0') 

        datos_alerta = self.base_de_datos.consultarProductosPorAlertaVentas()
        
        if datos_alerta:
            for prod in datos_alerta:
                # prod: [cod, nom]
                
                self.tabla_stock_alerta.insert('', tk.END, values=prod, tags=('alerta',))

    def cargarTablaProducto(self):
        """
        Carga los datos... Si ventas, umbral o alternativa son None, muestra cadena vacía.
        """
        self.tabla_productos.tag_configure('impar', background=COLOR_BLANCO)
        self.tabla_productos.tag_configure('par', background=COLOR_FONDO_APP)

        if self.datos:
            for i, fila_tupla in enumerate(self.datos):
                producto = list(fila_tupla)
                
                # Índices: [0]cod, [1]nom, [2]pre, [3]ventas, [4]umbral, [5]desc, [6]ALT, [7]ID
                
                if producto[3] is None: producto[3] = "" # Ventas
                if producto[4] is None: producto[4] = "" # Umbral
                
                # --- NUEVO: Manejo de Alternativa ---
                if producto[6] is None: producto[6] = "" 
                
                tag_fila = 'par' if i % 2 == 0 else 'impar'
                self.tabla_productos.insert('', tk.END, values=producto, tags=(tag_fila,))
            
            self.aplicarOrdenGuardado(self.tabla_productos, 'productos')

    def eliminarVenta(self):
        """
        Elimina la VENTA seleccionada de la tabla_ventas (historial).
        
        1. Pide confirmación para eliminar la venta.
        2. Si se elimina, pregunta si se desea DESCONTAR las ventas acumuladas.
        3. Si responde SÍ: resta la cantidad a 'ventas_acumuladas'.
        4. Finalmente elimina la venta de la BD y refresca la interfaz.
        """
        
        # 1. Verificar selección
        item_seleccionado = self.tabla_ventas.focus()
        if not item_seleccionado:
            MensajeModerno(self, "Atención", 
                           "Debe seleccionar una Venta de la tabla de la izquierda (Historial) para poder eliminarla.",
                           tipo="advertencia")
            return

        # 2. Pedir confirmación
        confirmacion = MensajeModerno(self, "Confirmar Eliminación", 
                                        "¿Está seguro de que desea eliminar esta VENTA permanentemente?\n"
                                        "Esta acción no se puede deshacer.", tipo="pregunta")
        
        if confirmacion.resultado:
            try:
                # 3. Obtener ID
                datos = self.tabla_ventas.item(item_seleccionado)['values']
                id_venta = datos[0] 
                
                # 4. Consultar detalles
                detalles = self.base_de_datos.consultarDetalleVenta(id_venta)
                
                if detalles:
                    # 5. Preguntar si se desea DESCONTAR DEL ACUMULADO
                    confirmacion_revertir = MensajeModerno(self, "Revertir Acumulado", 
                                                            "¿Desea descontar estas ventas del acumulado de los productos?\n\n"
                                                            "Sí: Se restará la cantidad a 'Ventas Acumuladas'.\n"
                                                            "No: Solo se borrará el registro de la venta.", tipo="pregunta")
                    
                    if confirmacion_revertir.resultado:
                        for item in detalles:
                            código = item[0]
                            cantidad = int(item[3])
                            self.base_de_datos.actualizarVentasProducto([-cantidad, código])

                # 6. Eliminar Venta
                self.base_de_datos.eliminarVentaPorID([id_venta])
                
                # 7. Limpiar UI
                funciones_útiles.borrarTodasLasFilas(self.tabla_carrito)
                self.etiqueta_valor_total_producto.config(text="0.00")
                
                # 8. Refrescar tablas
                self.actualizarTablaVentasEnHilo()
                self.datos = self.base_de_datos.consultarDatosProductos()
                self.cargarDatosEnTablaEnHilo() 
                
                MensajeModerno(self, "Éxito", "Venta eliminada correctamente.", tipo="exito") # Corregido tipo='exito'

                self.botón_eliminar_venta.config(state='disabled')
                self.tabla_ventas.selection_set(())
                
            except Exception as e:
                MensajeModerno(self, "Error", f"No se pudo eliminar la venta: {str(e)}", tipo="error")

    def verPrecioProducto(self):
        """
        Busca el precio de un producto por su código y lo muestra en la
        etiqueta de precio.
        """
        código = self.código_venta.get().strip()

        # 1. Validar que el campo no esté vacío
        if not código:
            MensajeModerno(self,"Campo vacío", "Por favor, ingrese un código de producto.", tipo="advertencia")
            self.entrada_código_producto_venta.focus()
            return

        # 2. Consultar la base de datos
        producto = self.base_de_datos.buscarProductoPorCódigo(código)

        # 3. Procesar el resultado
        if producto:
            # ÉXITO: Producto encontrado
            precio = producto[2]  # Índice 2 es 'precio_venta'
            self.precio_venta_var.set(f"$ {precio:.2f}")
            self.etiqueta_precio_venta.configure(style=ESTILO_PRECIO_ENCONTRADO_VENTA)
        else:
            # FALLO: Producto no encontrado
            MensajeModerno(self, "No encontrado", "No existe un producto con ese código.", tipo="info")
            self.precio_venta_var.set(ETIQUETA_PRECIO_VENTA) # Restablece a "Precio:"
            self.etiqueta_precio_venta.configure(style=ESTILO_PRECIO_ENCONTRADO_VENTA)
            self.entrada_código_producto_venta.focus()

    def cargarDatosEnTablaEnHilo(self):
        def cargar_datos():
            try:
                # Programa la actualización de la tabla en el hilo principal.
                # Usa 'ventana.after(0, ...)' para ejecutar 'actualizarTablaProductos'
                # tan pronto como sea posible en el hilo principal.
                self.after(0, self.actualizarTablaProductos)  # Actualizar la interfaz en el hilo principal
            except Exception as e:
                # Maneja cualquier error que ocurra durante la carga de datos.
                print(f"Error al cargar datos: {e}")  # Imprime un mensaje de error.

        # Crea un hilo secundario para la función 'cargar_datos'.
        # 'daemon=True' asegura que el hilo se cierre cuando la aplicación principal se cierre.
        hilo = threading.Thread(target=cargar_datos, daemon=True)
        # Agrega el hilo a la lista de hilos para mantener una referencia.
        self.hilos.append(hilo)
        # Inicia la ejecución del hilo.
        hilo.start()
    
    def crear_label_frame_medios_pago(self):
        """
        Crea el LabelFrame para gestionar los Medios de Pago en la pestaña 'Ajustes'.
        Incluye una lista de medios existentes, un campo para nuevos, un check para facturar y botones.
        """
        
        # 1. Crear la ETIQUETA del título (estilo moderno)
        self.etiqueta_título_medios = ttk.Label(self.página_cuaderno_ajustes, 
                                                text=TÍTULO_LABELFRAME_MEDIOS_PAGO, 
                                                font=FUENTE_TÍTULO_PRODUCTOS)
        
        # 2. Crear el LabelFrame
        self.labelframe_medios_pago = ttk.LabelFrame(self.página_cuaderno_ajustes, 
                                                     labelwidget=self.etiqueta_título_medios)
        
        # Posicionarlo arriba a la izquierda (Col 0, Fila 0)
        self.labelframe_medios_pago.grid(column=0, row=0, 
                                         padx=10, pady=10, 
                                         sticky="nw")

        # --- Fila 0: Lista de Existentes ---
        self.lbl_medios_existentes = ttk.Label(self.labelframe_medios_pago, 
                                               text=ETIQUETA_EXISTENTES_MEDIOS)
        self.lbl_medios_existentes.grid(column=0, row=0, padx=5, pady=5, sticky="nw")
        
        self.listbox_medios = tk.Listbox(self.labelframe_medios_pago, height=7, width=30, 
                                         font=('Segoe UI', 10), bd=1, relief="solid",
                                         selectmode=tk.MULTIPLE)
        self.listbox_medios.grid(column=1, row=0, padx=(5, 0), pady=5, sticky="ew")

        # Vinculamos al nuevo manejador inteligente
        self.listbox_medios.bind('<<ListboxSelect>>', self.manejarSelecciónMedio)
        
        self.scroll_medios = ttk.Scrollbar(self.labelframe_medios_pago, 
                                           orient="vertical", 
                                           command=self.listbox_medios.yview)
        self.scroll_medios.grid(column=2, row=0, sticky="ns", pady=5)
        self.listbox_medios.config(yscrollcommand=self.scroll_medios.set)

        # --- Fila 1: Nuevo Medio ---
        self.lbl_nuevo_medio = ttk.Label(self.labelframe_medios_pago, 
                                         text=ETIQUETA_NUEVO_MEDIO)
        self.lbl_nuevo_medio.grid(column=0, row=1, padx=5, pady=5, sticky="w")
        
        self.var_nuevo_medio = tk.StringVar()
        self.entry_nuevo_medio = ttk.Entry(self.labelframe_medios_pago, 
                                           textvariable=self.var_nuevo_medio,
                                           width=30)
        self.entry_nuevo_medio.grid(column=1, row=1, columnspan=2, padx=5, pady=5, sticky="ew")

        self.entry_nuevo_medio.bind(EVENTO_TECLA_PRESIONADA, 
            lambda event: self.limitar_longitud_entrada(
                event, 
                self.entry_nuevo_medio, 
                self.var_nuevo_medio, 
                MÁX_CARACTERES_NOMBRE_MEDIO_PAGO, 
                f"El nombre del medio de pago no puede superar los {MÁX_CARACTERES_NOMBRE_MEDIO_PAGO} caracteres."
            )
        )

        # --- Fila 2: Checkbutton "Facturar" (Estilo Moderno) ---
        
        # 1. Etiqueta de texto "Facturar:"
        self.lbl_facturar = ttk.Label(self.labelframe_medios_pago, text="Facturar:")
        self.lbl_facturar.grid(column=0, row=2, padx=5, pady=5, sticky="e")

        # 2. Variable de control
        self.var_facturar_medio = tk.BooleanVar(value=False) # Empezar activado (como en tu imagen)

        # 3. El Widget "Checkbox" (Label interactivo)
        self.lbl_icono_facturar = ttk.Label(self.labelframe_medios_pago, cursor="hand2")
        self.lbl_icono_facturar.grid(column=1, row=2, padx=5, pady=5, sticky="w")
        
        # 4. Configuración inicial (Usando el método de clase CORRECTO)
        self.actualizarIconoFacturar()
        
        # 5. Evento de clic (Usando el método de clase CORRECTO)
        self.lbl_icono_facturar.bind("<Button-1>", self.toggleFacturar)

        # --- Fila 3: Botones (Movidos una fila abajo) ---
        
        self.botón_agregar_medio = ttk.Button(self.labelframe_medios_pago, 
                                            text=BOTÓN_AGREGAR_MEDIO,
                                            command=self.agregarMedioPago)
        self.botón_agregar_medio.grid(column=0, row=3, padx=5, pady=10, sticky="ew")

        # Botón Editar (Fila 4, Columna 0) - DEBAJO DE AGREGAR
        self.botón_editar_medio = ttk.Button(self.labelframe_medios_pago, 
                                            text=BOTÓN_EDITAR_MEDIO,
                                            command=self.editarMedioPago)
        self.botón_editar_medio.grid(column=0, row=4, padx=5, pady=(0, 10), sticky="ew")
        
        self.botón_eliminar_medio = ttk.Button(self.labelframe_medios_pago, 
                                             text=BOTÓN_ELIMINAR_MEDIO,
                                             command=self.eliminarMedioPago)
        self.botón_eliminar_medio.grid(column=1, row=3, columnspan=2, padx=5, pady=10, sticky="ew")

        # Botón Limpiar (Fila 4, Columna 1-2) - DEBAJO DE ELIMINAR
        self.botón_limpiar_medio = ttk.Button(self.labelframe_medios_pago, 
                                            text=BOTÓN_LIMPIAR_MEDIO,
                                            command=self.limpiarCamposMedioPago)
        self.botón_limpiar_medio.grid(column=1, row=4, columnspan=2, padx=5, pady=(0, 10), sticky="ew")
    
    def manejarSelecciónMedio(self, event):
        """
        Cuenta cuántos ítems hay seleccionados y ajusta la interfaz.
        
        - 0 seleccionados: Modo "Agregar nuevo" (Todo limpio y habilitado).
        - 1 seleccionado: Modo "Edición" (Carga datos, habilita Editar/Eliminar).
        - >1 seleccionados: Modo "Eliminación Múltiple" (Bloquea edición, solo permite Eliminar).
        """
        selección = self.listbox_medios.curselection()
        cantidad = len(selección)

        if cantidad == 0:
            # --- NADA SELECCIONADO: Modo Agregar ---
            self.var_nuevo_medio.set("")                # Limpiar texto
            self.var_facturar_medio.set(False)          # Destildar
            self.actualizarIconoFacturar()
            
            # Habilitar controles de carga
            self.entry_nuevo_medio.config(state='normal')
            self.lbl_icono_facturar.bind("<Button-1>", self.toggleFacturar)
            self.lbl_icono_facturar.config(cursor="hand2", foreground="#555") # Color normal
            
            # Botones
            self.botón_agregar_medio.config(state='normal')
            self.botón_editar_medio.config(state='disabled')  # No se puede editar la nada
            self.botón_eliminar_medio.config(state='disabled')# No se puede eliminar la nada
            self.botón_limpiar_medio.config(state='normal')   # Permitimos limpiar

        elif cantidad == 1:
            # --- UN SOLO ÍTEM: Modo Edición ---
            
            # Cargar datos del único seleccionado
            nombre_medio = self.listbox_medios.get(selección[0])
            self.var_nuevo_medio.set(nombre_medio)
            
            # Consultar si factura
            datos = self.base_de_datos.obtenerDetalleMedioPago(nombre_medio)
            if datos:
                self.var_facturar_medio.set(bool(datos[0]))
                self.actualizarIconoFacturar()

            # Habilitar todo
            self.entry_nuevo_medio.config(state='normal')
            self.lbl_icono_facturar.bind("<Button-1>", self.toggleFacturar)
            self.lbl_icono_facturar.config(cursor="hand2")
            
            # Botones
            self.botón_agregar_medio.config(state='disabled') # Bloqueamos agregar para evitar duplicados por error
            self.botón_editar_medio.config(state='normal')
            self.botón_eliminar_medio.config(state='normal')
            self.botón_limpiar_medio.config(state='normal')

        else:
            # --- MÚLTIPLES ÍTEMS: Modo Borrado Masivo ---
            
            # Limpiar visualmente el formulario para no confundir
            self.var_nuevo_medio.set("")
            self.lbl_icono_facturar.config(text="☐", foreground="gray") # Gris indicando deshabilitado

            # Bloquear controles de edición
            self.entry_nuevo_medio.config(state='disabled')
            self.lbl_icono_facturar.unbind("<Button-1>")
            self.lbl_icono_facturar.config(cursor="arrow")
            
            # Botones
            self.botón_agregar_medio.config(state='disabled')
            self.botón_editar_medio.config(state='disabled')
            self.botón_limpiar_medio.config(state='disabled') # Bloqueamos limpiar para obligar a deseleccionar manualmente o borrar
            self.botón_eliminar_medio.config(state='normal')  # Solo permitimos eliminar

    def actualizarTablaVentasEnHilo(self):
        def cargar_datos():
            try:
                # Programa la actualización de la tabla en el hilo principal.
                # Usa 'ventana.after(0, ...)' para ejecutar 'actualizarTablaProductos'
                # tan pronto como sea posible en el hilo principal.
                self.after(0, self.actualizarTablaVentas)  # ActualiactualizarTablaVentaszar la interfaz en el hilo principal
            except Exception as e:
                # Maneja cualquier error que ocurra durante la carga de datos.
                print(f"Error al cargar datos: {e}")  # Imprime un mensaje de error.

        # Crea un hilo secundario para la función 'cargar_datos'.
        # 'daemon=True' asegura que el hilo se cierre cuando la aplicación principal se cierre.
        hilo = threading.Thread(target=cargar_datos, daemon=True)
        # Agrega el hilo a la lista de hilos para mantener una referencia.
        self.hilos.append(hilo)
        # Inicia la ejecución del hilo.
        hilo.start()
    
    def actualizarListaMediosEnHilo(self):
        """
        Inicia un hilo secundario para recargar la lista de Medios de Pago
        sin congelar la interfaz gráfica.
        """
        def cargar_datos():
            try:
                # Programa la actualización de la UI en el hilo principal
                self.after(0, self.actualizarListaMedios) 
            except Exception as e:
                print(f"Error al cargar medios de pago: {e}")

        # Crea y lanza el hilo
        hilo = threading.Thread(target=cargar_datos, daemon=True)
        self.hilos.append(hilo)
        hilo.start()
    
    def actualizarListaMedios(self):
        """
        Consulta la base de datos y rellena la Listbox de Medios de Pago.
        """
        try:
            # 1. Limpiar la lista actual
            self.listbox_medios.delete(0, tk.END)
            
            # 2. Consultar DB
            medios = self.base_de_datos.consultarMediosPago()
            
            # 3. Insertar nuevos datos
            if medios:
                for medio in medios:
                    # medio es una tupla (nombre,), insertamos el primer elemento
                    self.listbox_medios.insert(tk.END, medio[0])
                    
        except Exception as e:
            MensajeModerno(self, "Error", f"No se pudo actualizar la lista de medios: {e}", tipo="error")
    
    def cambiarEstadoControlesMedios(self, estado):
        """
        Habilita o deshabilita los controles del formulario de Medios de Pago.
        estado: 'normal' o 'disabled'
        """
        # 1. Caja de texto
        self.entry_nuevo_medio.config(state=estado)
        
        # 2. Botones (Agregar, Editar, Limpiar)
        self.botón_agregar_medio.config(state=estado)
        self.botón_editar_medio.config(state=estado)
        self.botón_limpiar_medio.config(state=estado)
        
        # 3. Checkbox (Simulado con Label)
        if estado == 'disabled':
            # Desvincular evento y poner en gris
            self.lbl_icono_facturar.unbind("<Button-1>")
            self.lbl_icono_facturar.config(cursor="arrow", foreground="gray")
        else:
            # Restaurar evento y color correcto
            self.lbl_icono_facturar.bind("<Button-1>", self.toggleFacturar)
            self.lbl_icono_facturar.config(cursor="hand2")
            self.actualizarIconoFacturar() # Restaura el color verde/rojo según el valor

    def finalizarVentaEnHilo(self):
        def cargar_datos_ventas():
            try:
                # Programa la actualización de la tabla en el hilo principal.
                # Usa 'ventana.after(0, ...)' para ejecutar 'actualizarTablaProductos'
                # tan pronto como sea posible en el hilo principal.
                self.after(0, self.finalizarVenta)  # Actualizar la interfaz en el hilo principal
            except Exception as e:
                # Maneja cualquier error que ocurra durante la carga de datos.
                print(f"Error al cargar datos: {e}")  # Imprime un mensaje de error.

        # Crea un hilo secundario para la función 'cargar_datos'.
        # 'daemon=True' asegura que el hilo se cierre cuando la aplicación principal se cierre.
        hilo = threading.Thread(target=cargar_datos_ventas, daemon=True)
        # Agrega el hilo a la lista de hilos para mantener una referencia.
        self.hilos.append(hilo)
        # Inicia la ejecución del hilo.
        hilo.start()
    
    def cargarRegistros(self, event=None):
        """
        Carga los datos de un producto seleccionado en la tabla (tabla_productos)
        y los muestra en los widgets del 'labelframe_productos'.
        """
        
        # 1. Verifica si hay algún elemento seleccionado en la tabla de productos.
        if len(self.tabla_productos.selection()) > 0:
            
            # Obtiene el identificador del elemento seleccionado.
            item_seleccionado = self.tabla_productos.focus()
            
            if item_seleccionado:
                # 2. Obtiene los valores de la fila seleccionada.
                datos = self.tabla_productos.item(item_seleccionado)['values']

                # 3. Limpia la descripción antes de cargar nuevos datos.
                self.texto_desplazado.delete('1.0', tk.END)

                # 4. Carga los datos en los widgets de la interfaz:
                self.código.set(datos[0])
                self.nombre.set(datos[1])
                self.precio.set(datos[2])
                self.umbral.set(datos[4])
                self.ventas_acumuladas.set(datos[3])
                self.texto_desplazado.insert('1.0', datos[5])
                self.alternativa.set(datos[6])
                self.manejarCambioUmbral()

                # Lista de todos los widgets Entry que acabamos de llenar
                entradas = [self.entrada_código, self.entrada_nombre, self.entrada_precio, 
                            self.entrada_umbral, self.entrada_ventas_acumuladas]
                
                for entrada in entradas:
                    entrada.selection_clear()   # Quita cualquier selección de texto
                    entrada.icursor(tk.END)     # Mueve el cursor al final del texto

                # Para el ScrolledText (Descripción)
                self.texto_desplazado.tag_remove("sel", "1.0", "end") # Quita selección
                self.texto_desplazado.mark_set("insert", "end")       # Mueve cursor al final
                # -----------------------------------------------------------

                # 6. Calcula y muestra los caracteres restantes para la descripción.
                descripción_actual = datos[5]
                caracteres_restantes = MÁX_CAR_DESCRIP - len(descripción_actual)
                self.etiqueta_contador_caracteres.config(text=str(caracteres_restantes))

                # 7. Cambia el color del contador de caracteres
                if caracteres_restantes <= ADVERTENCIA_CANT_CAR_DESCRIP:
                    self.etiqueta_contador_caracteres.configure(style="rojo.TLabel") # Rojo
                else:
                    self.etiqueta_contador_caracteres.configure(style="verde.TLabel") # Verde

    def editarProducto(self):
        """
        Intenta editar el producto seleccionado en la base de datos.
        """
        valores = []
        item_seleccionado = self.tabla_productos.focus()
        
        if item_seleccionado and self.esUnProductoVálido():
            datos_originales = self.tabla_productos.item(item_seleccionado)['values']
            
            # Recopilar datos del formulario
            código = self.código.get().strip()
            valores.append(código)                           # 0: Código
            valores.append(self.nombre.get().strip())        # 1: Nombre
            valores.append(self.texto_desplazado.get("1.0", tk.END).strip()) # 2: Descripción
            valores.append(float(self.precio.get().strip()) if self.precio.get().strip() else 0) # 3: Precio
            
            # Manejo de vacíos para enteros
            ventas = self.ventas_acumuladas.get().strip()
            valores.append(int(ventas) if ventas else None)  # 4: Ventas Acum.
            
            umbral = self.umbral.get().strip()
            valores.append(int(umbral) if umbral else None)  # 5: Umbral
            
            # NUEVO: Campo Alternativa
            alternativa = self.alternativa.get().strip()
            
            if alternativa and código == alternativa:
                MensajeModerno(self, "Error de validación", 
                               "El código del producto alternativo no puede ser el mismo que el código del propio producto.", 
                               tipo="error")
                self.entrada_alternativa.focus()
                return

            valores.append(alternativa if alternativa else None) # 6: Cod. Alternativa
            
            # ID Original
            valores.append(datos_originales[-1])                # 7: ID Producto (WHERE)
            
            try:
                self.base_de_datos.modificarUnProducto(valores)
                
                self.limpiarCamposProductos()
                self.datos = self.base_de_datos.consultarDatosProductos()
                self.cargarDatosEnTablaEnHilo()
                funciones_útiles.crearHiloRespaldarBaseDeDatos(self.base_de_datos)
                
                MensajeModerno(self, "Éxito", "Producto modificado correctamente.", tipo="éxito")

            except ValueError as ve:
                MensajeModerno(self, "Error de Validación", str(ve), tipo="error")
                self.entrada_código.focus()
            except Exception as e:
                MensajeModerno(self, "Error de Base de Datos", f"No se pudo modificar: {str(e)}", tipo="error")
        
        elif not item_seleccionado:
            MensajeModerno(self, "Atención", "Debe seleccionar un producto de la lista para editarlo.", tipo="advertencia")
    
    def crearLabelFrameAdministrarVentas(self):
        """
        Crea el LabelFrame para la gestión de ventas (eliminación, reportes, etc.)
        y ubica los botones de acción.
        """
        
        # 1. Crear la ETIQUETA del título
        self.etiqueta_título_administrar = ttk.Label(self.página_cuaderno_ventas, 
                                                text="Administrar ventas", 
                                                font=FUENTE_TÍTULO_PRODUCTOS)
        
        # 2. Crear el LabelFrame y pasar la etiqueta
        self.labelframe_administrar_ventas = ttk.LabelFrame(self.página_cuaderno_ventas, 
                                                            labelwidget=self.etiqueta_título_administrar)
        
        # 3. Posicionar el LabelFrame (Col 0, Fila 5 - Alineado con la tabla de Ventas)
        self.labelframe_administrar_ventas.grid(column=0, row=5,
                                                padx=PADX_GENERAL_VENTA, 
                                                pady=PADY_GENERAL_VENTA,
                                                sticky="wn") # Se pega arriba a la izquierda
        
        # 4. Botón "Eliminar venta" (Fila 0, Columna 0)
        self.botón_eliminar_venta = ttk.Button(self.labelframe_administrar_ventas, 
                                               text=BOTÓN_ELIMINAR_VENTA_VENTA,
                                               command=self.eliminarVenta,
                                               state='disabled')
        
        self.botón_eliminar_venta.grid(column=0, row=0, 
                                      padx=PADX_GENERAL_VENTA, 
                                      pady=PADY_GENERAL_VENTA, 
                                      sticky="w")

        # 5. Botón "Reporte Productos" (NUEVO - Fila 1, Columna 0 - DEBAJO de Eliminar Venta)
        self.botón_reporte_productos = ttk.Button(self.labelframe_administrar_ventas, 
                                      text="Reporte Productos",
                                      command=self.generarReporteProductos)
        
        self.botón_reporte_productos.grid(column=0, row=1, 
                              padx=PADX_GENERAL_VENTA, 
                              pady=PADY_GENERAL_VENTA, 
                              sticky="w")

        # 6. Botón "Reporte Ventas" (Fila 0, Columna 1 - A la DERECHA de Eliminar Venta)
        self.botón_excel = ttk.Button(self.labelframe_administrar_ventas, 
                                      text="Reporte Ventas",
                                      command=self.generarReporteExcel)
        
        self.botón_excel.grid(column=1, row=0, 
                              padx=PADX_GENERAL_VENTA, 
                              pady=PADY_GENERAL_VENTA, 
                              sticky="w")

    def generarReporteProductos(self):
        """
        Genera un Excel con el ranking de productos por recaudación.
        Se ejecuta en un Hilo para mostrar ventana de espera.
        """
        from openpyxl.styles import Border, Side
        
        # 1. Primero pedimos la ruta (En el hilo principal)
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivos de Excel", "*.xlsx")],
            initialfile=f"Ranking_Productos_{fecha_hoy}.xlsx",
            title="Guardar Reporte de Productos"
        )

        if not ruta_archivo: 
            return

        # 2. Creamos la ventana de carga
        ventana_carga = VentanaCierre(self, mensaje="Generando reporte de productos...\nEsta operación puede tardar unos momentos.")

        # 3. Definimos la tarea pesada
        def tarea_generar():
            exito = False
            mensaje = ""
            tipo_msg = "info"

            try:
                # Consultar BD
                datos = self.base_de_datos.consultarReporteProductos()
                
                if not datos:
                    mensaje = "No hay productos activos o ventas registradas."
                    tipo_msg = "info"
                else:
                    # Crear DataFrame
                    df = pd.DataFrame(datos, columns=["Producto", "Unidades Vendidas", "Recaudación Total ($)"])

                    # Exportar y Formatear
                    with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name='Ranking')
                        ws = writer.sheets['Ranking']
                        
                        negro_grueso = Side(border_style="thick", color="000000")
                        negro_fino = Side(border_style="thin", color="000000")
                        
                        max_row = ws.max_row
                        max_col = ws.max_column
                        
                        for r in range(1, max_row + 1):
                            for c in range(1, max_col + 1):
                                celda = ws.cell(row=r, column=c)
                                
                                b_left = negro_grueso
                                b_right = negro_grueso
                                b_top = negro_fino
                                b_bottom = negro_fino
                                
                                if r == 1: 
                                    b_top = negro_grueso
                                    b_bottom = negro_grueso
                                
                                if r == max_row:
                                    b_bottom = negro_grueso
                                    
                                celda.border = Border(left=b_left, right=b_right, top=b_top, bottom=b_bottom)
                        
                        # Autoajuste
                        for column in ws.columns:
                            max_length = 0
                            column_letter = column[0].column_letter
                            for cell in column:
                                try:
                                    if len(str(cell.value)) > max_length:
                                        max_length = len(str(cell.value))
                                except: pass
                            ws.column_dimensions[column_letter].width = (max_length + 2)

                    exito = True
                    mensaje = f"Reporte generado correctamente en:\n{ruta_archivo}"
                    tipo_msg = "éxito"

            except Exception as e:
                mensaje = f"Error al generar reporte: {e}"
                tipo_msg = "error"

            # 4. Volver al hilo principal para mostrar resultado
            self.after(0, lambda: finalizar_proceso(exito, mensaje, tipo_msg))

        def finalizar_proceso(resultado_exito, texto_msg, tipo):
            ventana_carga.cerrar() # Cerrar ventana de espera
            if texto_msg:
                MensajeModerno(self, "Resultado", texto_msg, tipo=tipo)

        # 5. Iniciar el Hilo
        threading.Thread(target=tarea_generar, daemon=True).start()
    
    def generarReporteExcel(self):
        """
        Consulta los datos, los formatea y exporta a Excel.
        Se ejecuta en un Hilo para mostrar ventana de espera.
        """
        from openpyxl.styles import Border, Side
        
        # 1. Pedir ruta primero
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivos de Excel", "*.xlsx")],
            initialfile=f"Reporte_Ventas_{fecha_hoy}.xlsx",
            title="Guardar Reporte de Ventas"
        )

        if not ruta_archivo:
            return 

        # 2. Ventana de carga
        ventana_carga = VentanaCierre(self, mensaje="Procesando ventas y generando Excel...\nPor favor, espere.")

        # 3. Tarea en segundo plano
        def tarea_generar():
            msg_texto = ""
            msg_tipo = "info"
            
            try:
                # Obtener datos de BD
                datos_raw = self.base_de_datos.consultarDatosParaExcel()
                
                if not datos_raw:
                    msg_texto = "No hay ventas registradas para exportar."
                    self.after(0, lambda: finalizar(msg_texto, "info"))
                    return

                # Procesar datos
                filas_procesadas = []
                ultimo_id_venta = None
                filas_inicio_venta = [] 

                for i, fila in enumerate(datos_raw):
                    id_venta, fecha_obj, total_venta, producto, precio_u, cantidad, subtotal = fila
                    fecha_str = fecha_obj.strftime("%d/%m/%Y %H:%M")
                    
                    fila_excel_actual = i + 2 

                    if id_venta != ultimo_id_venta:
                        nueva_fila = {
                            "ID Venta": id_venta,
                            "Fecha y Hora": fecha_str,
                            "Total Venta": float(total_venta),
                            "Producto": producto,
                            "Precio Unit.": float(precio_u),
                            "Cantidad": int(cantidad),
                            "Subtotal": float(subtotal)
                        }
                        ultimo_id_venta = id_venta
                        filas_inicio_venta.append(fila_excel_actual)
                    else:
                        nueva_fila = {
                            "ID Venta": "", "Fecha y Hora": "", "Total Venta": "",
                            "Producto": producto,
                            "Precio Unit.": float(precio_u),
                            "Cantidad": int(cantidad),
                            "Subtotal": float(subtotal)
                        }
                    
                    filas_procesadas.append(nueva_fila)

                # Crear DataFrame y Guardar
                df = pd.DataFrame(filas_procesadas)

                with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Ventas')
                    worksheet = writer.sheets['Ventas']

                    negro_grueso = Side(border_style="thick", color="000000")
                    negro_fino = Side(border_style="thin", color="000000")
                    
                    set_inicio_ventas = set(filas_inicio_venta)
                    max_row = worksheet.max_row
                    max_col = worksheet.max_column

                    for r in range(1, max_row + 1):
                        for c in range(1, max_col + 1):
                            celda = worksheet.cell(row=r, column=c)
                            
                            # Estilos de tu última modificación
                            b_left = negro_grueso
                            b_right = negro_grueso
                            b_top = negro_fino
                            b_bottom = negro_fino
                            
                            if r == 1:
                                b_top = negro_grueso
                                b_bottom = negro_grueso
                            else:
                                if r in set_inicio_ventas:
                                    b_top = negro_grueso
                                if r == max_row:
                                    b_bottom = negro_grueso
                                elif (r + 1) in set_inicio_ventas:
                                    b_bottom = negro_grueso
                            
                            celda.border = Border(left=b_left, right=b_right, top=b_top, bottom=b_bottom)

                    for column in worksheet.columns:
                        max_length = 0
                        column_letter = column[0].column_letter 
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except: pass
                        worksheet.column_dimensions[column_letter].width = (max_length + 2)

                msg_texto = f"Reporte generado correctamente en:\n{ruta_archivo}"
                msg_tipo = "éxito"

            except Exception as e:
                msg_texto = f"No se pudo generar el Excel: {str(e)}"
                msg_tipo = "error"
            
            # Llamar a finalizar en el hilo principal
            self.after(0, lambda: finalizar(msg_texto, msg_tipo))

        def finalizar(texto, tipo):
            ventana_carga.cerrar()
            if texto:
                MensajeModerno(self, "Resultado", texto, tipo=tipo)

        # 4. Arrancar hilo
        threading.Thread(target=tarea_generar, daemon=True).start()

    def eliminarProducto(self):
        """
        Elimina el producto seleccionado de la base de datos y actualiza la interfaz.

        Esta función se ejecuta cuando el usuario hace clic en el botón "Eliminar".
        Realiza las siguientes acciones:

        1. Obtiene el ítem seleccionado de la 'tabla_productos'.
        2. Pide confirmación al usuario antes de borrar.
        3. Si se confirma:
           - Extrae el 'id_producto' (que es el último valor en la lista 'values').
           - Llama a la función 'eliminarProductoPorID' de la base de datos.
           - Limpia los campos del formulario de productos.
           - Inicia un hilo para respaldar la base de datos.
           - Recarga los datos en la 'tabla_productos'.
        """
        
        item_seleccionado = self.tabla_productos.focus()  # Obtiene el ítem seleccionado de la tabla.

        if item_seleccionado:  # Verifica si hay un ítem seleccionado.
            
            # Pedir confirmación al usuario es una buena práctica antes de eliminar
            confirmación = MensajeModerno(self, "Confirmar Eliminación", 
                                            "¿Está seguro de que desea eliminar este producto permanentemente?", tipo="pregunta")
            respuesta = confirmación.resultado
            
            if respuesta: # Si el usuario hizo clic en "Sí"
                try:
                    # Obtiene los valores del item seleccionado
                    datos = self.tabla_productos.item(item_seleccionado)['values'] 
                    
                    # El id_producto es el último elemento en la lista 'values'
                    # (según cómo se carga en 'cargarTablaProducto' y se usa en 'editarProducto')
                    id_del_producto = datos[-1]
                    
                    # Llama a la función de la base de datos para eliminar el producto.
                    self.base_de_datos.eliminarProductoPorID([id_del_producto])

                    self.datos = self.base_de_datos.consultarDatosProductos()  # Actualiza los datos locales.
                    
                    # Limpia los campos del formulario de productos.
                    self.limpiarCamposProductos()  
                    
                    # Respalda la base de datos (en un hilo).
                    funciones_útiles.crearHiloRespaldarBaseDeDatos(self.base_de_datos)  
                    
                    # Recarga los datos en la tabla (en un hilo).
                    self.cargarDatosEnTablaEnHilo()  
                    
                    MensajeModerno(self, "Éxito", "Producto eliminado correctamente.", tipo="éxito")
                
                except ValueError as ve:
                    MensajeModerno(self, "No se puede eliminar", str(ve), tipo="error")
                
                except Exception as e:
                    MensajeModerno(self, "Error al Eliminar", 
                                         f"No se pudo eliminar el producto: {str(e)}", tipo="error")
        else:
            MensajeModerno(self,"Error", "Debe seleccionar un producto", tipo="advertencia")
    
    def eliminarMedioPago(self):
        """
        Elimina (lógicamente) los medios de pago seleccionados en la lista.
        """
        # 1. Obtener índices seleccionados
        indices = self.listbox_medios.curselection()
        
        # 2. Validar si hay selección
        if not indices:
            MensajeModerno(self, "Atención", "Debe seleccionar al menos un medio de pago para eliminar.", tipo="advertencia")
            return

        # 3. Confirmar acción
        confirmacion = MensajeModerno(self, "Confirmar Eliminación", 
                                      "¿Está seguro de eliminar los medios seleccionados?", tipo="pregunta")
        if not confirmacion.resultado:
            return

        try:
            # 4. Iterar y eliminar
            errores = []
            eliminados_count = 0
            
            # Recorremos en reverso para evitar problemas si borráramos de la lista visual uno a uno,
            # aunque aquí solo leemos el nombre.
            for index in indices:
                nombre_medio = self.listbox_medios.get(index)
                try:
                    self.base_de_datos.eliminarMedioPagoLogico(nombre_medio)
                    eliminados_count += 1
                except Exception as e:
                    errores.append(f"{nombre_medio}: {str(e)}")

            # 5. Actualizar UI
            self.actualizarListaMediosEnHilo()
            self.limpiarCamposMedioPago() # Limpia selección y campos

            # 6. Reportar resultado
            if not errores:
                MensajeModerno(self, "Éxito", f"Se eliminaron {eliminados_count} medios de pago correctamente.", tipo="éxito")
            else:
                msg_error = "Hubo problemas con algunos medios:\n" + "\n".join(errores)
                MensajeModerno(self, "Advertencia", msg_error, tipo="advertencia")

        except Exception as e:
            MensajeModerno(self, "Error Crítico", f"Error al procesar la eliminación: {e}", tipo="error")

    def limpiarCamposProductos(self):
        self.texto_desplazado.delete('1.0', tk.END)  # Borra el texto de la descripción.
        self.precio.set('')  # Limpia el campo de importe.
        self.entrada_umbral.delete(0, "end")
        self.entrada_ventas_acumuladas.delete(0, "end")
        self.entrada_código.delete(0, "end")
        self.entrada_nombre.delete(0, "end")
        self.tabla_productos.selection_set(()) # Deselecciona la tabla
        self.etiqueta_contador_caracteres.config(text=str(MÁX_CAR_DESCRIP)) # actualiza la cantidad de caracteres restantes
        # cambia a verde el color de la etiqueta de los caracteres restantes
        self.etiqueta_contador_caracteres.configure(style="verde.TLabel")
        self.entrada_ventas_acumuladas.config(state='disabled')

    def actualizar_contador(self, longitud_antes):
        """
        Actualiza el contador de caracteres de la descripción y aplica las restricciones correspondientes.

        Esta función se llama después de que se ha modificado el contenido del cuadro de texto de la descripción
        (ya sea por inserción o eliminación de texto). Calcula la diferencia en la longitud del texto,
        actualiza el contador y aplica las siguientes reglas:

        1. Límite máximo: Si el número de caracteres supera 'MÁX_CAR_DESCRIP', se trunca a 'MÁX_CAR_DESCRIP'.
        2. Límite mínimo de caracteres disponibles: Si el número de caracteres disponibles es menor que 0, se establece en 0.
            Si se excede el límite, se elimina cualquier texto que se haya pegado y exceda el límite.
        3.  Color del contador:
            *   Si el número de caracteres es menor que 'ADVERTENCIA_CANT_CAR_DESCRIP', el contador se muestra en rojo.
                Además, si llega a cero caracteres, muestra un mensaje de advertencia.
            *   Si el número de caracteres es mayor o igual que 'ADVERTENCIA_CANT_CAR_DESCRIP', el contador se muestra en verde.

        Args:
            longitud_antes (int): La longitud del texto en el cuadro de descripción *antes* de la modificación.

        """
        contenido_después = self.texto_desplazado.get("1.0", tk.END)  # Obtiene el texto actual del cuadro.
        longitud_después = len(contenido_después) - 1  # Calcula la longitud actual (restando el salto de línea final).
        caracteres_borrados_o_agregados = longitud_antes - longitud_después  # Calcula la diferencia de longitud.

        if caracteres_borrados_o_agregados != 0:  # Si hubo cambios en la longitud.
            cant_caracteres = int(self.etiqueta_contador_caracteres.cget("text"))  # Obtiene el valor actual del contador.
            nuevo_valor = cant_caracteres + caracteres_borrados_o_agregados  # Calcula el nuevo valor del contador.

            if nuevo_valor > MÁX_CAR_DESCRIP:  # Si se supera el límite máximo.
                nuevo_valor = MÁX_CAR_DESCRIP  # Trunca al máximo.
            if nuevo_valor < 0:  # Si el valor es negativo.
                nuevo_valor = 0  # Establece en 0.
                self.texto_desplazado.delete("1.0", tk.END)  # Borra todo el contenido.
                self.texto_desplazado.insert("1.0", contenido_después[:MÁX_CAR_DESCRIP])  # Inserta el contenido truncado.

            self.etiqueta_contador_caracteres.config(text=str(nuevo_valor))  # Actualiza el contador en la interfaz.

            # Actualizar color
            if nuevo_valor <= ADVERTENCIA_CANT_CAR_DESCRIP:  # Si está por debajo del umbral de advertencia.
                self.etiqueta_contador_caracteres.configure(style="rojo.TLabel")  # Cambia el color a rojo.
                if nuevo_valor <= 0:  # Si llega a 0.
                    MensajeModerno(self,"Advertencia", "Ha alcanzado el límite de caracteres.", tipo="advertencia")  # Muestra advertencia.
            else:  # Si está por encima o igual al umbral de advertencia.
                self.etiqueta_contador_caracteres.configure(style="verde.TLabel")  # Cambia el color a verde.
    
    def limitar_longitud_entrada(self, event, entry_widget, string_var, máx_caracteres, mensaje_error):
        """
        Limita la longitud del texto en un Entry. 
        Muestra una advertencia si se intenta escribir más allá del límite.
        Maneja escritura normal y pegado (Ctrl+V).

        Args:
            event: El evento de teclado.
            entry_widget: El widget Entry.
            string_var: La variable StringVar asociada.
            máx_caracteres: Entero con el límite máximo.
            mensaje_error: Texto a mostrar en la advertencia.
        """
         # Obtener el carácter real y la tecla presionada
        carácter = event.char
        tecla = event.keysym
        
        # 1. Identificar teclas de control (Navegación, Borrado, etc.)
        # Estas siempre se permiten y no disparan alertas.
        teclas_control = ('BackSpace', 'Delete', 'Left', 'Right', 'Home', 'End', 'Tab', 'Return', 'Escape')
        es_control = tecla in teclas_control
        
        # 2. Identificar atajos (Ctrl+C, Ctrl+A, etc.) excepto Pegar
        es_atajo = (event.state & 0x0004) and (tecla.lower() in ['c', 'x', 'a'])

        # 3. Verificar si hay texto seleccionado (si escribo encima, no sumo caracteres)
        hay_selección = entry_widget.select_present()

        # CASO A: Permitir teclas de control y atajos
        if es_control or es_atajo:
            return None

        # CASO B: Manejo de Pegado (Ctrl+V)
        if (event.state & 0x0004) and tecla.lower() == 'v':
            
            def validar_pegado():
                contenido = string_var.get()
                if len(contenido) > máx_caracteres:
                    # Opción: Truncar el texto al máximo permitido
                    string_var.set(contenido[:máx_caracteres])
                    MensajeModerno(self, "Límite excedido", mensaje_error, tipo="advertencia")
            
            entry_widget.after_idle(validar_pegado)
            return None

        # CASO C: Intento de escribir un carácter imprimible
        if carácter and carácter.isprintable():
            largo_actual = len(string_var.get())
            
            # Si ya llegamos al límite Y NO estamos sobrescribiendo una selección
            if largo_actual >= máx_caracteres and not hay_selección:
                MensajeModerno(self, "Límite alcanzado", mensaje_error, tipo="advertencia")
                return "break" # Bloquear la escritura
            
            return None # Permitir escribir

        return None

    def limitar_caracteres_descripción(self, event = None):
        """
        Limita la cantidad de caracteres que se pueden ingresar en el cuadro de texto de la descripción.

        Esta función se vincula al evento 'KeyPress' del cuadro de texto de la descripción ('self.texto_desplazado').
        Controla qué teclas se pueden presionar y cómo se procesan, para asegurar que no se exceda el límite
        de caracteres y para actualizar el contador de caracteres en tiempo real.

        Args:
            event (tkinter.Event, optional): El objeto de evento de Tkinter que contiene información sobre la tecla presionada.
                Defaults to None.

        Returns:
            str or None:  Retorna "break" para evitar que el evento se propague más (en algunos casos), o None para
            permitir el procesamiento normal del evento.

        """
        retornar = "break"  # Valor predeterminado para evitar la propagación del evento.
        tecla = event.char  # Obtiene el carácter real generado por la tecla presionada
        #  Verifica si es un carácter imprimible
        es_carácter_válido = len(tecla) == 1 and tecla.isprintable()
        tecla_símbolo = event.keysym  # Obtiene la tecla presionada
        #  Verifica si la tecla es BackSpace, Ctrl+X, Ctrl+V, o un carácter ASCII válido.
        if event and event.keysym == 'BackSpace' or (event.state & 0x0004) and (tecla_símbolo.lower() == 'x' or tecla_símbolo.lower() == 'v') or es_carácter_válido and ord(tecla) >= 32 and ord(tecla) <= 254 or tecla_símbolo in ('Delete'):
            # Guardar contenido antes del borrado o pegado.
            contenido_antes = self.texto_desplazado.get("1.0", tk.END)  # Obtiene el contenido actual.
            longitud_antes = len(contenido_antes) - 1  # Calcula la longitud (sin el salto de línea final).

            # Permitir que el evento Backspace, Ctrl+X o Ctrl+V se procese.
            retornar = None

            # Ejecutar después de que el evento se procese (usando after_idle para asegurar que el texto se haya actualizado).
            self.texto_desplazado.after_idle(functools.partial(self.actualizar_contador, longitud_antes))
        elif (event.state & 0x0004) and len(tecla_símbolo) == 1 and tecla_símbolo.isalpha():
            # Si se presiona Ctrl + una letra (excepto Ctrl+X o Ctrl+V, que ya se manejan antes),
            # se permite el evento para no bloquear atajos de teclado comunes.
            # Además, se habilita el botón de añadir a favoritos para indicar que puede usarse.
            retornar = None
        elif tecla_símbolo in ('Left', 'Right') and self.texto_desplazado.tag_ranges("sel") and not (event.state & 0x0001):
            # Si se presionan las teclas de flecha izquierda o derecha,
            # y hay texto seleccionado (tag "sel" activo),
            # y no se está presionando Shift (para evitar interferir con selección múltiple),
            # se mueve el cursor al inicio o al final de la selección según la flecha,
            # y se elimina la selección para que solo quede el cursor en esa posición.
            if tecla_símbolo == 'Left':
                self.texto_desplazado.mark_set("insert", "sel.first")
            else:
                self.texto_desplazado.mark_set("insert", "sel.last")
            self.texto_desplazado.tag_remove("sel", "1.0", "end")
        elif tecla_símbolo != 'Return':
            # Para cualquier otra tecla diferente de Enter, no hacer nada.
            retornar = None
        return retornar
    
    def controlar_caracteres_solo_enteros(self, event, entry_widget, string_var, max_valor=None):
        """
        Valida que solo se ingresen números enteros y que no superen un valor máximo.
        """
        # Importación local para evitar referencia circular si está en otro archivo
        from MensajeModerno import MensajeModerno 

        retornar = "break"
        carácter = event.char
        tecla = event.keysym.lower()

        # Permitir teclas de control siempre
        es_tecla_control = (event.keysym in ('BackSpace', 'Delete', 'Left', 'Right', 'Home', 'End', 'Tab'))
        es_copiar_pegar = (event.state & 0x0004 and tecla in ['x', 'v', 'c'])

        if es_tecla_control or es_copiar_pegar:
            
            # Lógica de PEGADO (Ctrl+V)
            if tecla == 'v': 
                contenido_antes = string_var.get()
                pos_antes = entry_widget.index("insert")
                retornar = None 

                def validar_pegado():
                    contenido = string_var.get()
                    # 1. Validar si es entero
                    if not validación_tipo_de_datos.esEntero(contenido):
                        string_var.set(contenido_antes)
                        entry_widget.icursor(pos_antes)
                    # 2. Validar si supera el máximo (solo si es un número válido y hay límite)
                    elif max_valor is not None:
                        try:
                            if int(contenido) > max_valor:
                                string_var.set(contenido_antes)
                                entry_widget.icursor(pos_antes)
                                MensajeModerno(self, "Valor excedido", 
                                               f"El valor para este campo no puede ser mayor a {max_valor}.", tipo="advertencia")
                        except ValueError:
                            pass # No debería pasar si esEntero es True

                entry_widget.after_idle(validar_pegado)
            else:
                return None # Permitir otras teclas de control

        # Lógica de ESCRITURA (Dígitos)
        elif carácter and carácter.isdigit():
            # Simulamos el nuevo texto antes de permitirlo
            texto_actual = string_var.get()
            pos_cursor = entry_widget.index("insert")
            
            # Construir el nuevo número hipotético
            if entry_widget.select_present(): # Si hay texto seleccionado que se va a reemplazar
                try:
                    sel_start = entry_widget.index("sel.first")
                    sel_end = entry_widget.index("sel.last")
                    nuevo_texto = texto_actual[:sel_start] + carácter + texto_actual[sel_end:]
                except tk.TclError:
                    nuevo_texto = texto_actual[:pos_cursor] + carácter + texto_actual[pos_cursor:]
            else:
                nuevo_texto = texto_actual[:pos_cursor] + carácter + texto_actual[pos_cursor:]

            # Validar el máximo
            if max_valor is not None:
                try:
                    if int(nuevo_texto) > max_valor:
                        MensajeModerno(self, "Valor excedido", 
                                       f"El valor para este campo no puede ser mayor a {max_valor}.", tipo="advertencia")
                        return "break" # Bloquear escritura
                except ValueError:
                    pass 

            return None # Permitir escritura

        return retornar
    
    def cerrarVentana(self):
        ventana_cierre = VentanaCierre(self)  # Crea la ventana, usando self como padre

        self.evento_cancelar.set()  # Indica a los hilos que se detengan

        def esperar_hilos():
            for hilo in self.hilos:  
                if hilo.is_alive():  # Verificar si el hilo está en ejecución  
                    print(f"Esperando a que termine el hilo {hilo.name}...")  
                    hilo.join(timeout=TIEMPO_A_ESPERAR_MÁXIMO)  
            ventana_cierre.cerrar() #Cierra el diálogo
            self.destroy()  # Cierra la ventana principal (y la app)

        # Ejecuta la espera de los hilos en un *NUEVO* hilo
        threading.Thread(target=esperar_hilos, daemon=True).start()
    
    def actualizarIconoFacturar(self):
        """Actualiza visualmente el Label que simula un Checkbox."""
        if self.var_facturar_medio.get():
            self.lbl_icono_facturar.config(text="☑", foreground=COLOR_ACENTO, font=('Segoe UI', 14))
        else:
            self.lbl_icono_facturar.config(text="☐", foreground="#555", font=('Segoe UI', 14))

    def toggleFacturar(self, event=None):
        """Cambia el estado del Checkbox al hacer clic."""
        # ERROR POTENCIAL: Solo actualiza visualmente si la lógica no está bien conectada
        estado = not self.var_facturar_medio.get()
        self.var_facturar_medio.set(estado) # <-- ASEGÚRATE DE QUE ESTA LÍNEA ESTÉ
        self.actualizarIconoFacturar()
    
    def ordenarColumna(self, tree, col, descendente, nombre_tabla=None):
        """
        Ordena una tabla (tree) por una columna (col).
        Maneja Números (Precios), Fechas y Texto.
        """
        # 1. Guardar el estado actual
        if nombre_tabla:
            self.estado_orden[nombre_tabla] = (col, descendente)

        # 2. Obtener la lista de tuplas
        datos = [(tree.set(k, col), k) for k in tree.get_children('')]

        # 3. Intentar ordenar
        try:
            # A. Intento numérico (para Precios, ID, Stock)
            # Quitamos '$' y espacios
            datos.sort(key=lambda t: float(t[0].replace('$', '').strip()), reverse=descendente)
        
        except ValueError:
            try:
                # B. Intento de FECHA (para la columna "Fecha y hora")
                # Usamos el mismo formato que definiste en funciones_útiles
                formato = funciones_útiles.FORMATO_PREFERIDO_HORA_Y_FECHA
                datos.sort(key=lambda t: datetime.strptime(t[0], formato), reverse=descendente)
            
            except ValueError:
                # C. Fallback: Orden alfabético (para Nombres, Códigos, etc.)
                datos.sort(key=lambda t: t[0].lower(), reverse=descendente)

        # 4. Mover los ítems y REAPLICAR TAGS DE COLOR
        for index, (val, k) in enumerate(datos):
            tree.move(k, '', index)
            
            tag_fila = 'par' if index % 2 == 0 else 'impar'
            
            # Mantenemos el tag 'alerta' si ya lo tenía
            tags_actuales = list(tree.item(k, 'tags'))
            if 'alerta' in tags_actuales:
                tree.item(k, tags=('alerta',))
            else:
                tree.item(k, tags=(tag_fila,))

        # 5. Actualizar el encabezado
        tree.heading(col, command=lambda: self.ordenarColumna(tree, col, not descendente, nombre_tabla))
    
    def aplicarOrdenGuardado(self, tree, nombre_tabla):
        """
        Re-aplica el ordenamiento guardado a una tabla después de recargarla.
        """
        # Recupera la columna y el sentido (asc/desc) del diccionario de estado
        columna, descendente = self.estado_orden.get(nombre_tabla, (None, False))
        
        # Si hay un orden guardado para esa tabla, lo aplicamos
        if columna:
            self.ordenarColumna(tree, columna, descendente, nombre_tabla)
    
if __name__ == "__main__":
    app = Aplicación()
    app.mainloop()