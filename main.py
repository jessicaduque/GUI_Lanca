import tkinter as tk
from customtkinter import *

import cv2
from PIL import Image, ImageTk

from random import randrange

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
    width, height = 440, 180
  
    # Set the width and height
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    return vid
  
### Inicialização
app = App()
app.geometry("1200x720")
app.resizable(0, 0)
app.title("DashMedidor")
app.configure(bg='#ebebeb')
# Configurar a câmera para o seu uso
vid = ConfigurarCamera()

# Frame central da tela
frameCentral = CTkFrame(app, fg_color='#f5f3ee')
frameCentral.place(relx=.5, rely=.5, anchor='center')

# Divisão da tela em duas partes (cima e baixo)
frameCima = CTkFrame(frameCentral, fg_color='#f5f3ee')
frameCima.grid(row=0, column=0, padx=10,  pady=10)

frameBaixo = CTkFrame(frameCentral, fg_color='#f5f3ee')
frameBaixo.grid(row=1, column=0, padx=10,  pady=10)

# Criação dos frames da parte de cima
frameVideo = CTkFrame(frameCima, width=500, height=250, fg_color="white", border_color="gray", border_width=2, corner_radius=15)
frameVideo.grid(row=0, column=0, padx=10,  pady=5)
# Para frame do vídeo não adaptar tamanho aos componentes dentro
frameVideo.grid_propagate(False)

frameAlertGraph = CTkFrame(frameCima, width=250, height=250, fg_color="white", border_color="gray", border_width=2, corner_radius=15)
frameAlertGraph.grid(row=0, column=1, padx=10,  pady=5)
frameAlertGraph.grid_propagate(False)

# Criação dos frames da parte de baixo
frameDataGraph = CTkFrame(frameBaixo, width=760, height=220, fg_color="white", border_color="gray", border_width=2, corner_radius=15)
frameDataGraph.grid(row=0, column=0, padx=10,  pady=5)


# Criar o label do texto do vídeo e colocar em cima dele
video_text_label = CTkLabel(frameVideo, text="Imagem Segmentada", font=("Arial", 23))
video_text_label.grid(row=0, pady=3, padx=10, sticky='W')

# Criar o label do vídeo e mostrar no app
video_widget = CTkLabel(frameVideo, text="")
video_widget.grid(row=1, pady=3, padx=10)

# Função de abrir a câmera e mostrar no video_widget do app
def open_camera(frameCount):
    # Captura do vídeo frame por frame
    _, frame = vid.read()
  
    frameCount += 1

    if (frameCount == 10):
        numData = randrange(10, 30)
        frameCount = 0

    # Convert image from one color space to other
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
  
    # Capture the latest frame and transform to image
    captured_image = Image.fromarray(opencv_image)

    # Convert captured image to photoimage
    photo_image = CTkImage(captured_image, size=(480,200))

    # Displaying photoimage in the label
    video_widget.photo_image = photo_image
  
    # Configure image in the label
    video_widget.configure(image=photo_image)
  
    # Repeat the same process after every 10 seconds
    video_widget.after(10, open_camera, frameCount)

# Inicializa variável para aleatorizar dados
frameCount = int()

#Função para abrir ativar câmera e encaixar ela no app
open_camera(frameCount)

# Função para rodar o app
app.mainloop()