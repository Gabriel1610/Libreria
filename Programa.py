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
ANCHO_COLUMNA_NOMBRE_PRODUCTOS = 425
MÁX_CARACTERES_NOMBRE_PRODUCTO = 100
MENSAJE_LÍMITE_NOMBRE_PRODUCTO = f"El nombre del producto no puede superar los {MÁX_CARACTERES_NOMBRE_PRODUCTO} caracteres."

PADX_ETIQUETA_PRECIO_PRODUCTOS = 0
PADY_ETIQUETA_PRECIO_PRODUCTOS = 0  # Padding específico para la etiqueta precio
PADX_ENTRADA_IZQUIERDA_PRECIO_PRODUCTOS = (80, 0)
MÁX_DÍGITOS_PRECIO = 10
MÁX_DECIMALES_PRECIO = 2

PADX_ETIQUETA_STOCK_ACTUAL_PRODUCTOS = 0
PADY_ETIQUETA_STOCK_ACTUAL_PRODUCTOS = 0  # Padding específico para la etiqueta stock

PADX_ENTRADA_IZQUIERDA_STOCK_ACTUAL_PRODUCTOS = (110, 0)
PADY_WIDGETS_GENERAL_PRODUCTOS = 5   # Padding vertical para la mayoría de widgets

ANCHO_ENTRADA_NOMBRE_PRODUCTOS = 40
ANCHO_ENTRADA_PRECIO_PRODUCTOS = 20

ETIQUETA_STOCK_ACTUAL_TEXTO_PRODUCTOS = "Stock actual:"
ANCHO_ENTRADA_STOCK_ACTUAL_PRODUCTOS = 11 # Puedes ajustar este valor según sea necesario
MÁX_STOCK_ACTUAL_PRODUCTO = 4294967295  # Define el valor máximo permitido para el stock actual
ETIQUETA_STOCK_MÍNIMO_TEXTO_PRODUCTOS = "Stock mínimo:"
ANCHO_ENTRADA_STOCK_MÍNIMO_PRODUCTOS = 11 # Puedes ajustar este valor según sea necesario
MÁX_STOCK_MÍNIMO_PRODUCTO = 4294967295  # Define el valor máximo permitido para el stock mínimo

PADX_ETIQUETA_STOCK_MÍNIMO_PRODUCTOS = 0
PADY_ETIQUETA_STOCK_MÍNIMO_PRODUCTOS = 0  # Padding específico para la etiqueta stock mínimo
PADX_ENTRADA_IZQUIERDA_STOCK_MÍNIMO_PRODUCTOS = (120, 0)

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

