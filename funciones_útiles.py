import validación_tipo_de_datos
from datetime import datetime, date
import Limpiar_pantalla_y_pausar
import os
import requests
from tkinter import ttk
import tkinter as tk
import threading
import socket
import platform

POS_ONEDRIVE_NOTEBOOK_POSADAS = 'D:/'
POS_ONEDRIVE_NOTEBOOK_RESISTENCIA = 'C:/Users/Gabriel/'
DISCO_PORTÁTIL = 'E:\\'
NOMBRE_EQUIPO_POSADAS = 'NOTEBOOK-POSADAS'
NOMBRE_CARPETA_RESPALDO_BASE_DE_DATOS = 'OneDrive/Computadora/Documents/Programas/Deuda con interfaz/Respaldo de la base de datos'
NOMBRE_CARPETA_RESPALDO_BASE_DE_DATOS_PRUEBA = 'OneDrive/Computadora/Documents/Programas/Deuda con interfaz/Respaldo base de datos prueba'
RESPALDAR = True
FORMATO_PREFERIDO_FECHA = '%d/%m/%Y'
FORMATO_FECHA_BD = '%Y-%m-%d'
FORMATO_FECHA_CALENDAR = '%d/%m/%y'
FORMATO_PREFERIDO_HORA_Y_FECHA = '%H:%M:%S %d/%m/%Y'

def obtenerNúmeroEnteroNaturalConMáximo(mínimo, máximo, primer_mensaje, mensaje_error_tipo_dato, mensaje_error_en_rango):
    valor = input(primer_mensaje)
    controlar = True
    while controlar:
        if not validación_tipo_de_datos.esEntero(valor):
            print(mensaje_error_tipo_dato, end = "")
            valor = input()
        elif int(valor) < mínimo or int(valor) > máximo:
            print(mensaje_error_en_rango, end = "")
            valor = input()
        else:
            valor = int(valor)
            controlar = False
    return valor

def obtenerNúmeroEnteroNatural(mínimo, primer_mensaje, mensaje_error_tipo_dato, mensaje_error_en_rango):
    valor = input(primer_mensaje)
    controlar = True
    while controlar:
        if not validación_tipo_de_datos.esEntero(valor):
            print(mensaje_error_tipo_dato, end = "")
            valor = input()
        elif int(valor) < mínimo:
            print(mensaje_error_en_rango, end = "")
            valor = input()
        else:
            valor = int(valor)
            controlar = False
    return valor

def esNúmeroDecimalConXDecimales(número, cant_decimales):
    es_decimal = validación_tipo_de_datos.esEntero(número)
    if not es_decimal:
        es_decimal = validación_tipo_de_datos.esDecimal(número)
        if es_decimal:
            if len(número) > cant_decimales + 1:
                parte = número[-cant_decimales - 1:]
                if "." not in parte:
                    es_decimal = False
    return es_decimal

def obtenerNombreEquipo():
    # Preferencia: socket (portátil)
    nombre = socket.gethostname()
    if not nombre:
        # Caída a platform
        nombre = platform.node()
        if not nombre:
            # Último recurso (Windows)
            nombre = os.environ.get("COMPUTERNAME")
    return nombre

def obtenerUbicaciónNotebook():
    nombre_notebook_actual = obtenerNombreEquipo()
    en_resistencia = nombre_notebook_actual != NOMBRE_EQUIPO_POSADAS
    if en_resistencia:
        ubicación_en_notebook = POS_ONEDRIVE_NOTEBOOK_RESISTENCIA
    else:
        ubicación_en_notebook = POS_ONEDRIVE_NOTEBOOK_POSADAS
    return ubicación_en_notebook

def chequearConexiónAInternet():
    try:
        requests.get('https://www.google.com', timeout=1)
        return True
    except requests.exceptions.RequestException as e:
        return False

def obtenerNúmeroDecimal(mínimo, incluir_mínimo, primer_mensaje, mensaje_error_tipo_dato, mensaje_error_en_rango):
    valor = input(primer_mensaje)
    controlar = True
    while controlar:
        if not validación_tipo_de_datos.esDecimal(valor):
            print(mensaje_error_tipo_dato, end = "")
            valor = input()
        elif float(valor) < mínimo or float(valor) == mínimo and not incluir_mínimo:
            print(mensaje_error_en_rango, end = "")
            valor = input()
        else:
            valor = float(valor)
            controlar = False
    return valor

