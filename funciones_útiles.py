import validación_tipo_de_datos
from datetime import datetime, date
import Limpiar_pantalla_y_pausar
import os
import requests
from tkinter import ttk
import sys
import tkinter as tk
import threading
import socket
import platform
from MensajeModerno import MensajeModerno
import configparser

NOMBRE_CARPETA_RESPALDO_BASE_DE_DATOS = 'Respaldo de la base de datos'
RESPALDAR = True
FORMATO_PREFERIDO_FECHA = '%d/%m/%Y'
FORMATO_FECHA_BD = '%Y-%m-%d'
FORMATO_FECHA_CALENDAR = '%d/%m/%y'
FORMATO_PREFERIDO_HORA_Y_FECHA = '%H:%M:%S %d/%m/%Y'
NOMBRE_ARCHIVO_CONFIG = 'config.ini'


def obtenerNúmeroEnteroNaturalConMáximo(mínimo, máximo, primer_mensaje, mensaje_error_tipo_dato, mensaje_error_en_rango):
    valor = input(primer_mensaje)
    controlar = True
    while controlar:
        if not validación_tipo_de_datos.esEntero(valor):
            print(mensaje_error_tipo_dato, end="")
            valor = input()
        elif int(valor) < mínimo or int(valor) > máximo:
            print(mensaje_error_en_rango, end="")
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
            print(mensaje_error_tipo_dato, end="")
            valor = input()
        elif int(valor) < mínimo:
            print(mensaje_error_en_rango, end="")
            valor = input()
        else:
            valor = int(valor)
            controlar = False
    return valor


def esNúmeroDecimalConLímites(número, máx_dígitos_totales, máx_decimales):
    """
    Valida si un string es un número decimal válido respetando límites de dígitos.
    Permite ceros no significativos a la derecha en la parte decimal.

    Ej: DECIMAL(10, 2).
    Acepta "12.5000" porque al recortar ceros queda "12.5" (1 decimal < 2).
    Rechaza "12.555" porque queda "12.555" (3 decimales > 2).
    """
    if not número:
        return True  # Permitir vacío mientras se escribe

    try:
        float(número)  # Primera validación simple: ¿es número?
    except ValueError:
        return False

    partes = número.split('.')

    # Validar parte entera
    parte_entera = partes[0]

    # Si el número es negativo, el signo '-' no cuenta como dígito de precisión en la BD
    longitud_entera = len(parte_entera)
    if parte_entera.startswith('-'):
        longitud_entera -= 1

    máx_enteros = máx_dígitos_totales - máx_decimales
    if longitud_entera > máx_enteros:
        return False

    # Validar parte decimal con recorte de ceros
    if len(partes) > 1:
        parte_decimal = partes[1]

        # CAMBIO CLAVE: Recortar ceros a la derecha antes de medir
        # "500" -> "5" (len 1)
        # "00" -> "" (len 0)
        parte_decimal_significativa = parte_decimal.rstrip('0')

        if len(parte_decimal_significativa) > máx_decimales:
            return False

    return True


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
            print(mensaje_error_tipo_dato, end="")
            valor = input()
        elif float(valor) < mínimo or float(valor) == mínimo and not incluir_mínimo:
            print(mensaje_error_en_rango, end="")
            valor = input()
        else:
            valor = float(valor)
            controlar = False
    return valor


def preguntarSíONo(pregunta):
    print(pregunta, " (S/N): ", sep="", end="")
    respuesta = input().upper()
    while respuesta != 'S' and respuesta != 'N':
        respuesta = input(
            "Ha ingresado una respuesta no válida. Vuelva a intentarlo: ").upper()
    return respuesta


def enumerarOpciones(mensaje, lista_opciones, obligatorio_elegir_una):
    print(mensaje + "\n")
    cant_opciones = len(lista_opciones)
    for x in range(len(lista_opciones)):
        print(x + 1, "_ ", lista_opciones[x], sep="")
    if not obligatorio_elegir_una:
        print(len(lista_opciones) + 1, "_ Ninguna de las anteriores.", sep="")
        cant_opciones += 1
    opción_elegida = obtenerNúmeroEnteroNaturalConMáximo(1, cant_opciones, "\nElija una de las opciones: ",
                                                         "Lo ingresado no es una opción. Las opciones son números enteros. Inténtelo nuevamente: ", "La opción ingresada no es válida. Vuelva a intentarlo: ")
    return opción_elegida


