
import subprocess
import os

def descargar_fragmento(url, start_time, end_time, output_filename):
    try:
        # Formatear los tiempos de inicio y fin en el formato requerido por ffmpeg
        start_time_str = f'{start_time // 3600:02}:{(start_time % 3600) // 60:02}:{start_time % 60:02}'
        end_time_str = f'{end_time // 3600:02}:{(end_time % 3600) // 60:02}:{end_time % 60:02}'
        
        # Obtener la ruta de la carpeta de descargas del usuario
        download_path = os.path.join(os.path.expanduser("~"), "Downloads\Videos", output_filename)
        
        # Ejecutar yt-dlp para descargar el fragmento especificado en la mejor calidad
        command = [
            'yt-dlp',
            '-f', 'bestvideo',
            '--external-downloader', 'ffmpeg',
            '--external-downloader-args', f'-ss {start_time_str} -to {end_time_str}',
            '-o', download_path,
            url
        ]
        
        subprocess.run(command, check=True)
        print(f'Fragmento guardado en: {download_path}')
    except subprocess.CalledProcessError as e:
        print(f'Error al ejecutar el comando: {e}')
    except Exception as e:
        print(f'Ocurrió un error: {e}')

if __name__ == "__main__":
    url = input('Introduce la URL del video de YouTube: ')
    start_time = int(input('Introduce el tiempo de inicio del fragmento (en segundos): '))
    end_time = int(input('Introduce el tiempo de fin del fragmento (en segundos): '))
    output_filename = input('Introduce el nombre del archivo de salida (con extensión .mp4): ')
    
    descargar_fragmento(url, start_time, end_time, output_filename)

