import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from zeep import Client
from zeep.transports import Transport
import arca_arg.settings as confg
from arca_arg.webservice import ArcaWebService
from arca_arg.settings import WSDL_FEV1_HOM, WSDL_FEV1_PROD
from datetime import datetime
import funciones_útiles
import configparser

# Constantes fijas de lógica (No de configuración de usuario)
TIPO_COMPROBANTE = 6  # Factura B
CONCEPTO_PRODUCTOS = 1
DOC_TIPO_SIN_IDENTIFICAR = 99
DOC_NRO_SIN_IDENTIFICAR = 0
CONDICION_IVA_CONSUMIDOR_FINAL = 5

# --- PARCHE DE SEGURIDAD SSL PARA AFIP ---


class CifradoFuerteAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.load_default_certs()
        context.options |= 0x4 | 0x8
        kwargs['ssl_context'] = context
        return super(CifradoFuerteAdapter, self).init_poolmanager(*args, **kwargs)

    def obtener_transporte_seguro():
        session = requests.Session()
        adapter = CifradoFuerteAdapter()
        session.mount('https://', adapter)
        return Transport(session=session, timeout=30)

    def emitir_factura_b(importe_total):
        """
        Emite una Factura B a Consumidor Final.
        """
        try:
            # 1. Cargar configuración desde funciones_útiles (Fuente Única de Verdad)
            cfg = funciones_útiles.leer_configuracion_facturacion()

            cuit = cfg.get('cuit')
            pto_vta = int(cfg.get('punto_venta')) if cfg.get(
                'punto_venta') else 1
            cert_path = cfg.get('certificado')
            key_path = cfg.get('key')
            es_prod = cfg.get('produccion') == 'True'

            if not all([cuit, pto_vta, cert_path, key_path]):
                return {'exito': False, 'mensaje': "Faltan datos de configuración de facturación. Revise la pestaña Ajustes."}

            # ... (resto del código de configuración de arca_arg sigue igual) ...
            confg.CUIT = int(cuit)
            confg.PRIVATE_KEY_PATH = key_path
            confg.CERT_PATH = cert_path
            confg.PROD = es_prod
            confg.TA_FILES_PATH = os.path.dirname(cert_path)

            wsdl_url = WSDL_FEV1_PROD if es_prod else WSDL_FEV1_HOM

            # 2. Conexión
            ws = ArcaWebService(wsdl_url, 'wsfe')
            transport = obtener_transporte_seguro()
            ws.client = Client(wsdl_url, transport=transport)

            cliente = ws.client
            auth_data = {'Token': ws.token,
                         'Sign': ws.sign, 'Cuit': confg.CUIT}

            # 3. Consultar último comprobante
            ultimo = cliente.service.FECompUltimoAutorizado(
                Auth=auth_data,
                PtoVta=pto_vta,
                CbteTipo=TIPO_COMPROBANTE
            )
            nro_cbte = ultimo['CbteNro'] + 1

            # 4. Calcular importes
            imp_neto = round(importe_total / 1.21, 2)
            imp_iva = round(importe_total - imp_neto, 2)

            # Ajuste por redondeo
            imp_total_calculado = imp_neto + imp_iva
            diff = round(importe_total - imp_total_calculado, 2)
            if diff != 0:
                imp_iva += diff

            fecha_hoy = datetime.now().strftime('%Y%m%d')

            # 5. Armar cuerpo
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
                'CondicionIVAReceptorId': CONDICION_IVA_CONSUMIDOR_FINAL,
                'Iva': {
                    'AlicIva': [
                        {'Id': 5, 'BaseImp': imp_neto, 'Importe': imp_iva}
                    ]
                }
            }

            # 6. Enviar solicitud
            solicitud = {
                'FeCAEReq': {
                    'FeCabReq': {
                        'CantReg': 1,
                        'PtoVta': pto_vta,
                        'CbteTipo': TIPO_COMPROBANTE
                    },
                    'FeDetReq': {
                        'FECAEDetRequest': [factura]
                    }
                }
            }

            respuesta = cliente.service.FECAESolicitar(
                Auth=auth_data, **solicitud)

            # 7. Procesar respuesta
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
                            observaciones.append(
                                f"{obs['Code']}: {obs['Msg']}")

                msg_error = "AFIP rechazó el comprobante.\n"
                if errores:
                    msg_error += f"Errores: {'; '.join(errores)}\n"
                if observaciones:
                    msg_error += f"Obs: {'; '.join(observaciones)}"

                return {'exito': False, 'mensaje': msg_error}

        except Exception as e:
            return {'exito': False, 'mensaje': f"Error de facturación: {str(e)}"}