def obtenerNombreMes(mes):
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
             "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    return meses[mes - 1]


def preguntarAño(primer_año):
    respuesta_año = preguntarSíONo("¿Se trata de este año?")
    if respuesta_año == 'N':
        Limpiar_pantalla_y_pausar.limpiarPantalla()
        año = obtenerNúmeroEnteroNaturalConMáximo(primer_año, date.today().year, "Ingrese el año del que quiere saber las estadísticas: ",
                                                  "Debe ingresar un número para referirse al año. Inténtelo nuevamente: ", "No se ha registrado estadística para ese año. Ingrese otro: ")
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
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
             "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
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
            fecha = input(
                "No ha ingresado una fecha. Ingrese una respetando este formato dd/mm/AAAA: ")
        elif fecha_del_futuro and not se_vale_fecha_del_futuro:
            Limpiar_pantalla_y_pausar.limpiarPantalla()
            fecha = input(
                "La fecha ingresada es del futuro y por tanto no es válida. Inténtelo nuevamente: ")
        elif fecha_inexistente:
            Limpiar_pantalla_y_pausar.limpiarPantalla()
            fecha = input("No existe el " + fecha +
                          ". Revise la fecha e inténtelo nuevamente: ")
        elif fecha_del_pasado_o_presente and solo_fecha_del_futuro:
            Limpiar_pantalla_y_pausar.limpiarPantalla()
            fecha = input(
                "La fecha ingresada es del pasado o presente y por tanto no es válida. Inténtelo nuevamente: ")
        elif len(fecha) == 10:
            fecha_válida = True
    return datetime.strptime(fecha, FORMATO_PREFERIDO_FECHA).date()


def crearHiloRespaldarBaseDeDatos(base_de_datos):
    hilo = threading.Thread(target=respaldarBaseDeDatos,
                            args=(base_de_datos,), daemon=True)
    hilo.start()


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


def leer_configuracion_facturacion():
    """
    Lee la configuración de facturación del archivo config.ini.
    Accesible desde Programa.py y facturación.py
    """
    config = configparser.ConfigParser()
    config.read(NOMBRE_ARCHIVO_CONFIG, encoding='utf-8')

    datos = {
        'cuit': '',
        'punto_venta': '1',
        'certificado': '',
        'key': '',
        'produccion': 'False'
    }

    if 'facturacion' in config:
        section = config['facturacion']
        datos['cuit'] = section.get('cuit', '')
        datos['punto_venta'] = section.get('punto_venta', '1')
        datos['certificado'] = section.get('certificado', '')
        datos['key'] = section.get('key', '')
        datos['produccion'] = section.get('produccion', 'False')

    return datos


def guardar_configuracion_facturacion(datos):
    """
    Guarda los datos de facturación en el archivo config.ini.
    """
    config = configparser.ConfigParser()
    config.read(NOMBRE_ARCHIVO_CONFIG, encoding='utf-8')

    if 'facturacion' not in config:
        config['facturacion'] = {}

    config['facturacion']['cuit'] = datos['cuit']
    config['facturacion']['punto_venta'] = datos['punto_venta']
    config['facturacion']['certificado'] = datos['certificado']
    config['facturacion']['key'] = datos['key']
    config['facturacion']['produccion'] = str(datos['produccion'])

    with open(NOMBRE_ARCHIVO_CONFIG, 'w', encoding='utf-8') as configfile:
        config.write(configfile)


def obtenerRutaRespaldo():
    """
    Obtiene la ruta absoluta donde se guardarán los respaldos.
    Si es un .exe (PyInstaller), usa la carpeta del ejecutable.
    Si es un script .py, usa la carpeta del script.
    Si la carpeta de respaldo no existe, la crea.
    """
    # Detectar si estamos corriendo como ejecutable (.exe) o script (.py)
    if getattr(sys, 'frozen', False):
        directorio_base = os.path.dirname(sys.executable)
    else:
        directorio_base = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta completa
    ruta_completa_respaldo = os.path.join(
        directorio_base, NOMBRE_CARPETA_RESPALDO_BASE_DE_DATOS)

    # Verificar si existe, si no, crearla
    if not os.path.exists(ruta_completa_respaldo):
        try:
            os.makedirs(ruta_completa_respaldo)
            print(f"Carpeta de respaldo creada en: {ruta_completa_respaldo}")
        except OSError as e:
            print(f"Error al crear el directorio de respaldo: {e}")
            # En caso de error crítico de permisos, podrías retornar directorio_base o lanzar error

    return ruta_completa_respaldo


