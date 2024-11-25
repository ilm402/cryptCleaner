import requests
from requests.exceptions import SSLError

# Ruta al certificado de la autoridad certificadora (CA)
CA_CERT = 'C:/Users/kekol/Desktop/TCC/cryptCleaner/certs/ca.crt'

def connect_to_server(url):
    """
    Intenta conectarse al servidor especificado usando el certificado CA para verificarlo.
    """
    try:
        print(f"Conectando a {url}...")
        response = requests.get(url, verify=CA_CERT)
        print("Conexión exitosa. Respuesta del servidor:")
        print(response.text)
    except SSLError as e:
        print(f"Error SSL: {e}")
        decision = input("El certificado no es válido. ¿Deseas continuar ignorando la advertencia? (s/n): ")
        if decision.lower() == 's':
            response = requests.get(url, verify=False)
            print("Conexión realizada sin verificar el certificado:")
            print(response.text)
        else:
            print("Conexión rechazada.")

if __name__ == "__main__":
    # URLs de los servidores
    legit_server_url = "https://127.0.0.1:8443/download"  # Servidor legítimo
    fake_server_url = "https://127.0.0.1:8444/download"  # Servidor falso

    # Conectar a los servidores
    print("\n--- PROBANDO SERVIDOR LEGÍTIMO ---")
    connect_to_server(legit_server_url)

    print("\n--- PROBANDO SERVIDOR FALSO ---")
    connect_to_server(fake_server_url)
