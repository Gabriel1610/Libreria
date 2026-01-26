import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from zeep import Client
from zeep.transports import Transport
import arca_arg.settings as confg


# Obtenemos la ruta donde está este archivo
base_dir = os.path.dirname(os.path.abspath(__file__))

# Constantes de AFIP
CUIT_EMISOR = 27350043344
PUNTO_VENTA = 1
TIPO_COMPROBANTE = 6  # Factura B
CONCEPTO_PRODUCTOS = 1
DOC_TIPO_SIN_IDENTIFICAR = 99 
DOC_NRO_SIN_IDENTIFICAR = 0
CONDICION_IVA_CONSUMIDOR_FINAL = 5 # <--- NUEVA CONSTANTE NECESARIA

# --- APLICAMOS LA CONFIGURACIÓN GLOBALMENTE AQUÍ ---
confg.CUIT = CUIT_EMISOR
confg.PRIVATE_KEY_PATH = os.path.join(base_dir, "homologacion.key")
confg.CERT_PATH = os.path.join(base_dir, "homologacion.crt")
confg.PROD = False 
confg.TA_FILES_PATH = base_dir

# --- PARCHE DE SEGURIDAD SSL PARA AFIP ---
class CifradoFuerteAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.load_default_certs()
        # Forzar cifrados compatibles con servidores antiguos/gubernamentales
        context.options |= 0x4 | 0x8 
        kwargs['ssl_context'] = context
        return super(CifradoFuerteAdapter, self).init_poolmanager(*args, **kwargs)

def obtener_transporte_seguro():
    session = requests.Session()
    adapter = CifradoFuerteAdapter()
    session.mount('https://', adapter)
    return Transport(session=session, timeout=30)
# -----------------------------------------

# ---------------------------------------------------------------------------
# PASO 2: AHORA SÍ IMPORTAMOS LA LIBRERÍA
# ---------------------------------------------------------------------------
from arca_arg.webservice import ArcaWebService
from arca_arg.settings import WSDL_FEV1_HOM
from datetime import datetime

def emitir_factura_b(importe_total):
    """
    Emite una Factura B a Consumidor Final por el importe total dado.
    Retorna un diccionario con el resultado o lanza una excepción si falla.
    """
    
    try:
        # 1. Conexión
        ws = ArcaWebService(WSDL_FEV1_HOM, 'wsfe')

        # Inyectamos nuestro transporte seguro al cliente Zeep
        transport = obtener_transporte_seguro()
        ws.client = Client(WSDL_FEV1_HOM, transport=transport)
        
        cliente = ws.client
        auth_data = {'Token': ws.token, 'Sign': ws.sign, 'Cuit': confg.CUIT}

        # 2. Consultar último comprobante
        ultimo = cliente.service.FECompUltimoAutorizado(
            Auth=auth_data, 
            PtoVta=PUNTO_VENTA,
            CbteTipo=TIPO_COMPROBANTE
        )
        nro_cbte = ultimo['CbteNro'] + 1

        # 3. Calcular importes (IVA incluido en Factura B)
        # Neto = Total / 1.21
        imp_neto = round(importe_total / 1.21, 2)
        imp_iva = round(importe_total - imp_neto, 2)
        
        # Ajuste por redondeo
        imp_total_calculado = imp_neto + imp_iva
        diff = round(importe_total - imp_total_calculado, 2)
        if diff != 0:
            imp_iva += diff

        fecha_hoy = datetime.now().strftime('%Y%m%d')

        # 4. Armar el cuerpo de la factura
        factura = {
            'Concepto': CONCEPTO_PRODUCTOS,
            'DocTipo': DOC_TIPO_SIN_IDENTIFICAR,
            'DocNro': DOC_NRO_SIN_IDENTIFICAR,
            'CbteDesde': nro_cbte,
            'CbteHasta': nro_cbte,
            'CbteFch': fecha_hoy, 
            'ImpTotal': importe_total,
            'ImpTotConc': 0,
            'ImpNeto': imp_neto,
            'ImpOpEx': 0,
            'ImpTrib': 0,
            'ImpIVA': imp_iva,
            'FchServDesde': None,
            'FchServHasta': None,
            'FchVtoPago': None,
            'MonId': 'PES',
            'MonCotiz': 1,
            
            # --- CORRECCIÓN CLAVE AQUÍ ---
            # AFIP requiere explícitamente la condición frente al IVA del receptor.
            # 5 = Consumidor Final
            'CondicionIVAReceptorId': CONDICION_IVA_CONSUMIDOR_FINAL, 
            # -----------------------------

            'Iva': {
                'AlicIva': [
                    {
                        'Id': 5, # 21%
                        'BaseImp': imp_neto,
                        'Importe': imp_iva
                    }
                ]
            }
        }

        # 5. Enviar solicitud
        solicitud = {
            'FeCAEReq': {
                'FeCabReq': {
                    'CantReg': 1,
                    'PtoVta': PUNTO_VENTA,
                    'CbteTipo': TIPO_COMPROBANTE
                },
                'FeDetReq': {
                    'FECAEDetRequest': [factura]
                }
            }
        }

        respuesta = cliente.service.FECAESolicitar(Auth=auth_data, **solicitud)

        # 6. Procesar respuesta
        if respuesta['FeCabResp']['Resultado'] == 'A':
            detalle = respuesta['FeDetResp']['FECAEDetResponse'][0]
            return {
                'exito': True,
                'cae': detalle['CAE'],
                'vencimiento_cae': detalle['CAEFchVto'],
                'numero_factura': nro_cbte,
                'mensaje': "Factura aprobada correctamente."
            }
        else:
            errores = []
            if 'Errors' in respuesta and respuesta['Errors']:
                for err in respuesta['Errors']['Err']:
                    errores.append(f"{err['Code']}: {err['Msg']}")
            
            observaciones = []
            if 'FeDetResp' in respuesta and respuesta['FeDetResp']['FECAEDetResponse']:
                det = respuesta['FeDetResp']['FECAEDetResponse'][0]
                if 'Observaciones' in det and det['Observaciones']:
                    for obs in det['Observaciones']['Obs']:
                        observaciones.append(f"{obs['Code']}: {obs['Msg']}")

            msg_error = "AFIP rechazó el comprobante.\n"
            if errores: msg_error += f"Errores: {'; '.join(errores)}\n"
            if observaciones: msg_error += f"Obs: {'; '.join(observaciones)}"
            
            return {'exito': False, 'mensaje': msg_error}

    except Exception as e:
        return {'exito': False, 'mensaje': f"Error de conexión o interno: {str(e)}"}