import ssl

from flask import Flask, send_from_directory

app = Flask(__name__)

# Configuración del servidor legítimo
DOWNLOAD_FOLDER = "C:/Users/kekol/Desktop/TCC/cryptCleaner/downloads"
FILENAME = "instalador_falso.txt"  # Cambia por el nombre del archivo


@app.route('/')
def fake_home():
    return "<h1>Sitio Falso</h1><p>Haz clic <a href='/download'>aquí</a> para descargar la aplicación.</p>"

@app.route('/download', methods=['GET'])
def fake_download():
    try:
        return send_from_directory(DOWNLOAD_FOLDER, FILENAME, as_attachment=True)
    except FileNotFoundError:
        return "Archivo no encontrado", 404
if __name__ == "__main__":
    # Certificados del servidor falso
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('C:/Users/kekol/Desktop/TCC/cryptCleaner/certs/fake_server.crt',
                            'C:/Users/kekol/Desktop/TCC/cryptCleaner/certs/fake_server.key')
    app.run(host="127.0.0.1", port=8444, ssl_context=context)  # Puerto HTTPS falso