def preguntarSíONo(pregunta):
    print(pregunta, " (S/N): ", sep = "", end = "")
    respuesta = input().upper()
    while respuesta != 'S' and respuesta != 'N':
        respuesta = input("Ha ingresado una respuesta no válida. Vuelva a intentarlo: ").upper()
    return respuesta

def enumerarOpciones(mensaje, lista_opciones, obligatorio_elegir_una):
    print(mensaje + "\n")
    cant_opciones = len(lista_opciones)
    for x in range(len(lista_opciones)):
        print(x + 1, "_ ", lista_opciones[x], sep = "")
    if not obligatorio_elegir_una:
        print(len(lista_opciones) + 1, "_ Ninguna de las anteriores.", sep = "")
        cant_opciones += 1
    opción_elegida = obtenerNúmeroEnteroNaturalConMáximo(1, cant_opciones, "\nElija una de las opciones: ", "Lo ingresado no es una opción. Las opciones son números enteros. Inténtelo nuevamente: ", "La opción ingresada no es válida. Vuelva a intentarlo: ")
    return opción_elegida

def obtenerNombreMes(mes):
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    return meses[mes - 1]

def preguntarAño(primer_año):
    respuesta_año = preguntarSíONo("¿Se trata de este año?")
    if respuesta_año == 'N':
        Limpiar_pantalla_y_pausar.limpiarPantalla()
        año = obtenerNúmeroEnteroNaturalConMáximo(primer_año, date.today().year, "Ingrese el año del que quiere saber las estadísticas: ", "Debe ingresar un número para referirse al año. Inténtelo nuevamente: ", "No se ha registrado estadística para ese año. Ingrese otro: ")
    else:
        año = date.today().year
    return año

def traducirAbreviaturaMesEspAIng(mes):
    traducción = ''
    meses = {
        'Ene': 'Jan', 'Feb': 'Feb', 'Mar': 'Mar', 'Abr': 'Apr', 'May': 'May', 'Jun': 'Jun',
        'Jul': 'Jul', 'Ago': 'Aug', 'Sep': 'Sep', 'Oct': 'Oct', 'Nov': 'Nov', 'Dic': 'Dec'
    }
    if mes.capitalize() in meses.keys():
        traducción = meses[mes.capitalize()]
    return traducción


def obtenerNúmeroMes(mes):
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    número_mes = -1
    x = 0
    while número_mes == -1 and x < len(meses):
        if meses[x] == mes.lower():
            número_mes = x + 1
        else:
            x += 1
    return número_mes

def obtenerDíasDeUnMes(mes, año):
    cantidad_días = 31
    if mes % 2 == 0 and mes < 7 and mes != 2 or mes % 2 != 0 and mes > 7:
        cantidad_días = 30
    elif mes == 2 and (año % 4 == 0 and año % 100 != 0 or año % 400 == 0):
        cantidad_días = 29
    elif mes == 2:
        cantidad_días = 28
    return cantidad_días

