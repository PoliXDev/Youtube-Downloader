# Youtube Downloader 1.7 - por Daniel Ruiz Poli aka NoahKnox

from pytube import YouTube
from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os
import threading
import requests
from io import BytesIO
import customtkinter as ctk
import re
import time

# Configuración de tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Clase principal de la aplicación
class YouTubeDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("YouTube Downloader por Daniel Ruiz Poli aka NoahKnox - PoliXDev")
        self.geometry("800x600")
        
        # Variables
        self.video_url = ctk.StringVar()
        self.download_path = ctk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.format_var = ctk.StringVar(value="video")
        self.quality_var = ctk.StringVar(value="720p")
        self.video_info = None
        
        # Mostrar intro primero
        self.show_intro()
        
    def show_intro(self):
        # Frame de introducción
        intro_frame = ctk.CTkFrame(self)
        intro_frame.pack(fill=BOTH, expand=True)
        
        # Título de ConquerBlocks
        ctk.CTkLabel(
            intro_frame,
            text="MASTER FULL STACK",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#3498db"
        ).pack(pady=(80, 0))
        #Academia ConquerBlocks 
        ctk.CTkLabel(
            intro_frame,
            text="ACADEMIA CONQUERBLOCKS",
            font=ctk.CTkFont(size=42, weight="bold")
        ).pack(pady=(10, 30))
        
        # Información del proyecto
        ctk.CTkLabel(
            intro_frame,
            text="Proyecto: YOUTUBE DOWNLOADER",
            font=ctk.CTkFont(size=32),
            text_color="#2ecc71"
        ).pack(pady=10)
        #Desarrollado en Python 3.12
        ctk.CTkLabel(
            intro_frame,
            text="Desarrollado en Python 3.12",
            font=ctk.CTkFont(size=28),
            text_color="#95a5a6"
        ).pack(pady=5)
        
        # Créditos
        ctk.CTkLabel(
            intro_frame,
            text="Código escrito por:",
            font=ctk.CTkFont(size=24) 
        ).pack(pady=(30, 5))
        #Daniel Ruiz Poli
        ctk.CTkLabel(
            intro_frame,
            text="Daniel Ruiz Poli",
            font=ctk.CTkFont(size=36),
            text_color="#2ecc71"
        ).pack(pady=5)
        #GitHub: PoliXDev
        ctk.CTkLabel(
            intro_frame,
            text="GitHub: PoliXDev",
            font=ctk.CTkFont(size=28),
            text_color="#3498db"
        ).pack(pady=5)
        
         # Botón para continuar
        ctk.CTkButton(
            intro_frame,
            text="Continuar",
            command=lambda: self.show_main_app(intro_frame),
            height=40,
            font=ctk.CTkFont(size=20)
        ).pack(pady=(30, 0))
    
    # Mostrar la pantalla principal
    def show_main_app(self, intro_frame):
        # Destruir frame de intro
        intro_frame.destroy()
        # Crear widgets principales
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Título
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="YouTube Downloader",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(pady=10)
        
        # Frame para URL
        self.url_frame = ctk.CTkFrame(self.main_frame)
        self.url_frame.pack(fill=X, pady=10)
        
        #Pega aquí el enlace de YouTube
        self.url_entry = ctk.CTkEntry(
            self.url_frame,
            placeholder_text="Pega aquí el enlace de YouTube",
            textvariable=self.video_url,
            width=500,
            height=40
        )
        self.url_entry.pack(side=LEFT, padx=5)
        
        #Obtener Info
        self.fetch_button = ctk.CTkButton(
            self.url_frame,
            text="Obtener Info",
            command=self.fetch_video_info,
            width=100
        )
        self.fetch_button.pack(side=LEFT, padx=5)
        
        # Frame para información del video
        self.info_frame = ctk.CTkFrame(self.main_frame)
        self.info_frame.pack(fill=X, pady=10)
        
        # Thumbnail del video de YouTube
        self.thumbnail_label = ctk.CTkLabel(self.info_frame, text="")
        self.thumbnail_label.pack(side=LEFT, padx=10)
        
        # Información del video
        self.video_info_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.video_info_label.pack(side=LEFT, padx=10)
        
        # Frame para opciones
        self.options_frame = ctk.CTkFrame(self.main_frame)
        self.options_frame.pack(fill=X, pady=10)
        
        # Selector de formato
        self.format_label = ctk.CTkLabel(
            self.options_frame,
            text="Formato:",
            font=ctk.CTkFont(size=12)
        )
        self.format_label.pack(side=LEFT, padx=5)
        
        #Selector de formato
        self.format_menu = ctk.CTkOptionMenu(
            self.options_frame,
            values=["Video", "Audio"],
            variable=self.format_var,
            command=self.update_quality_options
        )
        self.format_menu.pack(side=LEFT, padx=5)
        
        # Selector de calidad
        self.quality_label = ctk.CTkLabel(
            self.options_frame,
            text="Calidad:",
            font=ctk.CTkFont(size=12)
        )
        self.quality_label.pack(side=LEFT, padx=5)
        
        #Selector de calidad
        self.quality_menu = ctk.CTkOptionMenu(
            self.options_frame,
            values=["1080p", "720p", "480p", "360p"],
            variable=self.quality_var
        )
        self.quality_menu.pack(side=LEFT, padx=5)
        
        # Frame para directorio
        self.dir_frame = ctk.CTkFrame(self.main_frame)
        self.dir_frame.pack(fill=X, pady=10)
        
        #Seleccionar carpeta
        self.dir_button = ctk.CTkButton(
            self.dir_frame,
            text="Seleccionar carpeta",
            command=self.select_directory
        )
        self.dir_button.pack(side=LEFT, padx=5)
        
        self.dir_label = ctk.CTkLabel(
            self.dir_frame,
            textvariable=self.download_path
        )
        self.dir_label.pack(side=LEFT, padx=5)
        
        # Barra de progreso
        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.pack(fill=X, pady=10)
        self.progress_bar.set(0)
        
        # Botón de descarga
        self.download_button = ctk.CTkButton(
            self.main_frame,
            text="Descargar",
            command=self.start_download,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.download_button.pack(pady=10)
        
        # Etiqueta de estado
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=5)
        
        # Crear un frame separado para el footer
        footer_frame = ctk.CTkFrame(self)
        footer_frame.pack(side=BOTTOM, fill=X, pady=(0, 5))
        
        # Texto de ConquerBlocks en el footer
        ctk.CTkLabel(
            footer_frame,
            text="Proyecto de Estudios - ConquerBlocks - Noviembre 2024",
            font=ctk.CTkFont(size=12),
            text_color="#95a5a6"
        ).pack(pady=2)

    def fetch_video_info(self):
        try:
            url = self.video_url.get()
            self.video_info = YouTube(url)
            
            # Obtener y mostrar thumbnail
            response = requests.get(self.video_info.thumbnail_url)
            img = Image.open(BytesIO(response.content))
            img = img.resize((120, 68))
            photo = ImageTk.PhotoImage(img)
            self.thumbnail_label.configure(image=photo)
            self.thumbnail_label.image = photo
            
            # Mostrar información
            info_text = f"Título: {self.video_info.title}\n"
            info_text += f"Duración: {self.video_info.length//60}:{self.video_info.length%60:02d}\n"
            info_text += f"Vistas: {self.video_info.views:,}"
            self.video_info_label.configure(text=info_text)
            
        except Exception as e:
            self.show_message(f"Error: {str(e)}", "error")

    # Actualizar opciones de calidad
    def update_quality_options(self, choice):
        if choice == "Audio":
            self.quality_menu.configure(values=["320kbps", "256kbps", "128kbps"])
            self.quality_var.set("128kbps")
        else:
            self.quality_menu.configure(values=["1080p", "720p", "480p", "360p"])
            self.quality_var.set("720p")

    # Seleccionar directorio
    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.download_path.set(directory)

    # Iniciar descarga
    def start_download(self):
        if not self.video_info:
            self.show_message("Por favor, primero obtén la información del video", "error")
            return
        
        threading.Thread(target=self.download_video, daemon=True).start()

    # Descargar video
    def download_video(self):
        try:
            self.download_button.configure(state="disabled")
            self.progress_bar.set(0)
            self.show_message("Iniciando descarga...", "info")
            
            #Aplicar parche para el error 403 (No autorizado)
            patch_cipher()
            
            # Crear objeto YouTube con opciones adicionales
            self.video_info = YouTube(
                self.video_url.get(),
                use_oauth=True,
                allow_oauth_cache=True,
                on_progress_callback=self.on_progress
            )
            
            # Intentar múltiples veces si es necesario
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    if self.format_var.get().lower() == "audio":
                        stream = self.video_info.streams.get_audio_only()
                    else:
                        stream = self.video_info.streams.filter(
                            progressive=True,
                            resolution=self.quality_var.get()
                        ).first()
                    
                    if not stream:
                        self.show_message("Calidad no disponible para este video", "error")
                        return
                    
                    # Descargar con timeout
                    stream.download(
                        output_path=self.download_path.get(),
                        timeout=30
                    )
                    self.progress_bar.set(1)
                    self.show_message("¡Descarga completada con éxito!", "success")
                    break
                #Si hay un error, esperar 1 segundo antes de reintentar
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(1)
                
        except Exception as e:
            self.show_message(f"Error en la descarga: {str(e)}", "error")
        finally:
            self.download_button.configure(state="normal")

    # Agregar función para el progreso
    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.progress_bar.set(percentage / 100)

    # Mostrar mensaje
    def show_message(self, message, type_="info"):
        colors = {
            "error": "red",
            "success": "green",
            "info": "white"
        }
        self.status_label.configure(text=message, text_color=colors.get(type_, "white"))
        
#Parche para el error 403 (No autorizado) no deja descargar el video
def patch_cipher():
    """Parche para el error 403"""
    from pytube import cipher
    from pytube.cipher import get_initial_function_name as get_name

    def new_get_initial_function_name(js: str) -> str:
        try:
            return get_name(js)
        except:
            # Patrón de respaldo si falla el método original
            pattern = r'(?:^|,)\s*([a-zA-Z$][a-zA-Z0-9$]+):\bfunction\b\s*\(\s*a\s*\)\s*{\s*a\s*=\s*a\.split\(\s*""\s*\)'
            match = re.search(pattern, js)
            if match:
                return match.group(1)
            raise

    cipher.get_initial_function_name = new_get_initial_function_name

# Ejecutar la aplicación
if __name__ == "__main__":
    app = YouTubeDownloader()
    app.mainloop()






















