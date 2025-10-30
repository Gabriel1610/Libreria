import tkinter as tk
import os
from tkinter import messagebox
import sys
import base_de_datos
import math
from tkinter import ttk, filedialog
from tkinter import scrolledtext as st
from tkinter import messagebox
from datetime import date, datetime
from tkcalendar import Calendar
from argendolar import Argendolar, TipoDivisas
from VentanaCierre import VentanaCierre
import threading
import queue
import time
import logging
import functools
import sys
from funciones_útiles import FORMATO_PREFERIDO_FECHA, FORMATO_FECHA_BD, FORMATO_FECHA_CALENDAR, FORMATO_PREFERIDO_HORA_Y_FECHA
import funciones_útiles
import validación_tipo_de_datos

NOMBRE_ICONO = "librería.ico"
TAMAÑO_MÍNIMO_COLUMNA1_CPM = 620
TIEMPO_A_ESPERAR_MÁXIMO = 5

# --- Constantes para la UI de Productos ---

# Textos de etiquetas
TÍTULO_LABELFRAME_PRODUCTOS = 'Agregación, edición, control y eliminación de productos'
ETIQUETA_NOMBRE_TEXTO_PRODUCTOS = "Nombre:"
ETIQUETA_PRECIO_TEXTO_PRODUCTOS = "Precio: $ "

# Fuentes
FUENTE_TÍTULO_PRODUCTOS = ('Times New Roman', 15, 'bold')

# Parámetros de layout (Grid)
STICKY_LABELFRAME_PRODUCTOS = "nw"
STICKY_WIDGET_OESTE_PRODUCTOS = "w"

PADX_ETIQUETA_NOMBRE_PRODUCTOS = 0
PADY_ETIQUETA_NOMBRE_PRODUCTOS = 0  # Padding específico para la etiqueta nombre
PADX_ENTRADA_IZQUIERDA_NOMBRE_PRODUCTOS = (50, 0)

PADX_ETIQUETA_PRECIO_PRODUCTOS = 0
PADY_ETIQUETA_PRECIO_PRODUCTOS = 0  # Padding específico para la etiqueta precio
PADX_ENTRADA_IZQUIERDA_PRECIO_PRODUCTOS = (50, 0)

PADX_ETIQUETA_STOCK_ACTUAL_PRODUCTOS = 0
PADY_ETIQUETA_STOCK_ACTUAL_PRODUCTOS = 0  # Padding específico para la etiqueta stock

PADX_ENTRADA_IZQUIERDA_STOCK_ACTUAL_PRODUCTOS = (73, 0)
PADY_WIDGETS_GENERAL_PRODUCTOS = 5   # Padding vertical para la mayoría de widgets

ANCHO_ENTRADA_NOMBRE_PRODUCTOS = 40
ANCHO_ENTRADA_PRECIO_PRODUCTOS = 15

ETIQUETA_STOCK_ACTUAL_TEXTO_PRODUCTOS = "Stock actual:"
ANCHO_ENTRADA_STOCK_ACTUAL_PRODUCTOS = 10 #

ETIQUETA_STOCK_MÍNIMO_TEXTO_PRODUCTOS = "Stock mínimo:"
ANCHO_ENTRADA_STOCK_MÍNIMO_PRODUCTOS = 10

PADX_ETIQUETA_STOCK_MÍNIMO_PRODUCTOS = 0
PADY_ETIQUETA_STOCK_MÍNIMO_PRODUCTOS = 0  # Padding específico para la etiqueta stock mínimo
PADX_ENTRADA_IZQUIERDA_STOCK_MÍNIMO_PRODUCTOS = (82, 0)

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

# (Constantes anteriores...)

# --- Constantes para Botones de Productos ---
TEXTO_BOTÓN_AÑADIR_PRODUCTOS = "Añadir"
TEXTO_BOTÓN_EDITAR_PRODUCTOS = "Editar"
TEXTO_BOTÓN_ELIMINAR_PRODUCTOS = "Eliminar"
TEXTO_BOTÓN_LIMPIAR_PRODUCTOS = "Limpiar"

