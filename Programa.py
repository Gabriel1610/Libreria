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

        # --- Nombre ---
        self.etiqueta_nombre = ttk.Label(self.labelframe_productos, text=ETIQUETA_NOMBRE_TEXTO_PRODUCTOS)
        self.etiqueta_nombre.grid(column=0, row=0, 
                                padx=PADX_ETIQUETA_NOMBRE_PRODUCTOS, 
                                pady=PADY_ETIQUETA_NOMBRE_PRODUCTOS, 
                                sticky=STICKY_WIDGET_OESTE_PRODUCTOS)
        self.nombre = tk.StringVar()
        self.entrada_nombre = tk.Entry(self.labelframe_productos, 
                                    width=ANCHO_ENTRADA_NOMBRE_PRODUCTOS, 
                                    textvariable=self.nombre)
        self.entrada_nombre.grid(column=0, row=0, 
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

        # Bindeo con la constante de evento
        self.entrada_precio.bind(EVENTO_TECLA_PRESIONADA, 
                                lambda event: funciones_útiles.controlar_caracteres_precio(self.precio, self.entrada_precio, event))  # Validación de entrada

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