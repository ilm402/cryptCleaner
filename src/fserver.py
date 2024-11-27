import ssl
from flask import Flask, render_template, send_from_directory
import os

# Crear la aplicación Flask
app = Flask(__name__, template_folder='../templates')

# Configuración de rutas
DOWNLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../downloads'))
CERT_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../certs'))
FILENAME = "instalador_falso.txt"  # Cambia según el archivo en la carpeta "downloads"

@app.route('/')
def fake_home():
    # Renderizar la página principal
    return render_template("index.html")

@app.route('/download', methods=['GET'])
def fake_download():
    # Descargar archivo
    try:
        return send_from_directory(DOWNLOAD_FOLDER, FILENAME, as_attachment=True)
    except FileNotFoundError:
        return render_template("404.html"), 404

if __name__ == "__main__":
    # Configuración de certificados
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        os.path.join(CERT_FOLDER, 'fake_server.crt'),
        os.path.join(CERT_FOLDER, 'fake_server.key')
    )
    # Iniciar la aplicación
    app.run(host="127.0.0.1", port=8444, ssl_context=context)