def solicitarUnaFecha(mensaje, se_vale_fecha_del_futuro, solo_fecha_del_futuro):
    fecha_válida = False
    fecha = input(mensaje)
    while not fecha_válida:
        no_es_una_fecha = False
        fecha_inexistente = False
        fecha_del_futuro = False
        fecha_del_pasado_o_presente = False
        if len(fecha) == 10:
            x = 0
            fecha_válida = True
            while x < 10 and fecha_válida:
                if (x == 2 or x == 5) and fecha[x] != '/' or x != 2 and x != 5 and not validación_tipo_de_datos.esEntero(fecha[x]):
                    no_es_una_fecha = True
                    fecha_válida = False
                else:
                    x += 1
            if fecha_válida:
                día = int(fecha[:2])
                mes = int(fecha[3:5])
                año = int(fecha[-4:])
                if día > 31 or día < 1 or mes < 1 or mes > 12 or día == 31 and (mes % 2 == 0 and mes < 7 or mes % 2 != 0 and mes > 7) or día == 30 and mes == 2 or día == 29 and mes == 2 and not (año % 4 == 0 and año % 100 != 0 or año % 400 == 0):
                    fecha_inexistente = True
                    fecha_válida = False
                if not se_vale_fecha_del_futuro:
                    if año > date.today().year or año == date.today().year and mes > date.today().month or año == date.today().year and mes == date.today().month and día > date.today().day:
                        fecha_del_futuro = True
                        fecha_válida = False
                elif solo_fecha_del_futuro:
                    if año < date.today().year or año == date.today().year and mes < date.today().month or año == date.today().year and mes == date.today().month and día <= date.today().day:
                        fecha_del_pasado_o_presente = True
                        fecha_válida = False
        else:
            no_es_una_fecha = True
        if no_es_una_fecha:
            Limpiar_pantalla_y_pausar.limpiarPantalla()
            fecha = input("No ha ingresado una fecha. Ingrese una respetando este formato dd/mm/AAAA: ")
        elif fecha_del_futuro and not se_vale_fecha_del_futuro:
            Limpiar_pantalla_y_pausar.limpiarPantalla()
            fecha = input("La fecha ingresada es del futuro y por tanto no es válida. Inténtelo nuevamente: ")
        elif fecha_inexistente:
            Limpiar_pantalla_y_pausar.limpiarPantalla()
            fecha = input("No existe el " + fecha + ". Revise la fecha e inténtelo nuevamente: ")
        elif fecha_del_pasado_o_presente and solo_fecha_del_futuro:
            Limpiar_pantalla_y_pausar.limpiarPantalla()
            fecha = input("La fecha ingresada es del pasado o presente y por tanto no es válida. Inténtelo nuevamente: ")
        elif len(fecha) == 10:
            fecha_válida = True
    return datetime.strptime(fecha, FORMATO_PREFERIDO_FECHA).date()

def crearHiloRespaldarBaseDeDatos(base_de_datos):
        hilo = threading.Thread(target=respaldarBaseDeDatos, args = (base_de_datos,), daemon=True)
        hilo.start()
    
def respaldarBaseDeDatos(base_de_datos):
    ubicación_notebook = obtenerUbicaciónNotebook()
    if RESPALDAR:
        base_de_datos.respaldarBaseDeDatos(ubicación_notebook + NOMBRE_CARPETA_RESPALDO_BASE_DE_DATOS)
    else:
        base_de_datos.respaldarBaseDeDatos(ubicación_notebook + NOMBRE_CARPETA_RESPALDO_BASE_DE_DATOS_PRUEBA)

def controlar_caracteres_precio(importe, entrada_importe, event=None):
    """
    Controla los caracteres ingresados en el campo de entrada del importe.

    Esta función actúa como un filtro para el campo de entrada 'entrada_importe',
    asegurando que solo se permitan números, un punto decimal, y teclas especiales
    como BackSpace, Delete, las flechas, etc. También maneja el pegado (Ctrl+V)
    para validar que el texto pegado sea un número decimal válido con hasta 2 decimales.

    Args:
        event (tk.Event, optional): El evento de teclado que desencadenó la función.
            Se utiliza para obtener el carácter ingresado ('event.char'), la tecla
            presionada ('event.keysym') y el estado del teclado ('event.state').
            Defaults to None.

    Returns:
        str or None: Retorna "break" si el carácter ingresado no es válido (para
            evitar que se inserte). Retorna None si el carácter es válido o si
            se está manejando un evento de pegado.
    """
    retornar = "break"  # Valor por defecto: evita la inserción del carácter.
    carácter = event.char  # Obtiene el carácter individual ingresado.
    tecla = event.keysym.lower()  # Obtiene la tecla presionada (en minúsculas).

    # Permite dígitos, punto decimal, teclas de navegación/edición y combinaciones Ctrl+X/C/V.
    if (carácter and carácter in '0123456789.') or \
       (event and (event.keysym == 'BackSpace' or event.keysym.startswith('Shift') or \
                   event.keysym in ('Delete', 'Home', 'End', 'Up', 'Down', 'Left', 'Right'))) or \
       (event.state & 0x0004 and tecla in ['x', 'v', 'c']):

        # Maneja el pegado (Ctrl+V) y la entrada de números/punto.
        if (event.state & 0x0004 and tecla == 'v') or (carácter and carácter in '0123456789.'):
            contenido_antes = importe.get()  # Guarda el contenido actual del campo.
            posición_cursor_antes = entrada_importe.index("insert")  # Guarda la posición del cursor.
            retornar = None  # Permite la inserción (temporalmente).

            # Define una función para actualizar el contenido después del pegado.
            def actualizar_contenido():
                """
                Valida y corrige el contenido del campo después de un evento de pegado.
                Se asegura que el contenido sea un número decimal con como máximo 2 decimales.
                Si no lo es, revierte al contenido anterior y reposiciona el cursor.
                """
                contenido_después = importe.get()  # Obtiene el contenido después del pegado.
                es_decimal = esNúmeroDecimalConXDecimales(contenido_después, 2)
                if not es_decimal:  # Si el contenido no es un decimal válido.
                    importe.set(contenido_antes)  # Restaura el contenido anterior.
                    entrada_importe.icursor(posición_cursor_antes)  # Restaura la posición del cursor.

            # Ejecuta 'actualizar_contenido' después de que Tkinter termine de procesar el evento de pegado.
            entrada_importe.after_idle(actualizar_contenido)
        else:
            retornar = None  # Permite la inserción de dígitos y punto decimal.
    return retornar  # Retorna "break" si el carácter no es válido, None si es válido.

