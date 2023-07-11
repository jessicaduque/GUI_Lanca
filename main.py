import queue
import tkinter as tk
from customtkinter import *

import cv2
from PIL import Image, ImageTk

import random
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
#plt.style.use("seaborn")
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
def Open_Camera(frameCount):
    # Captura do vídeo frame por frame
    _, frame = vid.read()

    # Converção de imagem de uma espaço de cores para o outro
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
  
    # Captura do frame mais atual e transformação dela para imagem
    captured_image = Image.fromarray(opencv_image)

    # Converção da imagem capturada para photoimage
    photo_image = CTkImage(captured_image, size=(480,200))

    # Definindo o photoimage do label
    video_widget.photo_image = photo_image
  
    # Configurando a imagem no label
    video_widget.configure(image=photo_image)
  
    # Repetiçãoo do mesmo processo apóos 10 milisegundos
    video_widget.after(10, Open_Camera, frameCount)

def CriacaoGrafico():
    queueTempo = deque([], maxlen = 15)
    queueDados = deque([], maxlen = 15)

    queueDados.append(0) 
    queueTempo.append("0")

    # to run GUI event loop
    fig, ax = plt.subplots()
    linha, = ax.plot(list(queueTempo), list(queueDados))
    plt.title("Diâmetro do cascão", fontsize=20)
    plt.xlabel("Horas")
    plt.ylabel("Diâmetro")

    return fig, queueDados, queueTempo, linha

# Função para plot do gráfico de acordo com dados recebidos
def PlotarGraficoData(queueDados, queueTempo):

    # Declaração variáveis
    x = queueTempo
    y = queueDados
    
    # Gerãção e adição na lista de dados para teste
    numData = random.randrange(10, 30)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    x.append(current_time)
    y.append(numData)

    # Atualização do range dos eixos x e y
    plt.ylim(min(list(y)), max(list(y)))
    plt.xlim(list(x)[0], list(x)[-1])

    # Atualização dos dados do eixo x e y
    linha.set_xdata(list(x))
    linha.set_ydata(list(y))

    # Desenhando o novo gráfico
    fig.canvas.draw()
    
    # Chamando a função recursiva de segundo em segundo para rodar a função novamente e continuar atualizando o gráfico
    canvas.get_tk_widget().after(1000, PlotarGraficoData, y, x)

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
Open_Camera(frameCount)

# Criação do gráfico e chamada da função para atualizá-la
fig, queueDados, queueTempo, linha = CriacaoGrafico()
canvas = FigureCanvasTkAgg(fig, app)
canvas.get_tk_widget().grid(row=0, column=1)
PlotarGraficoData(queueDados, queueTempo)

# Função para rodar o app
app.mainloop()