PADX_BOTÓN_AÑADIR_PRODUCTOS = (0, 0)
PADX_BOTÓN_EDITAR_PRODUCTOS = (100, 0)
PADX_BOTÓN_ELIMINAR_PRODUCTOS = (200, 0)
PADX_BOTÓN_LIMPIAR_PRODUCTOS = (300, 0)
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
ANCHO_ENTRADA_CÓDIGO_VENTA = 20
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
STOCK_ACTUAL_TABLA_ALERTA = 1
STOCK_MÍNIMO_TABLA_ALERTA = 2

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

            # Posiciona el cuaderno (con las pestañas) en la ventana principal.
            self.cuaderno.grid(column=0, row=0, sticky="nsew")

            # Llama a los métodos para crear los diferentes elementos de la interfaz:
            self.crearTablaConProductos()  # Crea la tabla principal.
            self.crearTablaStockAlerta()
            self.crearLabelFrameProductos() # Crea el LabelFrame para agregar productos.
            self.crearTablaConVentas()
            self.crearLabelFrameVentaProducto()
            self.crearTablaCarrito()
            self.actualizarTablaVentasEnHilo()

            self.etiqueta_total_produdcto = ttk.Label(self.página_cuaderno_ventas, 
                                                      text=ETIQUETA_TOTAL_PRODUCTOS,
                                                      font=FUENTE_TOTAL_PRODUCTO)
            self.etiqueta_total_produdcto.grid(column=COLUMNA_TOTAL_PRODUCTOS, row=FILA_TOTAL_PRODUCTO, 
                                    padx=PADX_TOTAL_PRODUCTO, 
                                    pady=PADY_TOTAL_PRODUCTO, 
                                    sticky=STICKY_TOTAL_PRODUCTO)

            self.etiqueta_valor_total_produdcto = ttk.Label(self.página_cuaderno_ventas, 
                                                      text=ETIQUETA_VALOR_TOTAL_PRODUCTOS,
                                                      font=FUENTE_TOTAL_PRODUCTO)
            self.etiqueta_valor_total_produdcto.grid(column=COLUMNA_VALOR_TOTAL_PRODUCTOS, row=FILA_TOTAL_PRODUCTO, 
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
            'stock_actual',
            'stock_mínimo',
            'descripción'
        )

        self.tabla_productos = ttk.Treeview(
            self.página_cuaderno_productos,
            columns=columnas,
            show='headings',
            height=5
        )

        self.tabla_productos.heading('código', text='Código')
        self.tabla_productos.heading('nombre', text='Nombre')
        self.tabla_productos.heading('precio', text='Precio')
        self.tabla_productos.heading('stock_actual', text='Stock actual')
        self.tabla_productos.heading('stock_mínimo', text='Stock mínimo')
        self.tabla_productos.heading('descripción', text='Descripción', anchor='w')

        # Habilitar ordenamiento por clic en columnas
        for col in columnas:
            self.tabla_productos.heading(col, command=lambda c=col: self.ordenarColumna(self.tabla_productos, c, False, 'productos'))

        self.tabla_productos.grid(
            row=1,
            column=0,
            columnspan=2,
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
            width=100,
            minwidth=100,
            stretch=tk.NO
        )
        
        self.tabla_productos.column(
            "stock_actual",
            anchor='center',
            width=100,
            minwidth=100,
            stretch=tk.NO
        )
        self.tabla_productos.column(
            "stock_mínimo",
            anchor='center',
            width=100,
            minwidth=100,
            stretch=tk.NO
        )
        self.tabla_productos.column(
            "descripción",
            width=1000,
            minwidth=1000,
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

        self.barra_desplazamiento_vertical.grid(row=1, column=2, sticky='ns')
        self.barra_desplazamiento_horizontal.grid(row=2, column=0, columnspan=2, sticky='we')

        self.tabla_productos.bind("<<TreeviewSelect>>", self.cargarRegistros)
    
    # (Fin de crearLabelFrameProductos, línea 519)

    def crearTablaStockAlerta(self):
        """
        Crea la etiqueta y la tabla (Treeview) para mostrar los productos
        con bajo stock en la pestaña de productos.
        """
        # --- 1. Crear la Etiqueta ---
        self.etiqueta_stock_alerta = ttk.Label(self.página_cuaderno_productos, 
                                               text="Stock en alerta", 
                                               font=FUENTE_TÍTULO_PRODUCTOS) # Re-usamos la fuente
        
        # Posicionar la etiqueta (Fila 4, debajo del formulario)
        self.etiqueta_stock_alerta.grid(column=1, row=3, columnspan=2, 
                                        padx=10, pady=(0, 0), sticky="w")

        # --- 2. Definir Columnas ---
        columnas_stock = ('código', 'stock_actual', 'stock_mínimo', 'nombre')

        self.tabla_stock_alerta = ttk.Treeview(
            self.página_cuaderno_productos,
            columns=columnas_stock,
            show='headings',
            height=12,  # Altura para la tabla de alertas
            selectmode='none'  # <-- AÑADE ESTA LÍNEA
        )

        # 3. Configurar el tag para la alerta (texto rojo)
        self.tabla_stock_alerta.tag_configure('alerta', foreground='red')

        # --- 4. Definir Encabezados ---
        self.tabla_stock_alerta.heading('código', text='Código', anchor='w')
        self.tabla_stock_alerta.heading('stock_actual', text='Stock actual', anchor='center')
        self.tabla_stock_alerta.heading('stock_mínimo', text='Stock mínimo', anchor='center')
        self.tabla_stock_alerta.heading('nombre', text='Nombre', anchor='w')

        # --- 5. Posicionar la Tabla ---
        self.tabla_stock_alerta.grid(
            row=4,
            column=1,
            padx=(10, 0),
            columnspan=2, # Ocupa todo el ancho horizontal
            sticky='nsew' # Se expande para llenar el espacio
        )

        # --- 6. Definir Anchos de Columna ---
        # (Ajustados para que la tabla se expanda)
        self.tabla_stock_alerta.column("código", anchor='w', width=205, stretch=tk.NO)
        self.tabla_stock_alerta.column("stock_actual", anchor='center', width=100, stretch=tk.NO)
        self.tabla_stock_alerta.column("stock_mínimo", anchor='center', width=100, stretch=tk.NO)
        self.tabla_stock_alerta.column("nombre", anchor='w', width=ANCHO_COLUMNA_NOMBRE_PRODUCTOS, stretch=tk.NO) # Se estira
        
        # --- 7. Scrollbars para la nueva tabla ---
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

        # Posicionar scrollbars
        self.barra_desplazamiento_vertical_stock.grid(row=4, column=3, sticky='ns')
        self.barra_desplazamiento_horizontal_stock.grid(row=5, column=1, columnspan=2, sticky='we')

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
        total_actual_str = self.etiqueta_valor_total_produdcto.cget('text')
        total_actual_float = float(total_actual_str)
        nuevo_total_float = total_actual_float - subtotal_a_restar

        self.etiqueta_valor_total_produdcto.config(text=f"{nuevo_total_float:.2f}")

    def crearTablaConVentas(self):
        """
        Crea la etiqueta y la tabla (Treeview) para mostrar el listado
        de ventas en la pestaña de ventas.
        """
        
        # --- 1. Crear la Etiqueta "Ventas" (Fila 0) ---
        self.etiqueta_título_ventas = ttk.Label(self.página_cuaderno_ventas, 
                                               text="Ventas", 
                                               font=FUENTE_TÍTULO_PRODUCTOS) # Re-usamos la fuente
        
        # Posicionar la etiqueta (Fila 0, Col 0)
        self.etiqueta_título_ventas.grid(column=0, row=0, 
                                        padx=5, pady=(2, 2), sticky="w")

        # --- 2. Definir Columnas ---
        columnas_ventas = ('id', 'fecha_hora', 'total')

        self.tabla_ventas = ttk.Treeview(
            self.página_cuaderno_ventas,
            columns=columnas_ventas,
            show='headings',
            height=15  # Altura de la tabla
        )

        # --- 3. Definir Encabezados ---
        self.tabla_ventas.heading('id', text='ID', anchor='center')
        self.tabla_ventas.heading('fecha_hora', text='Fecha y hora', anchor='center')
        self.tabla_ventas.heading('total', text='Total', anchor='center')

        # Habilitar ordenamiento por clic en columnas
        for col in columnas_ventas:
            self.tabla_ventas.heading(col, command=lambda c=col: self.ordenarColumna(self.tabla_ventas, c, False, 'ventas'))

        # --- 4. Posicionar la Tabla (Fila 1, Col 0) ---
        self.tabla_ventas.grid(
            row=1,
            column=0,
            rowspan=2,
            sticky='nsw' # Se expande verticalmente (ns) y se pega a la izquierda (w)
        )

        # --- 5. Definir Anchos de Columna (No expandibles) ---
        self.tabla_ventas.column("id", anchor='center', width=85, stretch=tk.NO)
        self.tabla_ventas.column("fecha_hora", anchor='center', width=125, stretch=tk.NO)
        self.tabla_ventas.column("total", anchor='e', width=120, stretch=tk.NO)
        
        # --- 6. Scrollbars para la tabla de ventas ---
        self.barra_desplazamiento_vertical_ventas = ttk.Scrollbar(
            self.página_cuaderno_ventas,
            orient=tk.VERTICAL,
            command=self.tabla_ventas.yview
        )
        self.barra_desplazamiento_horizontal_ventas = ttk.Scrollbar(
            self.página_cuaderno_ventas,
            orient=tk.HORIZONTAL,
            command=self.tabla_ventas.xview
        )

        self.tabla_ventas.configure(xscrollcommand=self.barra_desplazamiento_horizontal_ventas.set)
        self.tabla_ventas.configure(yscrollcommand=self.barra_desplazamiento_vertical_ventas.set)

        # --- 7. Posicionar scrollbars ---
        self.barra_desplazamiento_vertical_ventas.grid(row=1, column=1, rowspan=2, sticky='ns')
        self.barra_desplazamiento_horizontal_ventas.grid(row=3, column=0, sticky='nwe')
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
        # --- Stock Actual ---
        self.etiqueta_stock = ttk.Label(self.labelframe_productos, text=ETIQUETA_STOCK_ACTUAL_TEXTO_PRODUCTOS)
        self.etiqueta_stock.grid(column=0, row=3,
                                padx=PADX_ETIQUETA_STOCK_ACTUAL_PRODUCTOS, 
                                pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        self.stock = tk.StringVar()
        self.entrada_stock = ttk.Entry(self.labelframe_productos, 
                                    width=ANCHO_ENTRADA_STOCK_ACTUAL_PRODUCTOS, 
                                    textvariable=self.stock)
        self.entrada_stock.grid(column=0, row=3,
                                padx=PADX_ENTRADA_IZQUIERDA_STOCK_ACTUAL_PRODUCTOS, 
                                pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        self.entrada_stock.bind(EVENTO_TECLA_PRESIONADA, 
                                lambda event, widget=self.entrada_stock, var=self.stock: 
                                self.controlar_caracteres_solo_enteros(event, widget, var, max_valor=MÁX_STOCK_ACTUAL_PRODUCTO))

        # --- Stock Mínimo ---
        self.etiqueta_stock_mínimo = ttk.Label(self.labelframe_productos, text=ETIQUETA_STOCK_MÍNIMO_TEXTO_PRODUCTOS)
        self.etiqueta_stock_mínimo.grid(column=0, row=4,
                                        padx=PADX_ETIQUETA_STOCK_MÍNIMO_PRODUCTOS, 
                                        pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                        sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        self.stock_mínimo = tk.StringVar()
        self.entrada_stock_mínimo = ttk.Entry(self.labelframe_productos, 
                                            width=ANCHO_ENTRADA_STOCK_MÍNIMO_PRODUCTOS, 
                                            textvariable=self.stock_mínimo)
        self.entrada_stock_mínimo.grid(column=0, row=4,
                                        padx=PADX_ENTRADA_IZQUIERDA_STOCK_MÍNIMO_PRODUCTOS, 
                                        pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                        sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        
        self.entrada_stock_mínimo.bind(EVENTO_TECLA_PRESIONADA, 
                                       lambda event, widget=self.entrada_stock_mínimo, var=self.stock_mínimo: 
                                       self.controlar_caracteres_solo_enteros(event, widget, var, max_valor=MÁX_STOCK_MÍNIMO_PRODUCTO))

        # --- Descripción (en Columna 1) ---
        self.etiqueta_descripción = ttk.Label(self.labelframe_productos, 
                                            text=ETIQUETA_DESCRIPCIÓN_TEXTO_PRODUCTOS)
        # Etiqueta en Col 1, Fila 0 (para alinear con "Nombre")
        self.etiqueta_descripción.grid(column=1, row=0, 
                                    padx=PADX_WIDGETS_DESCRIPCIÓN_PRODUCTOS, 
                                    pady=PADY_ETIQUETA_DESCRIPCIÓN_PRODUCTOS, 
                                    sticky=STICKY_WIDGET_OESTE_PRODUCTOS) # Re-usamos "w"

        self.texto_desplazado = st.ScrolledText(self.labelframe_productos, 
                                                width=ANCHO_TEXTO_DESCRIPCIÓN_PRODUCTOS, 
                                                height=ALTO_TEXTO_DESCRIPCIÓN_PRODUCTOS, 
                                                wrap=WRAP_TEXTO_DESCRIPCIÓN_PRODUCTOS,
                                                font=('Segoe UI', 10),          # Fuente moderna
                                                relief="solid",                 # Borde plano (sin efecto 3D)
                                                borderwidth=1,                  # Borde fino y elegante
                                                padx=10, pady=10,               # "Aire" interno para que el texto no toque los bordes
                                                bg=COLOR_BLANCO,                # Fondo blanco limpio
                                                fg=COLOR_TEXTO,                 # Color de texto gris oscuro
                                                selectbackground=COLOR_ACENTO,  # Color de selección azul (tu color de acento)
                                                selectforeground="white")       # Texto blanco al seleccionar

        # Texto en Col 1, Fila 2, y se expande 3 filas (para alinear con Precio, Stock y Stock Mínimo)
        self.texto_desplazado.grid(column=1, row=1, 
                                rowspan=FILASPAN_TEXTO_DESCRIPCIÓN_PRODUCTOS,
                                padx=PADX_WIDGETS_DESCRIPCIÓN_PRODUCTOS, 
                                pady=PADY_TEXTO_DESCRIPCIÓN_PRODUCTOS, 
                                sticky=STICKY_TEXTO_DESCRIPCIÓN_PRODUCTOS) # "nsew" para que llene

        self.texto_desplazado.bind(EVENTO_TECLA_PRESIONADA, self.limitar_caracteres_descripción)

        # - Etiqueta: contador de caracteres restantes para la descripción.
        #    - Muestra el número máximo de caracteres permitidos (MÁX_CAR_DESCRIP).
        #    - Se actualiza dinámicamente con 'self.limitar_caracteres_descripción'.
        self.etiqueta_contador_caracteres = ttk.Label(self.labelframe_productos, text=str(MÁX_CAR_DESCRIP))
        self.etiqueta_contador_caracteres.grid(column=1, row=5, padx=(300, 0), pady=(0, 0), sticky="w")
        self.etiqueta_contador_caracteres.configure(style="verde.TLabel")  # Color verde inicial (suficientes caracteres)

        # --- Botones: Añadir, Editar, Eliminar, Limpiar --- (Fila 6)

        # --- Botón Añadir ---
        self.botón_añadir_productos = ttk.Button(self.labelframe_productos, 
                                                 text=TEXTO_BOTÓN_AÑADIR_PRODUCTOS, 
                                                 command=self.añadirProducto)
        self.botón_añadir_productos.grid(column=0, row=6, 
                                         padx=PADX_BOTÓN_AÑADIR_PRODUCTOS, 
                                         pady=PADY_WIDGETS_GENERAL_PRODUCTOS, # Reutilizamos constante
                                         sticky=STICKY_WIDGET_OESTE_PRODUCTOS) # Reutilizamos constante

        
        # --- Botón Editar ---
        self.botón_editar_productos = ttk.Button(self.labelframe_productos, 
                                                 text=TEXTO_BOTÓN_EDITAR_PRODUCTOS, 
                                                 command=self.editarProducto) # (Asumo que la función se llama así)
        self.botón_editar_productos.grid(column=0, row=6, 
                                         padx=PADX_BOTÓN_EDITAR_PRODUCTOS, 
                                         pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                         sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        
        # --- Botón Eliminar ---
        self.botón_eliminar_productos = ttk.Button(self.labelframe_productos, 
                                                   text=TEXTO_BOTÓN_ELIMINAR_PRODUCTOS, 
                                                   command=self.eliminarProducto) # (Asumo que la función se llama así)
        self.botón_eliminar_productos.grid(column=0, row=6, 
                                           padx=PADX_BOTÓN_ELIMINAR_PRODUCTOS, 
                                           pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                           sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        
        # --- Botón Limpiar ---
        self.botón_limpiar_productos = ttk.Button(self.labelframe_productos, 
                                                  text=TEXTO_BOTÓN_LIMPIAR_PRODUCTOS, 
                                                  command=self.limpiarCamposProductos) # (Asumo que la función se llama así)
        self.botón_limpiar_productos.grid(column=0, row=6, 
                                          padx=PADX_BOTÓN_LIMPIAR_PRODUCTOS, 
                                          pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                          sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
    
        # --- Botón Buscar ---
        self.botón_buscar_productos = ttk.Button(self.labelframe_productos, 
                                                  text=TEXTO_BOTÓN_BUSCAR_PRODUCTOS, 
                                                  command=self.buscarProducto) # (Asumo que la función se llama así)
        self.botón_buscar_productos.grid(column=1, row=6, 
                                          padx=PADX_BOTÓN_BUSCAR_PRODUCTOS, 
                                          pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                          sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        
        # --- Botón mostrar Todo ---

        self.botón_mostrar_todos_los_productos = ttk.Button(self.labelframe_productos, text=TEXTO_BOTÓN_MOSTRAR_TODOS_LOS_PRODUCTOS,
                                                            command=self.mostrarTodosLosProductos)
        self.botón_mostrar_todos_los_productos.grid(column=1, row=6, 
                                          padx=PADX_BOTÓN_MOSTRAR_TODOS_LOS_PRODUCTOS, 
                                          pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                          sticky=STICKY_WIDGET_OESTE_PRODUCTOS)

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
        self.labelframe_venta_producto.grid(column=0, row=5, rowspan=1,
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
                                            width=ANCHO_ENTRADA_CÓDIGO_VENTA, 
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
        self.botón_agregar_carrito.grid(column=5, row=0, 
                                      padx=PADX_GENERAL_VENTA, 
                                      pady=PADY_GENERAL_VENTA, 
                                      sticky=STICKY_WIDGET_OESTE_VENTA)
        
        # Botón "Limpiar"
        self.botón_limpiar = ttk.Button(self.labelframe_venta_producto, 
                                           text=BOTÓN_LIMPIAR_VENTA,
                                           command=self.limpiarCamposVenta)
        self.botón_limpiar.grid(column=6, row=0, 
                                   padx=PADX_GENERAL_VENTA, 
                                   pady=PADY_GENERAL_VENTA, 
                                   sticky=STICKY_WIDGET_OESTE_VENTA)

        # --- Fila 2 (Interior) ---
        
        # Botón "Eliminar venta"
        self.botón_eliminar_venta = ttk.Button(self.labelframe_venta_producto, 
                                               text=BOTÓN_ELIMINAR_VENTA_VENTA,
                                               command=self.eliminarVenta, # Asignamos la nueva función
                                               state='disabled')
        self.botón_eliminar_venta.grid(column=3, row=1, # Col 3, Fila 1 (Nuevo espacio)
                                      padx=PADX_GENERAL_VENTA, 
                                      pady=PADY_GENERAL_VENTA, 
                                      sticky=STICKY_WIDGET_OESTE_VENTA)
        
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
            self.etiqueta_valor_total_produdcto.config(text="0.00")
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
            # (Devuelve: codigo, nombre, precio_unitario, cantidad, subtotal)
            detalles = self.base_de_datos.consultarDetalleVenta(id_venta_seleccionada)

            if detalles is None:
                MensajeModerno(self, "Error de BD", "No se pudieron consultar los detalles de la venta.", tipo="error")
                self.etiqueta_valor_total_produdcto.config(text="0.00") # Reset total
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
            self.etiqueta_valor_total_produdcto.config(text=f"{total_recuperado:.2f}")

            # Activar el botón "Eliminar venta"
            self.botón_eliminar_venta.config(state='normal')

        except Exception as e:
            MensajeModerno(self, "Error", f"Ocurrió un error al cargar los detalles: {str(e)}", tipo="error")
            self.etiqueta_valor_total_produdcto.config(text="0.00") # Reset total

    def finalizarVenta(self):
        """
        Finaliza la venta actual:
        1. Verifica que el carrito no esté vacío.
        2. Registra la VENTA.
        3. Registra el DETALLE_VENTA para cada ítem.
        4. Actualiza el STOCK de cada producto.
        5. Refresca la tabla de ventas.
        6. Refresca la tabla de productos (stock).
        """
        
        # 1. Obtener todos los items del carrito
        items_carrito_ids = self.tabla_carrito.get_children()

        # Condición 1: Carrito vacío
        if not items_carrito_ids:
            MensajeModerno(self,"Carrito vacío", "No hay productos en el carrito para finalizar la venta.", tipo="advertencia")
            return

        # Confirmar la venta con el total
        total_venta_str = self.etiqueta_valor_total_produdcto.cget('text')
        total_float = float(total_venta_str) # Convertimos a float para la factura
        confirmación = MensajeModerno(self, "Confirmar Venta", 
                                        f"¿Desea finalizar la venta por un total de $ {total_venta_str}?", tipo="pregunta")
        respuesta = confirmación.resultado
        if not respuesta:
            return

        # --- INICIO FACTURACIÓN AFIP ---
        # Intentamos facturar ANTES de guardar en la BD local
        # (Opcional: Puedes hacerlo al revés si prefieres guardar aunque falle AFIP)
        
        resultado_afip = facturación.emitir_factura_b(total_float)
        
        if not resultado_afip['exito']:
            MensajeModerno(self, "Error AFIP", resultado_afip['mensaje'], tipo="error")
            return # Cancelamos todo si no se pudo facturar
            
        cae = resultado_afip['cae']
        nro_factura = resultado_afip['numero_factura']
        # --- FIN FACTURACIÓN AFIP ---

        try:
            # 2. Guardar los datos de las filas ANTES de borrarlas
            items_a_procesar = []
            for item_id in items_carrito_ids:
                # (código, nombre, precio_unitario, cantidad, subtotal)
                items_a_procesar.append(self.tabla_carrito.item(item_id, 'values'))

            # 3. Registrar la VENTA principal y obtener el id_venta
            fecha_actual = datetime.now()
            id_venta_generado = self.base_de_datos.registrarVenta([fecha_actual])

            if id_venta_generado is None:
                MensajeModerno(self, "Error", "No se pudo registrar la venta principal.", tipo="error")
                return

            # 4. Registrar los DETALLES y actualizar STOCK (Loop)
            for item in items_a_procesar:
                código = item[0]
                precio_unitario = float(item[2])
                cantidad = int(item[3])

                # 4a. Ingresar el detalle de la venta
                #     Espera: [id_venta, código_producto, cantidad, precio_unitario]
                datos_detalle = [id_venta_generado, código, cantidad, precio_unitario]
                self.base_de_datos.ingresarDetalleVenta(datos_detalle)

                # 4b. Actualizar (restar) el stock del producto
                #     Espera: [cantidad_vendida, codigo_producto]
                datos_stock = [cantidad, código]
                self.base_de_datos.actualizarStockProducto(datos_stock)
            
            # 5. Limpiar la UI de Venta
            funciones_útiles.borrarTodasLasFilas(self.tabla_carrito)
            self.etiqueta_valor_total_produdcto.config(text="0.00") # Reset total
            self.limpiarCamposVenta()

            # 6. Refrescar la tabla de VENTAS (ahora que hay una nueva)
            self.actualizarTablaVentasEnHilo()

            # 7. Refrescar la tabla de PRODUCTOS (porque el stock cambió)
            self.datos = self.base_de_datos.consultarDatosProductos() # Recargar datos principales
            self.cargarDatosEnTablaEnHilo() # Esto actualiza tabla_productos y tabla_alertas

            # 8. Respaldar la base de datos
            funciones_útiles.crearHiloRespaldarBaseDeDatos(self.base_de_datos)

            MensajeModerno(self, "Éxito", 
                           f"Venta registrada correctamente.\n\n"
                           f"Factura B N°: {nro_factura}\n"
                           f"CAE: {cae}", 
                           tipo="éxito")

        except ValueError as ve:
            # Captura errores de "Stock insuficiente" o "Código duplicado en carrito"
            MensajeModerno(self, "Error en Venta", str(ve), tipo="error")
        except Exception as e:
            # Captura cualquier otro error de BD
            MensajeModerno(self, "Error Crítico", f"Ocurrió un error al procesar la venta: {str(e)}", tipo="error")

    def actualizarTablaVentas(self):
        """
        Consulta la base de datos para obtener todas las ventas con su total
        y actualiza la 'tabla_ventas' en la interfaz.
        """
        
        try:
            
            self.tabla_ventas.tag_configure('impar', background=COLOR_BLANCO)
            self.tabla_ventas.tag_configure('par', background=COLOR_FONDO_APP)

            # 1. Consultar los datos frescos
            lista_ventas = self.base_de_datos.consultarVentasConTotal()

            # 2. Borrar todos los items existentes
            funciones_útiles.borrarTodasLasFilas(self.tabla_ventas)
            
            # 3. Cargar datos en la tabla
            if lista_ventas:
                for i, venta in enumerate(lista_ventas):
                    # Formatear la fecha/hora
                    id_v = venta[0]
                    fecha_hora_dt = venta[1] # Es un objeto datetime
                    fecha_hora_str = fecha_hora_dt.strftime(funciones_útiles.FORMATO_PREFERIDO_HORA_Y_FECHA)
                    total = f"{venta[2]:.2f}"
                    
                    # Calcular par/impar
                    tag_fila = 'par' if i % 2 == 0 else 'impar'
                    
                    # Insertar CON tags
                    self.tabla_ventas.insert('', tk.END, values=(id_v, fecha_hora_str, total), tags=(tag_fila,))
            
            self.aplicarOrdenGuardado(self.tabla_ventas, 'ventas')
                    
        except Exception as e:
            MensajeModerno(self, "Error", f"No se pudieron cargar las ventas: {str(e)}", tipo="error")
            
    def agregarAlCarrito(self):
        """
        Agrega o actualiza un producto en el carrito, verificando el stock.

        1. Valida campos de entrada.
        2. Consulta el producto y su stock.
        3. Verifica si el producto ya está en el carrito.
        4. Calcula el stock total necesario (nuevo + en carrito).
        5. Compara con el stock disponible y advierte si es insuficiente.
        6. Si hay stock, INSERTA una nueva fila o ACTUALIZA la existente.
        7. Actualiza el total del carrito.
        """
        
        # 1. Validación de campos (Código y Cantidad no vacíos)
        if not self.esUnProductoValidoParaElCarrito():
            return
        
        código = self.código_venta.get().strip()
        cantidad_deseada_str = self.cantidad_venta.get().strip()
        cantidad_deseada = int(cantidad_deseada_str) # Convertir ahora

        # 2. Consultar producto (Necesitamos el stock disponible primero)
        try:
            producto_encontrado = self.base_de_datos.buscarProductoPorCódigo(código)
        except Exception as e:
            MensajeModerno(self, "Error de BD", f"Error al buscar el producto por código: {str(e)}", tipo="error")
            return

        # 3. Producto no encontrado
        if not producto_encontrado:
            MensajeModerno(self, "No encontrado", "No existe un producto con ese código.", tipo="info")
            self.entrada_código_producto_venta.focus()
            return

        # 4. PROCESAR Y VERIFICAR STOCK
        # (Índices: 1:nombre, 2:precio_venta, 3:stock_actual)
        nombre = producto_encontrado[1]
        precio_unitario = float(producto_encontrado[2])
        stock_disponible = int(producto_encontrado[3])

        # 5. VERIFICAR SI EL PRODUCTO YA ESTÁ EN EL CARRITO
        cantidad_en_carrito = 0
        item_id_en_carrito = None # Para saber si debemos UPTATE o INSERT

        for item_id in self.tabla_carrito.get_children():
            fila = self.tabla_carrito.item(item_id, 'values')
            if fila[0].lower() == código.lower(): # Si el código (fila[0]) coincide
                cantidad_en_carrito = int(fila[3]) # Obtener la cantidad (fila[3])
                item_id_en_carrito = item_id # Guardar el ID de la fila
                break # Encontramos el producto, salir del loop
        
        # 6. Calcular stock total necesario
        stock_necesario = cantidad_deseada + cantidad_en_carrito

        # 7. ¡La Validación de Stock!
        if stock_necesario > stock_disponible:
            MensajeModerno(self,"Stock Insuficiente", 
                                 f"No hay stock suficiente para '{nombre}'.\n\n"
                                 f"Stock disponible: {stock_disponible}\n"
                                 f"Cantidad ya en carrito: {cantidad_en_carrito}\n"
                                 f"Cantidad deseada: {cantidad_deseada}\n\n"
                                 f"Total necesario: {stock_necesario}",
                                 tipo="advertencia")
            self.entrada_cantidad_venta.focus()
            return # Detener la función

        # 8. Si hay stock, INSERTAR o ACTUALIZAR
        
        # Subtotal de los *nuevos* items a añadir
        subtotal_float_nuevo = precio_unitario * cantidad_deseada 
        
        # Calcular la *nueva cantidad total* y el *nuevo subtotal* para la FILA
        nueva_cantidad_total_item = cantidad_deseada + cantidad_en_carrito
        nuevo_subtotal_item_fila = precio_unitario * nueva_cantidad_total_item
        
        # Preparar los valores de la fila
        valores_fila = (
            código, 
            nombre, 
            str(precio_unitario), 
            nueva_cantidad_total_item, 
            f"{nuevo_subtotal_item_fila:.2f}" # Usar el *total* subtotal para la fila
        )

        # Calcular si la nueva fila será par o impar basándonos en cuántas hay
        numero_filas_actuales = len(self.tabla_carrito.get_children())
        tag_fila = 'par' if numero_filas_actuales % 2 == 0 else 'impar'

        # Configurar estilos (solo necesitas hacerlo una vez, pero aquí asegura que existan)
        self.tabla_carrito.tag_configure('impar', background=COLOR_BLANCO)
        self.tabla_carrito.tag_configure('par', background=COLOR_FONDO_APP)
        
        if item_id_en_carrito:
            # ACTUALIZAR la fila existente
            self.tabla_carrito.item(item_id_en_carrito, values=valores_fila)
        else:
            # INSERTAR una nueva fila
            self.tabla_carrito.insert('', tk.END, values=valores_fila, tags=(tag_fila,))

        # 9. Actualizar el Valor total de la venta
        # Sumamos solo el subtotal de la cantidad *nueva* que se agregó
        total_actual_str = self.etiqueta_valor_total_produdcto.cget('text')
        nuevo_total_float = float(total_actual_str) + subtotal_float_nuevo
        nuevo_total_formateado = f"{nuevo_total_float:.2f}"
        self.etiqueta_valor_total_produdcto.config(text=nuevo_total_formateado)
        
        # 10. Limpiar campos de entrada de venta para el próximo producto
        self.limpiarCamposVenta()

    def esUnProductoValidoParaElCarrito(self):
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

    def añadirProducto(self):
        """
        Valida los campos de entrada y añade el nuevo producto a la base de datos.
        """
        if self.esUnProductoVálido():  # 1. Verifica si los datos ingresados son válidos.
            # 2. Obtiene el código del producto
            código = self.código.get().strip()
            # 3. Obtiene el resto de los datos de los widgets de entrada
            nombre = self.nombre.get().strip()
            # La validación ya confirmó que estos son números válidos
            precio = float(self.precio.get().strip())
            stock_actual = int(self.stock.get().strip())
            stock_mínimo = int(self.stock_mínimo.get().strip())
            descripción = self.texto_desplazado.get("1.0", tk.END).strip()

            # 4. Crea una lista con los datos del nuevo producto
            #    (El orden debe coincidir con el de tu tabla en la base de datos)
            producto = [
                código,
                nombre,
                nombre,
                descripción,
                descripción,
                precio,
                stock_actual,
                stock_mínimo
            ]
                
            try:
                # 5. Llama a la función para ingresar el producto en la base de datos.
                self.base_de_datos.ingresarProducto(producto)
                
                # 6. Actualiza la interfaz
                self.limpiarCamposProductos()      # Limpia los campos de entrada
                self.datos = self.base_de_datos.consultarDatosProductos()  # Actualiza la lista de datos
                self.cargarDatosEnTablaEnHilo()  # Recarga los datos en la tabla (en un hilo)

                # 7. Respalda la base de datos (como en tus otras funciones)
                funciones_útiles.crearHiloRespaldarBaseDeDatos(self.base_de_datos)
                
                MensajeModerno(self, "Éxito", "Producto añadido correctamente.", tipo="info")

            # --- NUEVO BLOQUE "except" ---
            except ValueError as ve:
                # Captura el error de "Código duplicado" que lanzamos desde la BD
                MensajeModerno(self, "Error de Duplicado", str(ve), tipo="error")
                self.entrada_código.focus() # Pone el foco en el campo incorrecto

            except Exception as e: # Captura todos los demás errores
                MensajeModerno(self, "Error de Base de Datos", 
                              f"No se pudo añadir el producto: {str(e)}", tipo="error")

    def esUnProductoVálido(self):
        producto_válido = True  # Asume inicialmente que los datos son válidos
        
        código = self.código.get().strip()
        nombre = self.nombre.get().strip()
        precio_str = self.precio.get().strip()
        stock_str = self.stock.get().strip()
        stock_min_str = self.stock_mínimo.get().strip()

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

        # 4. Verifica que se haya ingresado un stock actual (solo si lo anterior es válido)
        if stock_str == '':
            MensajeModerno(self,'¡Atención!', 'Debe ingresar el stock actual.', tipo="advertencia")
            self.entrada_stock.focus()
            producto_válido = False

        # 5. Verifica que se haya ingresado un stock mínimo (solo si lo anterior es válido)
        if stock_min_str == '':
            MensajeModerno(self,'¡Atención!', 'Debe ingresar el stock mínimo.', tipo="advertencia")
            self.entrada_stock_mínimo.focus()
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
        self.tabla_carrito.column("nombre", anchor='w', width=290) # Columna expandible
        self.tabla_carrito.column("precio_unitario", anchor='e', width=100, stretch=tk.NO)
        self.tabla_carrito.column("cantidad", anchor='center', width=60, stretch=tk.NO)
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
        """
        Limpia la tabla de stock en alerta y la recarga con productos...
        """
        funciones_útiles.borrarTodasLasFilas(self.tabla_stock_alerta)
        
        # --- Configurar tags modernos ---
        self.tabla_stock_alerta.tag_configure('impar', background=COLOR_BLANCO)
        self.tabla_stock_alerta.tag_configure('par', background=COLOR_FONDO_APP)
        self.tabla_stock_alerta.tag_configure('alerta', foreground='red', background='#FFF0F0') # Rojo suave de fondo para alertas
        
        if not self.datos:
            return

        stock_en_alerta = self.base_de_datos.consultarProductosPorPorcentajeStock()
        
        if stock_en_alerta:
            # Usamos enumerate para saber si es par o impar
            for i, producto_alerta in enumerate(stock_en_alerta):
                
                tag_fila = 'par' if i % 2 == 0 else 'impar'
                
                # Prioridad: Si es alerta, usa el tag 'alerta', si no, usa el color alterno
                if int(producto_alerta[STOCK_ACTUAL_TABLA_ALERTA]) <= int(producto_alerta[STOCK_MÍNIMO_TABLA_ALERTA]):
                    self.tabla_stock_alerta.insert('', tk.END, values=producto_alerta, tags=('alerta',))
                else:
                    self.tabla_stock_alerta.insert('', tk.END, values=producto_alerta, tags=(tag_fila,))

    def cargarTablaProducto(self):
        """
        Carga los datos de los productos alternando colores de fila.
        """
        # Configurar los tags de color en la tabla
        self.tabla_productos.tag_configure('impar', background=COLOR_BLANCO)
        self.tabla_productos.tag_configure('par', background=COLOR_FONDO_APP)

        if self.datos:
            for i, producto in enumerate(self.datos):
                # Determinar si la fila es par o impar
                tag_fila = 'par' if i % 2 == 0 else 'impar'
                
                # Insertar con el tag correspondiente
                self.tabla_productos.insert('', tk.END, values=producto, tags=(tag_fila,))
            self.aplicarOrdenGuardado(self.tabla_productos, 'productos')

    def eliminarVenta(self):
        """
        Elimina la VENTA seleccionada de la tabla_ventas (historial).
        
        1. Pide confirmación para eliminar la venta.
        2. Si se elimina, pregunta si se desea REPONER el stock de los productos.
        3. Si responde SÍ: actualiza el stock.
        4. Finalmente elimina la venta de la BD y refresca la interfaz.
        """
        
        # 1. Verificar que una VENTA esté seleccionada (tabla izquierda)
        item_seleccionado = self.tabla_ventas.focus()
        if not item_seleccionado:
            MensajeModerno(self,"Atención", 
                                   "Debe seleccionar una Venta de la tabla de la izquierda (Historial) para poder eliminarla.",
                                   tipo="advertencia")
            
            return

        # 2. Pedir confirmación DE ELIMINACIÓN
        confirmación = MensajeModerno(self, "Confirmar Eliminación", 
                                        "¿Está seguro de que desea eliminar esta VENTA permanentemente?\n"
                                        "Esta acción no se puede deshacer.", tipo="pregunta")
        respuesta_eliminar = confirmación.resultado
        
        if respuesta_eliminar:
            try:
                # 3. Obtener el ID de la Venta
                datos = self.tabla_ventas.item(item_seleccionado)['values']
                id_venta = datos[0] # El ID es la primera columna
                
                # 4. Consultar los detalles (necesarios para saber qué reponer)
                # (Devuelve: codigo, nombre, precio_unitario, cantidad, subtotal)
                detalles = self.base_de_datos.consultarDetalleVenta(id_venta)
                
                if detalles:
                    # 5. Preguntar si se desea REPONER STOCK
                    confirmación_reponer = MensajeModerno(self, "Reponer Stock", 
                                                            "¿Desea devolver los productos al stock?\n\n"
                                                            "Sí: Se sumará la cantidad al stock actual.\n"
                                                            "No: Solo se borrará el registro de la venta.", tipo="pregunta")
                    respuesta_reponer = confirmación_reponer.resultado
                    
                    if respuesta_reponer:
                        # Hacer el bucle para reponer uno por uno
                        for item in detalles:
                            codigo = item[0]
                            cantidad = int(item[3])
                            # Llama a la función existente en tu base_de_datos.py
                            # Espera: [cantidad_repuesta, codigo_producto]
                            self.base_de_datos.reponerStockProducto([cantidad, codigo])

                # 6. Llamar a la BD para eliminar la VENTA (Siempre se hace)
                # (ON DELETE CASCADE borrará los detalles automáticamente)
                self.base_de_datos.eliminarVentaPorID([id_venta])
                
                # 7. Limpieza de la interfaz
                # Si el carrito estaba mostrando esa venta, lo vaciamos visualmente
                funciones_útiles.borrarTodasLasFilas(self.tabla_carrito)
                self.etiqueta_valor_total_produdcto.config(text="0.00")
                
                # 8. Refrescar la tabla de ventas
                self.actualizarTablaVentasEnHilo()
                
                # 9. Refrescar la tabla de productos (por si el stock cambió)
                self.datos = self.base_de_datos.consultarDatosProductos()
                
                self.cargarDatosEnTablaEnHilo() # Actualiza productos y alertas de stock
                
                MensajeModerno(self, "Éxito", "Venta eliminada correctamente.", tipo="info")

                # Resetear controles
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

        Esta función se activa cuando el usuario hace clic en una fila de la
        tabla de productos. Realiza las siguientes acciones:

        1. Verifica si hay un elemento seleccionado.
        2. Obtiene los datos del elemento seleccionado.
        3. Limpia todos los campos de entrada del labelframe de productos.
        4. Carga los datos de la fila en los widgets correspondientes (Código, Nombre, etc.).
        5. Habilita los botones "Editar", "Eliminar" y "Limpiar".
        6. Actualiza el contador de caracteres de la descripción.
        """
        
        # 1. Verifica si hay algún elemento seleccionado en la tabla de productos.
        if len(self.tabla_productos.selection()) > 0:
            
            # Obtiene el identificador del elemento seleccionado.
            item_seleccionado = self.tabla_productos.focus()
            
            if item_seleccionado:
                # 2. Obtiene los valores de la fila seleccionada.
                # El orden de 'datos' coincide con las columnas de 'crearTablaConProductos':
                # 0: código, 1: nombre, 2: precio, 3: stock_actual, 4: stock_mínimo, 5: descripción
                datos = self.tabla_productos.item(item_seleccionado)['values']

                # 3. Limpia la descripción antes de cargar nuevos datos.
                self.texto_desplazado.delete('1.0', tk.END)

                # 4. Carga los datos en los widgets de la interfaz:
                self.código.set(datos[0])
                self.nombre.set(datos[1])
                self.precio.set(datos[2])
                self.stock.set(datos[3])
                self.stock_mínimo.set(datos[4])
                self.texto_desplazado.insert('1.0', datos[5])

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

        Recopila los nuevos valores del formulario y los envía a la base de datos.
        Confía en la restricción UNIQUE de la base de datos para capturar 
        errores de código duplicado.
        """
        valores = []  # Lista para almacenar los nuevos valores del producto.
        item_seleccionado = self.tabla_productos.focus()  # Obtiene el ítem seleccionado.
        
        # 1. Verifica si hay un ítem seleccionado Y si el formulario es válido
        if item_seleccionado and self.esUnProductoVálido():
            datos = self.tabla_productos.item(item_seleccionado)['values']  # Obtiene los valores ORIGINALES.
            
            # 2. Prepara los valores para enviar a la BD
            valores.append(self.código.get().strip()) # 0: código
            valores.append(self.nombre.get().strip()) # 1: nombre
            valores.append(self.texto_desplazado.get("1.0", tk.END).strip()) # 2: desc
            valores.append(float(self.precio.get().strip()) if self.precio.get().strip() else 0) # 3: precio
            valores.append(int(self.stock.get().strip()) if self.stock.get().strip() else 0) # 4: stock
            valores.append(int(self.stock_mínimo.get().strip()) if self.stock_mínimo.get().strip() else 0) # 5: stock_min
            valores.append(datos[-1])  # 6: Agrega el id_producto (para el WHERE)

            # 3. Intenta modificar, confiando en la BD para capturar duplicados
            try:
                self.base_de_datos.modificarUnProducto(valores)  # Modifica el producto
                
                self.limpiarCamposProductos()
                self.datos = self.base_de_datos.consultarDatosProductos()  # Actualiza los datos locales.
                self.cargarDatosEnTablaEnHilo()
                funciones_útiles.crearHiloRespaldarBaseDeDatos(self.base_de_datos)
                MensajeModerno(self, "Éxito", "Producto modificado correctamente.", tipo="éxito")

            except ValueError as ve:
                # Captura el error de "Código duplicado" (1062)
                MensajeModerno(self, "Error de Duplicado", str(ve), tipo="error")
                self.entrada_código.focus() # Pone el foco en el campo incorrecto
            except Exception as e:
                # Captura cualquier otro error
                MensajeModerno(self, "Error de Base de Datos", 
                                     f"No se pudo modificar el producto: {str(e)}", tipo="error")
        elif not item_seleccionado:
            MensajeModerno(self,"Error", "Debe seleccionar un producto", tipo="advertencia")
    
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
    
    def limpiarCamposProductos(self):
        self.texto_desplazado.delete('1.0', tk.END)  # Borra el texto de la descripción.
        self.precio.set('')  # Limpia el campo de importe.
        self.entrada_stock.delete(0, "end")
        self.entrada_stock_mínimo.delete(0, "end")
        self.entrada_código.delete(0, "end")
        self.entrada_nombre.delete(0, "end")
        self.tabla_productos.selection_set(()) # Deselecciona la tabla
        self.etiqueta_contador_caracteres.config(text=str(MÁX_CAR_DESCRIP)) # actualiza la cantidad de caracteres restantes
        # cambia a verde el color de la etiqueta de los caracteres restantes
        self.etiqueta_contador_caracteres.configure(style="verde.TLabel")

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
    
    def ordenarColumna(self, tree, col, descendente, nombre_tabla=None):
        """
        Ordena una tabla (tree) por una columna (col) y guarda el estado.
        Reaplica el color de filas (cebra) después de ordenar.
        """
        # 1. Guardar el estado actual
        if nombre_tabla:
            self.estado_orden[nombre_tabla] = (col, descendente)

        # 2. Obtener la lista de tuplas
        datos = [(tree.set(k, col), k) for k in tree.get_children('')]

        # 3. Intentar ordenar
        try:
            # Eliminar símbolos de moneda ($)
            datos.sort(key=lambda t: float(t[0].replace('$', '').strip()), reverse=descendente)
        except ValueError:
            # Orden alfabético
            datos.sort(key=lambda t: t[0].lower(), reverse=descendente)

        # 4. Mover los ítems y REAPLICAR TAGS DE COLOR
        for index, (val, k) in enumerate(datos):
            tree.move(k, '', index)
            
            # --- NUEVO: Recalcular par/impar ---
            tag_fila = 'par' if index % 2 == 0 else 'impar'
            
            # Mantenemos el tag 'alerta' si ya lo tenía (para la tabla de stock)
            tags_actuales = list(tree.item(k, 'tags'))
            if 'alerta' in tags_actuales:
                # Si es alerta, forzamos 'alerta' (que tiene fondo rojo)
                tree.item(k, tags=('alerta',))
            else:
                # Si no, aplicamos el color alterno
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