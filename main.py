import tkinter as tk
from customtkinter import *

import cv2
from PIL import Image, ImageTk

# Chamando a janela do aplicativo
class App(CTk):
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)

        self.main_frame = CTkFrame(self)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

# Função que configura a câmera a ser usada
def ConfigurarCamera():
    # Define a video capture object
    vid = cv2.VideoCapture(0)
  
    # Declare the width and height in variables
    width, height = 800, 600
  
    # Set the width and height
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    return vid

# Função de abrir a câmera e mostrar no video_widget do app
def open_camera():
  
    # Captura do vídeo frame por frame
    _, frame = vid.read()
  
    # Convert image from one color space to other
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
  
    # Capture the latest frame and transform to image
    captured_image = Image.fromarray(opencv_image)

    # Convert captured image to photoimage
    photo_image = CTkImage(captured_image, size=(800, 600))

    # Displaying photoimage in the label
    video_widget.photo_image = photo_image
  
    # Configure image in the label
    video_widget.configure(image=photo_image)
  
    # Repeat the same process after every 10 seconds
    video_widget.after(10, open_camera)

app = App()
app.geometry("960x540") 
app.title("DashMedidor")

# Configurar a câmera para o seu uso
vid = ConfigurarCamera()

# Criar o label e mostrar no app
video_widget = CTkLabel(app, text="")
video_widget.pack()
  
# Função para abrir ativar câmera e encaixar ela no app
open_camera()

# Função para rodar app
app.mainloop()