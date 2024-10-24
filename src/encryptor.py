from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
from pathlib import Path
import logging

# Configurar logging para mostrar mensajes detallados
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Definir la ruta de la clave como una ruta relativa al directorio del script
KEY_PATH = Path("C:/Users/kekol/Desktop/TCC/cryptCleaner/key/key.key")

# Función para verificar si la clave es válida
def is_valid_key(key):
    return len(key) in [16, 24, 32]  # AES permite claves de 128, 192 o 256 bits (16, 24 o 32 bytes)

# Función para generar o leer la clave
def load_or_generate_key():
    try:
        if not KEY_PATH.exists():
            key = os.urandom(32)  # Generar clave AES de 256 bits
            # Guardar la clave en formato hexadecimal
            KEY_PATH.parent.mkdir(parents=True, exist_ok=True)  # Crear directorio si no existe
            with open(KEY_PATH, 'w') as key_file:
                key_file.write(key.hex())  # Guardar la clave en formato hexadecimal
            logging.info(f"Clave generada y guardada en {KEY_PATH}")
            return key
        else:
            with open(KEY_PATH, 'r') as key_file:
                key_hex = key_file.read()  # Leer la clave en formato hexadecimal
                key = bytes.fromhex(key_hex)  # Convertir de hexadecimal a bytes
            logging.info(f"Clave cargada desde {KEY_PATH}")
            if is_valid_key(key):
                return key
            else:
                logging.error("Clave cargada no es válida.")
                raise ValueError("Clave cargada no es válida.")
    except Exception as e:
        logging.error(f"Error al generar o cargar la clave: {e}")
        raise

# Cifrar un archivo
def encrypt_file(file_path):
    try:
        key = load_or_generate_key()
        iv = os.urandom(16)  # Vector de inicialización
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        logging.info(f"Cifrando archivo: {file_path}")
        with open(file_path, 'rb') as f:
            plaintext = f.read()

        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        encrypted_file = file_path.with_suffix(file_path.suffix + '.enc')
        with open(encrypted_file, 'wb') as f:
            f.write(iv + ciphertext)

        logging.info(f"Archivo {file_path} cifrado exitosamente como {encrypted_file}")

    except Exception as e:
        logging.error(f"Error al cifrar archivo {file_path}: {e}")
        raise


def decrypt_file(file_path):
    try:
        key = load_or_generate_key()

        logging.info(f"Descifrando archivo: {file_path}")
        with open(file_path, 'rb') as f:
            iv = f.read(16)  # Leer los primeros 16 bytes que contienen el IV
            ciphertext = f.read()

        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # Modificamos la ruta agregando "_decrypted" antes de la extensión original
        decrypted_file = file_path.with_name(file_path.stem + '_decrypted' + file_path.suffix.replace('.enc', ''))

        with open(decrypted_file, 'wb') as f:
            f.write(plaintext)

        logging.info(f"Archivo {file_path} descifrado exitosamente como {decrypted_file}")

    except Exception as e:
        logging.error(f"Error al descifrar archivo {file_path}: {e}")
        raise