# Padding (horizontal) para los botones en la fila 6.
# Ajusta estos valores numéricos (85, 170, 255)
# para que coincidan con el espaciado que deseas.
PADX_BOTÓN_AÑADIR_PRODUCTOS = (0, 0)
PADX_BOTÓN_EDITAR_PRODUCTOS = (85, 0)
PADX_BOTÓN_ELIMINAR_PRODUCTOS = (170, 0)
PADX_BOTÓN_LIMPIAR_PRODUCTOS = (255, 0)

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

        # --- Inicialización de variables y objetos ---
            self.base_de_datos = base_de_datos.BaseDeDatos()  # Crea una instancia de la clase BaseDeDatos.
            self.hilos = []  # Lista para almacenar los hilos que se creen.
            self.evento_cancelar = threading.Event()  # Evento para cancelar hilos.
        
        #Crea un widget Notebook, que permite tener varias pestañas
            self.cuaderno = ttk.Notebook(self)  
            
            #Crea la primera página del cuaderno (pestaña "Productos").
            self.página_cuaderno_productos = ttk.Frame(self.cuaderno)

            self.página_cuaderno_productos.grid_columnconfigure(0, weight=1)
            self.página_cuaderno_productos.grid_columnconfigure(1, weight=0)

            self.página_cuaderno_productos.grid_rowconfigure(0, weight=1)

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

             # --- Configuración de estilos ---
            self.estilo_apariencia = ttk.Style()  # Crea un objeto de estilo para personalizar la apariencia.
            self.estilo_apariencia.configure("rojo.TLabel", foreground="red")  # Estilo para texto rojo.
            self.estilo_apariencia.configure("verde.TLabel", foreground="#37C11E")  # Estilo para texto verde.
            self.estilo_apariencia.configure("negro.TLabel", foreground="black")  # Estilo para texto negro.

            # Crea la página de "Ventas" dentro del cuaderno de productos.
            self.página_cuaderno_ventas = ttk.Frame(self.cuaderno)
            self.cuaderno.add(self.página_cuaderno_ventas, text="Ventas")

            # Guarda los índices de las pestañas de "Productos" y "Ventas" para usarlos luego.
            self.índice_productos = self.cuaderno.index(self.página_cuaderno_productos)
            self.índice_ventas = self.cuaderno.index(self.página_cuaderno_ventas)

            # Posiciona el cuaderno (con las pestañas) en la ventana principal.
            self.cuaderno.grid(column=0, row=0, sticky="nsew")

            # Llama a los métodos para crear los diferentes elementos de la interfaz:
            self.crearTablaConProductos()  # Crea la tabla principal.
            self.crearLabelFrameProductos() # Crea el LabelFrame para agregar productos.

            # Configura la función que se ejecutará cuando se cierre la ventana.
            self.protocol("WM_DELETE_WINDOW", self.cerrarVentana)

        except Exception as e:
            messagebox.showerror("Error crítico", f"Fallo en inicialización: {str(e)}")
            sys.exit(1)
    
    def crearTablaConProductos(self):

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
            height=14
        )

        self.tabla_productos.heading('código', text='Código')
        self.tabla_productos.heading('nombre', text='Nombre')
        self.tabla_productos.heading('precio', text='Precio')
        self.tabla_productos.heading('stock_actual', text='Stock actual')
        self.tabla_productos.heading('stock_mínimo', text='Stock mínimo')
        self.tabla_productos.heading('descripción', text='Descripción', anchor='w')

        self.tabla_productos.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky='ns'
        )

        self.tabla_productos.column(
            "código",
            anchor='center',
            width=150,
            minwidth=150,
            stretch=tk.NO
        )
        self.tabla_productos.column(
            "nombre",
            anchor='center',
            width=200,
            minwidth=200,
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

        self.barra_desplazamiento_vertical.grid(row=0, column=2, sticky='ns')
        self.barra_desplazamiento_horizontal.grid(row=1, column=0, columnspan=2, sticky='we')

        # self.tabla_productos.bind("<<TreeviewSelect>>", self.cargarRegistros)
    
    def crearLabelFrameProductos(self):
        # --- Creación de Widgets ---

        self.etiqueta_título_labelframe_productos = tk.Label(self.página_cuaderno_productos, 
                                                        text=TÍTULO_LABELFRAME_PRODUCTOS, 
                                                        font=FUENTE_TÍTULO_PRODUCTOS)
        self.labelframe_productos = ttk.LabelFrame(self.página_cuaderno_productos, 
                                                labelwidget=self.etiqueta_título_labelframe_productos)

        self.labelframe_productos.grid(column=0, row=2, rowspan=2, 
                                    padx=PADX_ETIQUETA_NOMBRE_PRODUCTOS, 
                                    pady=PADY_ETIQUETA_NOMBRE_PRODUCTOS,
                                    sticky=STICKY_LABELFRAME_PRODUCTOS)

        # --- CÓDIGO (NUEVO) --- (Fila 0)
        self.etiqueta_código = ttk.Label(self.labelframe_productos, text=ETIQUETA_CÓDIGO_TEXTO_PRODUCTOS)
        self.etiqueta_código.grid(column=0, row=0, 
                                padx=PADX_ETIQUETA_CÓDIGO_PRODUCTOS, 
                                pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        self.código = tk.StringVar()
        self.entrada_código = tk.Entry(self.labelframe_productos, 
                                    width=ANCHO_ENTRADA_CÓDIGO_PRODUCTOS, 
                                    textvariable=self.código)
        self.entrada_código.grid(column=0, row=0, 
                                padx=PADX_ENTRADA_IZQUIERDA_CÓDIGO_PRODUCTOS, 
                                pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)

        # --- Nombre ---
        self.etiqueta_nombre = ttk.Label(self.labelframe_productos, text=ETIQUETA_NOMBRE_TEXTO_PRODUCTOS)
        self.etiqueta_nombre.grid(column=0, row=1, 
                                padx=PADX_ETIQUETA_NOMBRE_PRODUCTOS, 
                                pady=PADY_ETIQUETA_NOMBRE_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        self.nombre = tk.StringVar()
        self.entrada_nombre = tk.Entry(self.labelframe_productos, 
                                    width=ANCHO_ENTRADA_NOMBRE_PRODUCTOS, 
                                    textvariable=self.nombre)
        self.entrada_nombre.grid(column=0, row=1, 
                                padx=PADX_ENTRADA_IZQUIERDA_NOMBRE_PRODUCTOS, 
                                pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)

        # --- Precio ---
        self.etiqueta_precio = ttk.Label(self.labelframe_productos, text=ETIQUETA_PRECIO_TEXTO_PRODUCTOS)
        self.etiqueta_precio.grid(column=0, row=2, 
                                padx=PADX_ETIQUETA_PRECIO_PRODUCTOS, 
                                pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        self.precio = tk.StringVar()
        self.entrada_precio = tk.Entry(self.labelframe_productos, 
                                    width=ANCHO_ENTRADA_PRECIO_PRODUCTOS, 
                                    textvariable=self.precio)
        self.entrada_precio.grid(column=0, row=2, 
                                padx=PADX_ENTRADA_IZQUIERDA_PRECIO_PRODUCTOS, 
                                pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)

        # Bindeo con la constante de evento
        self.entrada_precio.bind(EVENTO_TECLA_PRESIONADA, 
                                lambda event: funciones_útiles.controlar_caracteres_precio(self.precio, self.entrada_precio, event))  # Validación de entrada

        # --- Stock Actual ---
        self.etiqueta_stock = ttk.Label(self.labelframe_productos, text=ETIQUETA_STOCK_ACTUAL_TEXTO_PRODUCTOS)
        self.etiqueta_stock.grid(column=0, row=3,
                                padx=PADX_ETIQUETA_STOCK_ACTUAL_PRODUCTOS, 
                                pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        self.stock = tk.StringVar()
        self.entrada_stock = tk.Entry(self.labelframe_productos, 
                                    width=ANCHO_ENTRADA_STOCK_ACTUAL_PRODUCTOS, 
                                    textvariable=self.stock)
        self.entrada_stock.grid(column=0, row=3,
                                padx=PADX_ENTRADA_IZQUIERDA_STOCK_ACTUAL_PRODUCTOS, 
                                pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)

        self.entrada_stock.bind(EVENTO_TECLA_PRESIONADA, self.controlar_caracteres_stock)

        # --- Stock Mínimo ---
        self.etiqueta_stock_mínimo = ttk.Label(self.labelframe_productos, text=ETIQUETA_STOCK_MÍNIMO_TEXTO_PRODUCTOS)
        self.etiqueta_stock_mínimo.grid(column=0, row=4,
                                        padx=PADX_ETIQUETA_STOCK_MÍNIMO_PRODUCTOS, 
                                        pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                        sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        self.stock_mínimo = tk.StringVar()
        self.entrada_stock_mínimo = tk.Entry(self.labelframe_productos, 
                                            width=ANCHO_ENTRADA_STOCK_MÍNIMO_PRODUCTOS, 
                                            textvariable=self.stock_mínimo)
        self.entrada_stock_mínimo.grid(column=0, row=4,
                                        padx=PADX_ENTRADA_IZQUIERDA_STOCK_MÍNIMO_PRODUCTOS, 
                                        pady=PADY_WIDGETS_GENERAL_PRODUCTOS, 
                                        sticky=STICKY_WIDGET_OESTE_PRODUCTOS)

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
                                                wrap=WRAP_TEXTO_DESCRIPCIÓN_PRODUCTOS)

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

    def añadirProducto(self):
        if self.esUnProductoVálido():  # Verifica si los datos ingresados son válidos.
            nombre = self.nombre.get()  # Obtiene el nombre del producto.
            precio = float(self.precio.get())  # Obtiene el precio como float.
            categoria = self.categoria.get()  # Obtiene la categoría.
            stock = int(self.stock.get())  # Obtiene el stock como entero.
            es_deuda = self.tipo_movimiento.get() % 2  # Determina si es deuda (1) o haber (0).
            medio = self.medio.get()  # Obtiene el medio de pago.
            cantidad_de_cuotas = 1  # Valor por defecto para la cantidad de cuotas.
            if self.cant_cuotas.get() != '':  # Si se especificó la cantidad de cuotas...
                cantidad_de_cuotas = int(self.cant_cuotas.get())  # ...la obtiene como entero.
            la_descripción = self.texto_desplazado.get("1.0", tk.END).rstrip('\n')  # Obtiene la descripción.
            # Crea una lista con los datos del nuevo movimiento.
            movimiento = [
                fecha_string,
                importe,
                es_deuda,
                en_dólares,
                medio,
                la_descripción,
                cantidad_de_cuotas
            ]
            # Llama a la función para ingresar el movimiento en la base de datos.
            self.base_de_datos.ingresarMovimiento(movimiento)
            # Actualiza la interfaz (limpia campos, recarga tabla, recalcula deuda) y respalda la BD.
            self.actualizarEstadoYRespaldar()
            if medio != 'Efectivo':
                self.cargarDatosEnTablaTarjetasEnHilo()

    def esUnProductoVálido(self):
        añadir_producto = True  # Asume inicialmente que los datos son válidos.

        # Verifica que se haya ingresado la cantidad de cuotas, si el campo está habilitado.
        if self.cant_cuotas.get() == '' and not self.entrada_cantidad_cuotas['state'] == 'disabled':
            messagebox.showwarning('¡Atención!', 'Debe añadir la cantidad de cuotas')
            añadir_producto = False

        # Verifica que se haya ingresado un importe y que sea un número decimal válido.
        if self.importe.get() == '':
            messagebox.showwarning('¡Atención!', 'Se olvidó de ingresar el importe')
            añadir_producto = False

        return añadir_producto  # Devuelve True si todas las validaciones fueron exitosas, False si alguna falló.
    
    def editarProducto(self):
        """
        Edita un movimiento existente en la base de datos si la entrada es válida.

        Esta función se ejecuta cuando el usuario hace clic en el botón "Editar".
        Realiza las siguientes acciones:

        1. Obtiene el ítem seleccionado de la tabla de movimientos.
        2. Verifica si hay un ítem seleccionado y si los datos ingresados son válidos llamando a 'esUnMovimientoVálido()'.
        3. Si se cumplen ambas condiciones:
           - Obtiene la fecha del calendario y la formatea como 'YYYY-MM-DD'.
           - Crea una lista 'valores' para almacenar los nuevos valores del movimiento.
           - Agrega la fecha formateada a la lista 'valores'.
           - Agrega el importe a la lista 'valores'.
           - Determina si el movimiento es en dólares (1) o pesos (0) y lo agrega a 'valores'.
           - Determina si es deuda (1) o haber (0) y lo agrega a 'valores'.
           - Agrega el medio de pago a 'valores'.
           - Agrega la descripción (eliminando saltos de línea al final) a 'valores'.
           - Obtiene la cantidad de cuotas (por defecto es 1 si no se especifica) y la agrega a 'valores'.
           - Agrega el código único del movimiento original (obtenido de 'datos[ÍNDICE_CÓD_MOV]') a 'valores'.  Esto es crucial
             para identificar el movimiento que se va a editar.
           - Llama a 'modificarUnMovimiento' en la base de datos para actualizar el movimiento.
           - Finalmente, actualiza el estado de la interfaz y respalda la base de datos.
        
        valores = []  # Lista para almacenar los nuevos valores del movimiento.
        item_seleccionado = self.tabla_movimientos.focus()  # Obtiene el ítem seleccionado.
        datos = self.tabla_movimientos.item(item_seleccionado)['values']  # Obtiene los valores del ítem.
        if item_seleccionado and self.esUnMovimientoVálido():  # Verifica selección y validez.
            fecha_date = datetime.strptime(self.calendario_fecha.get_date(), FORMATO_FECHA_CALENDAR).date()  # Obtiene la fecha.
            fecha = fecha_date.strftime(FORMATO_FECHA_BD)  # Formatea la fecha.
            valores.append(fecha)  # Agrega la fecha a la lista de valores.
            valores.append(self.importe.get())  # Agrega el importe.
            valores.append(0)  # Valor por defecto para 'en_dólares'.
            if self.tipo_moneda.get() == 2:  # Si es en dólares...
                valores[-1] = 1  # ...cambia el valor a 1.
            valores.append(1)  # Valor por defecto para 'es_deuda'.
            if self.tipo_movimiento.get() == 2:  # Si es haber...
                valores[-1] = 0  # ...cambia el valor a 0.
            medio_pago = self.medio.get()  # Obtiene el medio de pago.
            valores.append(medio_pago)  # Agrega el medio de pago.
            valores.append(self.texto_desplazado.get('1.0', tk.END).rstrip())  # Agrega la descripción.
            cuotas_totales = 1  # Valor por defecto para cuotas totales.
            cuotas_totales_cuadro_texto = self.cant_cuotas.get()  # Obtiene cuotas del cuadro de texto.
            if cuotas_totales_cuadro_texto != '':  # Si se especificó un valor...
                cuotas_totales = int(cuotas_totales_cuadro_texto)  # ...lo usa.
            # else:  # Este 'else' es redundante, ya que cuotas_totales ya tiene el valor por defecto.
            #     cuotas_totales = 1
            valores.append(cuotas_totales)  # Agrega la cantidad de cuotas.
            valores.append(datos[ÍNDICE_CÓD_MOV_TABLA])  # Agrega el código único del movimiento original.
            self.base_de_datos.modificarUnMovimiento(valores)  # Modifica el movimiento en la base de datos.
            # Actualiza la interfaz (limpia campos, recarga tabla, recalcula deuda) y respalda la BD.
            self.actualizarEstadoYRespaldar()
            self.cargarDatosEnTablaEnHilo()
            self.cargarDatosEnTablaTarjetasEnHilo()"""

    def eliminarProducto(self):
        """
        Elimina el movimiento seleccionado de la base de datos y actualiza la interfaz.

        Esta función se ejecuta cuando el usuario hace clic en el botón "Eliminar".
        Realiza las siguientes acciones:

        1. Obtiene el ítem seleccionado de la tabla de movimientos.
        2. Si hay un ítem seleccionado:
           - Extrae los datos del ítem, incluyendo su código único (que está en la posición 9 de la lista 'values').
           - Llama a la función 'eliminarMovimientoPorCódigo' de la base de datos para eliminar el movimiento.
           - Llama a la función 'limpiar' para limpiar los campos de entrada.
           - Llama a la función 'crearHiloRespaldarBaseDeDatos' para crear un hilo que respalde la base de datos.
           - Establece 'self.cambiar_deuda_dólar' en 'True' para indicar que la deuda en dólares debe ser recalculada.
           - Llama a 'self.actualizarAdvertenciaDeActualizaciónDeDeuda' para actualizar la advertencia sobre la actualización del precio del dólar
           y que así el usuario sepa que el monto que está viendo puede no ser el real y presione en "Calcular" si quiere ver el verdadero.
           - Llama a 'self.cargarDatosEnTablaEnHilo' para recargar los datos en la tabla (en un hilo separado).
        
        item_seleccionado = self.tabla_movimientos.focus()  # Obtiene el ítem seleccionado de la tabla.
        datos = self.tabla_movimientos.item(item_seleccionado)['values'] #Obtiene los valores del item seleccionado
        if item_seleccionado:  # Verifica si hay un ítem seleccionado.
            self.base_de_datos.eliminarMovimientoPorCódigo([datos[ÍNDICE_CÓD_MOV_TABLA]]) # Elimina el movimiento de la base de datos.
            self.limpiar()  # Limpia los campos de entrada.
            funciones_útiles.crearHiloRespaldarBaseDeDatos(self.base_de_datos)  # Respalda la base de datos (en un hilo).
            self.cambiar_deuda_dólar = True  # Indica que se debe recalcular la deuda en dólares.
            self.actualizarAdvertenciaDeActualizaciónDeDeuda()  # Actualiza la advertencia sobre el precio del dólar.
            self.cargarDatosEnTablaEnHilo()  # Recarga los datos en la tabla (en un hilo).
            if datos[ÍNDICE_NOMBRE_MEDIO_PAGO_TABLA] != 'Efectivo':
                self.cargarDatosEnTablaTarjetasEnHilo()"""
    
    def limpiarCamposProductos(self):
        self.texto_desplazado.delete('1.0', tk.END)  # Borra el texto de la descripción.
        self.precio.set('')  # Limpia el campo de importe.
        self.entrada_stock.delete(0, "end")
        self.botón_editar_productos.config(state='disabled')  # Deshabilita el botón "Editar".
        self.botón_eliminar_productos.config(state='disabled')  # Deshabilita el botón "Eliminar".
        self.botón_limpiar_productos.config(state="disabled")  # Deshabilita el botón "Limpiar".
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
                self.botón_añadir_a_favoritos.config(state = 'disabled') #Deshabilita el botón de añadir a favoritos
            if nuevo_valor < 0:  # Si el valor es negativo.
                nuevo_valor = 0  # Establece en 0.
                self.texto_desplazado.delete("1.0", tk.END)  # Borra todo el contenido.
                self.texto_desplazado.insert("1.0", contenido_después[:MÁX_CAR_DESCRIP])  # Inserta el contenido truncado.

            self.etiqueta_contador_caracteres.config(text=str(nuevo_valor))  # Actualiza el contador en la interfaz.

            # Actualizar color
            if nuevo_valor <= ADVERTENCIA_CANT_CAR_DESCRIP:  # Si está por debajo del umbral de advertencia.
                self.etiqueta_contador_caracteres.configure(style="rojo.TLabel")  # Cambia el color a rojo.
                if nuevo_valor <= 0:  # Si llega a 0.
                    messagebox.showwarning("Advertencia", "Ha alcanzado el límite de caracteres.")  # Muestra advertencia.
            else:  # Si está por encima o igual al umbral de advertencia.
                self.etiqueta_contador_caracteres.configure(style="verde.TLabel")  # Cambia el color a verde.

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
            self.botón_añadir_a_favoritos.config(state = 'normal') #Habilita el botón de añadir a favoritos
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
    
    def controlar_caracteres_stock(self, event = None):
        retornar = "break"  # Valor por defecto: evita la inserción del carácter.
        carácter = event.char  # Obtiene el carácter individual ingresado.
        tecla = event.keysym.lower()  # Obtiene la tecla presionada (en minúsculas).

        # Permite dígitos, teclas de navegación/edición y combinaciones Ctrl+X/C/V.
        if carácter and carácter in '123456789':
            retornar = None  # Permite dígitos.
        elif (event and (event.keysym == 'BackSpace' or event.keysym.startswith('Shift') or \
                         event.keysym in ('Delete', 'Home', 'End', 'Up', 'Down', 'Left', 'Right'))) or \
             (event.state & 0x0004 and tecla in ['x', 'v', 'c']):

            # Maneja el pegado (Ctrl+V).
            if event.state & 0x0004 and tecla == 'v':
                contenido_antes = self.cant_cuotas.get()  # Guarda el contenido actual.
                posición_cursor_antes = self.entrada_cantidad_cuotas.index("insert")  # Guarda la posición del cursor.
                retornar = None  # Permite la inserción (temporalmente).

                # Define una función para actualizar el contenido después del pegado.
                def actualizar_contenido():
                    """
                    Valida y corrige el contenido después de un evento de pegado.
                    Se asegura que el contenido sea un entero. Si no lo es,
                    revierte al contenido anterior y reposiciona el cursor.
                    """
                    contenido_después = self.cant_cuotas.get()  # Obtiene el contenido después del pegado.
                    es_entero_natural = validación_tipo_de_datos.esEntero(contenido_después)
                    if not es_entero_natural:  # Si el contenido no es un entero válido.
                        self.cant_cuotas.set(contenido_antes)  # Restaura el contenido anterior.
                        self.entrada_cantidad_cuotas.icursor(posición_cursor_antes)  # Restaura la posición.

                # Ejecuta 'actualizar_contenido' después de que Tkinter termine de procesar el evento.
                self.entrada_cantidad_cuotas.after_idle(actualizar_contenido)
            else:
                retornar = None  # Permite otras teclas permitidas (Ctrl+X/C, navegación, etc.).
        return retornar  # Retorna "break" si el carácter no es válido, None si es válido.
    
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
    

# --- Necesitas esta parte para ejecutar la aplicación ---
if __name__ == "__main__":
    app = Aplicación()
    app.mainloop()