from encryptor import encrypt_file, decrypt_file
from pathlib import Path

def main():
    choice = input("¿Deseas cifrar (C) o descifrar (D) un archivo?: ").lower()

    if choice == 'c':
        file_path = Path(input("Introduce la ruta del archivo a cifrar: "))
        if file_path.is_file():
            encrypt_file(file_path)
        else:
            print("Archivo no encontrado.")
    elif choice == 'd':
        file_path = Path(input("Introduce la ruta del archivo a descifrar: "))
        if file_path.is_file():
            decrypt_file(file_path)
        else:
            print("Archivo no encontrado.")
    else:
        print("Opción no válida.")

if __name__ == "__main__":
    main()
