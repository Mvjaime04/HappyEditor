import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter
import cv2
import threading
import os
import subprocess

class EditorMultimedia:
    def __init__(self, root):
        self.root = root
        self.root.title("HappyEditor")
        self.root.geometry("800x600")

        # Variables
        self.imagen = None
        self.video_clip = None
        self.video_path = None
        self.video_recortado_path = None
        self.audio_path = "temp_audio.mp3"
        self.playing = False

        # Interfaz gráfica
        self.boton_cargar_foto = tk.Button(root, text="Cargar Foto", command=self.cargar_foto)
        self.boton_cargar_foto.pack(pady=10)

        self.boton_cargar_video = tk.Button(root, text="Cargar Video", command=self.cargar_video)
        self.boton_cargar_video.pack(pady=10)

        self.boton_aplicar_filtro = tk.Button(root, text="Aplicar Filtro (Foto)", command=self.aplicar_filtro)
        self.boton_aplicar_filtro.pack(pady=10)

        self.label_inicio = tk.Label(root, text="Inicio (segundos):")
        self.label_inicio.pack()
        self.entry_inicio = tk.Entry(root)
        self.entry_inicio.pack()

        self.label_fin = tk.Label(root, text="Fin (segundos):")
        self.label_fin.pack()
        self.entry_fin = tk.Entry(root)
        self.entry_fin.pack()

        self.boton_recortar_video = tk.Button(root, text="Recortar Video", command=self.recortar_video)
        self.boton_recortar_video.pack(pady=10)

        self.boton_guardar = tk.Button(root, text="Guardar", command=self.guardar_archivo)
        self.boton_guardar.pack(pady=10)

        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.toggle_video_playback)

    def cargar_foto(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg;*.png;*.jpeg")])
        if ruta:
            self.imagen = Image.open(ruta)
            self.imagen.thumbnail((640, 480))
            self.mostrar_imagen()

    def cargar_video(self):
        ruta = filedialog.askopenfilename(filetypes=[("Videos", "*.mp4;*.avi;*.mov")])
        if ruta:
            self.video_path = ruta
            self.video_clip = cv2.VideoCapture(ruta)
            self.extraer_audio()
            self.mostrar_video()

    def extraer_audio(self):
        # Extraer el audio del video y guardarlo en un archivo temporal usando ffmpeg
        comando = f"ffmpeg -i \"{self.video_path}\" -q:a 0 -map a \"{self.audio_path}\" -y"
        subprocess.run(comando, shell=True)

    def aplicar_filtro(self):
        if self.imagen:
            self.imagen = self.imagen.filter(ImageFilter.BLUR)  # Ejemplo de filtro
            self.mostrar_imagen()
        else:
            messagebox.showwarning("Advertencia", "Primero carga una foto.")

    def recortar_video(self):
        if self.video_clip:
            try:
                inicio = float(self.entry_inicio.get())
                fin = float(self.entry_fin.get())
            except ValueError:
                messagebox.showwarning("Advertencia", "Por favor, ingresa valores numéricos válidos para inicio y fin.")
                return

            fps = self.video_clip.get(cv2.CAP_PROP_FPS)
            inicio_frame = int(inicio * fps)
            fin_frame = int(fin * fps)

            ruta_guardado = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4", "*.mp4")])
            if not ruta_guardado:
                return

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(ruta_guardado, fourcc, fps, (int(self.video_clip.get(3)), int(self.video_clip.get(4))))

            self.video_clip.set(cv2.CAP_PROP_POS_FRAMES, inicio_frame)
            for i in range(inicio_frame, fin_frame):
                ret, frame = self.video_clip.read()
                if not ret:
                    break
                out.write(frame)

            out.release()
            self.video_clip.release()
            self.video_recortado_path = ruta_guardado
            messagebox.showinfo("Info", f"Video recortado de {inicio} a {fin} segundos.")
        else:
            messagebox.showwarning("Advertencia", "Primero carga un video.")

    def guardar_archivo(self):
        if self.imagen:
            ruta = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
            if ruta:
                self.imagen.save(ruta)
                messagebox.showinfo("Info", "Foto guardada correctamente.")
        elif self.video_recortado_path:
            ruta = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4", "*.mp4")])
            if ruta:
                cv2.VideoCapture(self.video_recortado_path).release()
                messagebox.showinfo("Info", "Video guardado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "No hay archivo para guardar.")

    def mostrar_imagen(self):
        if self.imagen:
            foto = ImageTk.PhotoImage(self.imagen)
            self.canvas.create_image(320, 240, image=foto)
            self.canvas.image = foto

    def mostrar_video(self):
        if self.video_clip:
            ret, frame = self.video_clip.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                imagen = Image.fromarray(frame)
                imagen.thumbnail((640, 480))
                foto = ImageTk.PhotoImage(imagen)
                self.canvas.create_image(320, 240, image=foto)
                self.canvas.image = foto

    def toggle_video_playback(self, event):
        if self.playing:
            self.playing = False
        else:
            self.playing = True
            threading.Thread(target=self.reproducir_video).start()

    def reproducir_video(self):
        if self.video_path:
            audio_thread = threading.Thread(target=self.reproducir_audio)
            audio_thread.start()
            while self.playing:
                ret, frame = self.video_clip.read()
                if not ret:
                    break
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                imagen = Image.fromarray(frame)
                imagen.thumbnail((640, 480))
                foto = ImageTk.PhotoImage(imagen)
                self.canvas.create_image(320, 240, image=foto)
                self.canvas.image = foto
                self.root.update()
            self.video_clip.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.playing = False

    def reproducir_audio(self):
        comando = f"ffplay -nodisp -autoexit \"{self.audio_path}\""
        subprocess.run(comando, shell=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = EditorMultimedia(root)
    root.mainloop()

    # Eliminar el archivo de audio temporal al salir
    if os.path.exists("temp_audio.mp3"):
        os.remove("temp_audio.mp3")

