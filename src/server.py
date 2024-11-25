from flask import Flask, send_from_directory
import ssl

app = Flask(__name__)

# Configuración del servidor legítimo
DOWNLOAD_FOLDER = "C:/Users/kekol/Desktop/TCC/cryptCleaner/downloads"
FILENAME = "instalador.txt"  # Cambia por el nombre del archivo

@app.route('/download', methods=['GET'])
def download_file():
    try:
        return send_from_directory(DOWNLOAD_FOLDER, FILENAME, as_attachment=True)
    except FileNotFoundError:
        return "Archivo no encontrado", 404

if __name__ == "__main__":
    # Certificados del servidor legítimo
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('C:/Users/kekol/Desktop/TCC/cryptCleaner/certs/server.crt',
                            'C:/Users/kekol/Desktop/TCC/cryptCleaner/certs/server.key')
    app.run(host="127.0.0.1", port=8443, ssl_context=context)  # Puerto HTTPS