def respaldarBaseDeDatos(base_de_datos):
    """
    Llama a la base de datos para generar el dump, pasándole
    la ruta dinámica obtenida.
    """
    try:
        ruta_destino = obtenerRutaRespaldo()
        base_de_datos.respaldarBaseDeDatos(ruta_destino)
    except Exception as e:
        print(f"No se pudo realizar el respaldo automático: {e}")


def controlar_caracteres_precio(importe, entrada_importe, máx_dígitos=10, máx_decimales=2, event=None):
    """
    Controla la entrada de caracteres verificando longitud total y decimales.
    Muestra una advertencia si se excede el límite.
    """

    retornar = "break"
    carácter = event.char
    tecla = event.keysym.lower()

    # Construcción dinámica del mensaje de límite (Ej: "99999999.99")
    cant_enteros = máx_dígitos - máx_decimales
    max_valor_str = f"{'9' * cant_enteros}.{'9' * máx_decimales}"

    # Lógica para teclas de control
    es_tecla_control = (event.keysym in (
        'BackSpace', 'Delete', 'Left', 'Right', 'Home', 'End', 'Tab'))
    es_copiar_pegar = (event.state & 0x0004 and tecla in ['x', 'v', 'c'])

    if es_tecla_control or es_copiar_pegar:

        if tecla == 'v':  # Pegar
            contenido_antes = importe.get()
            pos_antes = entrada_importe.index("insert")
            retornar = None

            def validar_pegado():
                contenido = importe.get()
                if not esNúmeroDecimalConLímites(contenido, máx_dígitos, máx_decimales):
                    importe.set(contenido_antes)
                    entrada_importe.icursor(pos_antes)
                    # Advertencia al pegar
                    if float(contenido) > float(max_valor_str):
                        MensajeModerno(entrada_importe.winfo_toplevel(), "Valor fuera de rango",
                                       f"El valor del precio debe ser menor o igual a $ {max_valor_str}", tipo="advertencia")
                    else:
                        MensajeModerno(entrada_importe.winfo_toplevel(), "Formato inválido",
                                       f"El valor pegado no es un número decimal válido. Se permiten números decimales con hasta {máx_decimales} decimales.", tipo="advertencia")

            entrada_importe.after_idle(validar_pegado)
        else:
            return None

    # Lógica para caracteres numéricos y punto
    elif carácter and (carácter.isdigit() or carácter == '.'):
        texto_actual = importe.get()
        pos_cursor = entrada_importe.index("insert")

        # Construir el nuevo texto hipotético
        if entrada_importe.select_present():
            sel_start = entrada_importe.index("sel.first")
            sel_end = entrada_importe.index("sel.last")
            nuevo_texto = texto_actual[:sel_start] + \
                carácter + texto_actual[sel_end:]
        else:
            nuevo_texto = texto_actual[:pos_cursor] + \
                carácter + texto_actual[pos_cursor:]

        # Validar
        if esNúmeroDecimalConLímites(nuevo_texto, máx_dígitos, máx_decimales):
            return None  # Aceptar
        else:
            if float(nuevo_texto) > float(max_valor_str):
                # Advertencia al escribir
                MensajeModerno(entrada_importe.winfo_toplevel(), "Valor fuera de rango",
                               f"El valor del precio debe ser menor o igual a $ {max_valor_str}", tipo="advertencia")
            else:
                MensajeModerno(entrada_importe.winfo_toplevel(), "Formato inválido",
                               f"El valor ingresado no es un número decimal válido. Se permiten números decimales con hasta {máx_decimales} decimales.", tipo="advertencia")
            return "break"

    return retornar


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
        tabla.heading(nombre_columna,
                      text=detalles_columna[0], anchor=detalles_columna[2])
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
    contenedor.master.grid_columnconfigure(
        columna_tabla, weight=peso_columna_tabla)

    # en Python la columna con más pesos se expande todo lo que necesite, pero si sobra espacio se expande
    # en todo el espacio sobrante
    # de esa manera la tabla es más ancha que su contenedor, el espacio visible termina siendo menor que la tabla
    # y entonces se activa la barra horizontal

    barra_desplazamiento_vertical.grid(row=0, column=1, sticky='ns')
    barra_desplazamiento_horizontal.grid(
        row=1, column=0, columnspan=1, sticky='we')

    # tabla_movimientos.bind("<<TreeviewSelect>>", cargarRegistros)

    return tabla