def borrarTodasLasFilas(tabla):
    """
    Borra todas las filas de la tabla.

    Itera sobre cada elemento (fila) hijo de la tabla y lo elimina.
    Esta función se utiliza para limpiar la tabla antes de cargar nuevos datos.
    """
    for item in tabla.get_children():  # Itera sobre los identificadores de las filas.
        tabla.delete(item)  # Elimina la fila correspondiente al identificador.

def crearTabla(
        contenedor, 
        columnas, 
        filas_mostrar,
        columna_tabla,
        sticky_tabla,
        peso_columna_tabla
    ):
    tabla = ttk.Treeview(
        contenedor,
        columns=tuple(columnas.keys()),
        show='headings',
        height=filas_mostrar
    )
    for nombre_columna, detalles_columna in columnas.items():
        tabla.heading(nombre_columna, text=detalles_columna[0], anchor = detalles_columna[2])
        tabla.column(
            nombre_columna,
            anchor=detalles_columna[1],
            width=detalles_columna[3],
            minwidth=detalles_columna[4],
            stretch=detalles_columna[5]
        )

    tabla.grid(
        row=0,
        column=0,
        sticky=sticky_tabla
    )

    barra_desplazamiento_vertical = ttk.Scrollbar(
        contenedor,
        orient=tk.VERTICAL,
        command=tabla.yview
    )
    barra_desplazamiento_horizontal = ttk.Scrollbar(
        contenedor,
        orient=tk.HORIZONTAL,
        command=tabla.xview
    )

    tabla.configure(xscrollcommand=barra_desplazamiento_horizontal.set)
    tabla.configure(yscrollcommand=barra_desplazamiento_vertical.set)

    # La tabla utiliza todo el espacio que necesite dentro de donde está
    # La columna 0 (tabla y barra horizontal) se expande horizontalmente, se expande todos los píxeles que necesite porque necesita más
    # que el tamaño de su contenedor
    contenedor.grid_columnconfigure(columna_tabla, weight=peso_columna_tabla)  

    # Configurar expansión del contenedor del contenedor para que crezca
    # el contenedor padre no tiene un tamaño fijo y entonces utiliza todo su espacio dentro de su contenedor,
    # siempre se adapta a su contenedor,
    # es el cotenedor quien le da el espacio al padre y el padre no crece más allá si tiene un tamaño menor a su contenedor
    # el contenedor padre, al igual que la tabla en el contenedor, también se expande todo lo que necesite, pero su tamaño
    # es 0 y entonces se expande simplemente a todo el espacio que hay y si no hay más no se expande más
    contenedor.master.grid_columnconfigure(columna_tabla, weight=peso_columna_tabla)

    # en Python la columna con más pesos se expande todo lo que necesite, pero si sobra espacio se expande
    # en todo el espacio sobrante
    # de esa manera la tabla es más ancha que su contenedor, el espacio visible termina siendo menor que la tabla
    # y entonces se activa la barra horizontal

    barra_desplazamiento_vertical.grid(row=0, column=1, sticky='ns')
    barra_desplazamiento_horizontal.grid(row=1, column=0, columnspan=1, sticky='we')

    # tabla_movimientos.bind("<<TreeviewSelect>>", cargarRegistros)

    return tabla

