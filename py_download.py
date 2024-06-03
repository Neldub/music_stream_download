import importlib
import subprocess

def install(package):
    subprocess.check_call(["pip", "install", package])

def check_libraries():
    libraries = ['pytube', 'moviepy', 'yt-dlp', 'savify', 'tkinter']
    for lib in libraries:
        try:
            importlib.import_module(lib)
        except ImportError:
            print(f"{lib} no está instalada. Se procederá a instalarla...")
            install(lib)

check_libraries()

import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube
from moviepy.editor import AudioFileClip
from yt_dlp import YoutubeDL
from savify import Savify
from savify.types import Type, Format

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Descargar audio")

        # Definir el tamaño de la ventana
        self.root.geometry("400x400")

        # Cuadro de texto para la URL
        self.url_label = tk.Label(self.root, text="Introduce la URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self.root, width=50)
        self.url_entry.pack()

        # Botón para seleccionar el directorio de descarga
        self.directory_label = tk.Label(self.root, text="Selecciona el directorio de descarga:")
        self.directory_label.pack()

        self.directory_path = tk.StringVar()
        self.directory_entry = tk.Entry(self.root, width=50, textvariable=self.directory_path)
        self.directory_entry.pack()

        self.directory_button = tk.Button(self.root, text="Seleccionar", command=self.select_directory)
        self.directory_button.pack()

        # Botón para seleccionar el archivo de credenciales
        self.credentials_label = tk.Label(self.root, text="Selecciona el archivo de credenciales (solo para Spotify):")
        self.credentials_label.pack()

        self.credentials_path = tk.StringVar()
        self.credentials_entry = tk.Entry(self.root, width=50, textvariable=self.credentials_path)
        self.credentials_entry.pack()

        self.credentials_button = tk.Button(self.root, text="Seleccionar", command=self.select_credentials)
        self.credentials_button.pack()

        # Botón para descargar el audio
        self.download_button = tk.Button(self.root, text="Descargar", command=self.download)
        self.download_button.pack()

    def select_directory(self):
        # Mostrar el diálogo de selección de directorio y guardar la ruta seleccionada
        directory_path = filedialog.askdirectory()
        self.directory_path.set(directory_path)

    def select_credentials(self):
        # Mostrar el diálogo de selección de archivo y guardar la ruta seleccionada
        credentials_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        self.credentials_path.set(credentials_path)

    def identify_service(self, url):
        if 'youtube.com' in url or 'youtu.be' in url:
            return 'youtube'
        elif 'soundcloud.com' in url:
            return 'soundcloud'
        elif 'spotify.com' in url:
            return 'spotify'
        else:
            return None

    def download(self):
        try:
            # Obtener la URL y el directorio de descarga
            url = self.url_entry.get()
            directory = self.directory_path.get()
            credentials_file = self.credentials_path.get()

            if not url or not directory:
                messagebox.showerror("Error", "Debe proporcionar una URL y seleccionar un directorio.")
                return

            service = self.identify_service(url)
            if service == 'youtube':
                self.download_from_youtube(url, directory)
            elif service == 'soundcloud':
                self.download_from_soundcloud(url, directory)
            elif service == 'spotify':
                if not credentials_file:
                    messagebox.showerror("Error", "Debe seleccionar un archivo de credenciales para Spotify.")
                    return
                self.download_from_spotify(url, directory, credentials_file)
            else:
                messagebox.showerror("Error", "No se pudo identificar el servicio de la URL proporcionada.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

    def download_from_youtube(self, url, directory):
        # Descargar el video
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        video.download(directory)

        # Convertir el video descargado a MP3
        video_path = os.path.join(directory, video.default_filename)
        mp3_path = os.path.splitext(video_path)[0] + '.mp3'
        video_clip = AudioFileClip(video_path)
        video_clip.write_audiofile(mp3_path)

        # Eliminar el video original
        os.remove(video_path)

        messagebox.showinfo("Descarga completa", "El audio de YouTube se ha descargado correctamente.")

    def download_from_soundcloud(self, url, directory):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(directory, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        messagebox.showinfo("Descarga completa", "El audio de SoundCloud se ha descargado correctamente.")

    def download_from_spotify(self, url, directory, credentials_file):
        # Cargar las credenciales de la API
        with open(credentials_file, 'r') as f:
            credentials = json.load(f)

        savify = Savify(api_credentials=credentials, quality=Type.MP3_320, download_format=Format.MP3, output_path=directory)
        savify.download(url)

        messagebox.showinfo("Descarga completa", "El audio de Spotify se ha descargado correctamente.")

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
