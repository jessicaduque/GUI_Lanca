import queue
import tkinter as tk
from customtkinter import *

import cv2
from PIL import Image, ImageTk

import random
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from collections import deque
from  matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
  
# Função de abrir a câmera e mostrar no video_widget do app
def open_camera(frameCount):
    # Captura do vídeo frame por frame
    _, frame = vid.read()
  
    frameCount += 1

    if (frameCount == 30):
        numData = random.randrange(10, 30)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
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
  
    # Repeat the same process after every 10 miliseconds
    video_widget.after(10, open_camera, frameCount)

#def createQueue(data, q):
#    queue = deque([], maxlen=15)
#    queue.append(data)

#    return q

# Função para plot do gráfico de acordo com dados recebidos
def PlotarGraficoData(queueX, queueY, queueDados, queueTempo):
    numData = random.randrange(10, 30)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    queueX.append(current_time)
    print(queueX[0])
    print(type(current_time))

    queueY.append(numData)
    print(queueY[0])


    x = queueTempo
    y = queueDados

    y[3] = y[3] + 1

    # updating data values
    linha.set_xdata(x)
    linha.set_ydata(y)
    plt.ylim(0, 31)
    #for i in y:
    #   plt.ylim(0, i)
    # drawing updated values
    fig.canvas.draw()
    
    canvas.get_tk_widget().after(1000, PlotarGraficoData, queueX, queueY, queueDados, queueTempo)


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

# Inicializa variável para aleatorizar dados
frameCount = int()

#Função para abrir ativar câmera e encaixar ela no app
open_camera(frameCount)



### Criação do gráfico
queueX = deque([], maxlen = 15)
queueY = deque([], maxlen = 15)

queueDados = [1, 2, 3, 6, 7]
queueTempo = ["0.1", "0.2", "0.3", "0.4", "0.5"]

# to run GUI event loop
fig, ax = plt.subplots()
linha, = ax.plot(queueTempo, queueDados)
plt.title("Diâmetro do cascão", fontsize=20)
plt.xlabel("Horas")
plt.ylabel("Diâmetro")

canvas = FigureCanvasTkAgg(fig, app)
canvas.get_tk_widget().grid(row=0, column=1)
PlotarGraficoData(queueX, queueY, queueDados, queueTempo)

# Função para rodar o app
app.mainloop()