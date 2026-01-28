from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
from cryptography import x509


def generar_archivos_afip(cuit, nombre_empresa):
    print(f"--- Generando claves para CUIT: {cuit} ---")

    # 1. Generar la Clave Privada (Private Key)
    # AFIP requiere RSA de 2048 bits
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Nombre del archivo de la clave
    nombre_key = f"privada_{cuit}.key"

    # Guardar la clave privada en el disco
    with open(nombre_key, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            # No poner contraseña para facilitar el uso en el sistema
            encryption_algorithm=serialization.NoEncryption(),
        ))

    print(f"✅ Archivo de CLAVE PRIVADA generado: {nombre_key}")
    print("   (ADVERTENCIA: Este archivo es secreto. No lo compartas con nadie).")

    # 2. Generar el Pedido de Certificado (CSR)
    # El Common Name (CN) suele usarse como el "Alias" del servicio
    common_name = f"sistema_{cuit}"

    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        # Datos requeridos por AFIP
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, nombre_empresa),
        x509.NameAttribute(NameOID.COUNTRY_NAME, "AR"),
        # El Serial Number DEBE tener el formato "CUIT xxxxxxxxxxx"
        x509.NameAttribute(NameOID.SERIAL_NUMBER, f"CUIT {cuit}"),
    ])).sign(key, hashes.SHA256())

    # Nombre del archivo CSR
    nombre_csr = f"pedido_{cuit}.csr"

    # Guardar el pedido CSR en el disco
    with open(nombre_csr, "wb") as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))

    print(f"✅ Archivo de PEDIDO (CSR) generado: {nombre_csr}")
    print("-" * 50)
    print("PASOS SIGUIENTES PARA EL USUARIO:")
    print(f"1. Ingresar a AFIP con Clave Fiscal.")
    print(f"2. Ir al servicio 'Administración de Certificados Digitales'.")
    print(f"3. Agregar un alias (ej: '{common_name}').")
    print(f"4. Subir el archivo '{nombre_csr}' que se acaba de crear.")
    print(f"5. Descargar el certificado .crt que devolverá AFIP.")
    print("-" * 50)


if __name__ == "__main__":
    # --- CONFIGURACIÓN DE EJEMPLO ---
    # Puedes cambiar esto o hacer inputs para pedirlo al usuario

    mi_cuit = input("Ingrese el CUIT (solo números): ").strip()
    mi_nombre = input("Ingrese Nombre de la Empresa o Persona: ").strip()

    if mi_cuit:
        generar_archivos_afip(mi_cuit, mi_nombre)
    else:
        print("Error: El CUIT es obligatorio.")
