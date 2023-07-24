import tkinter as tk
import sqlite3
from customtkinter import *

import cv2
from PIL import Image, ImageTk

import random
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from collections import deque
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from database import dbAdd, dbShow

plt.style.use("seaborn-v0_8-whitegrid")

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
    width, height = 585, 250
  
    # Set the width and height
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    return vid
  
# Função de abrir a câmera e mostrar no video_widget do app
def Open_Camera():
    # Captura do vídeo frame por frame
    _, frame = vid.read()

    # Converção de imagem de uma espaço de cores para o outro
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
  
    # Captura do frame mais atual e transformação dela para imagem
    captured_image = Image.fromarray(opencv_image)

    # Converção da imagem capturada para photoimage
    photo_image = CTkImage(captured_image, size=(585,250))

    # Definindo o photoimage do label
    video_widget.photo_image = photo_image
  
    # Configurando a imagem no label
    video_widget.configure(image=photo_image)
  
    # Repetiçãoo do mesmo processo apóos 10 milisegundos
    video_widget.after(10, Open_Camera)

def CriacaoGrafico():
    queueTempo = deque([], maxlen = 15)
    queueDados = deque([], maxlen = 15)

    queueDados.append(2) 
    queueTempo.append("0")

    # to run GUI event loop
    fig = Figure(figsize=(11, 4), dpi = 100)
    #fig, ax = plt.subplots()
    ax = fig.add_subplot()

    print("Dot per inch(DPI) for the figure is: ", fig.dpi)
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    print("Axis sizes are(in pixels):", width, height)

    fig.autofmt_xdate()
    linha, = ax.plot(list(queueTempo), list(queueDados))
    #plt.title("Diâmetro do cascão", fontsize=20)
    ax.set_xlabel("Horas")
    ax.set_ylabel("Diâmetro [mm]")
    #plt.xlabel("Horas")
    #plt.ylabel("Diâmetro [mm]")

    #fig.set_figwidth(11)
    #fig.set_figheight(4)
    

    return fig, ax, queueDados, queueTempo, linha

# Função para plot do gráfico de acordo com dados recebidos
def PlotarGraficoData(queueDados, queueTempo):

    # Declaração variáveis
    x = queueTempo
    y = queueDados
    
    # Geração e adição na lista de dados para teste
    numData = random.randrange(40, 80)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    dbAdd(numData, current_time)
    #dbShow()

    x.append(current_time)
    y.append(numData)

    # Atualização do range dos eixos x e y
    ax.set_ylim(min(list(y)) - 2, max(list(y)) + 2)
    ax.set_xlim(list(x)[0], list(x)[-1])

    linha.set_data(list(x), list(y))

    # Desenhando o novo gráfico
    canvas.draw()
    
    # Chamando a função recursiva de segundo em segundo para rodar a função novamente e continuar atualizando o gráfico
    #GaugeGraph()
    canvas.get_tk_widget().after(1000, PlotarGraficoData, y, x)

def GaugeGraph():
    color = ["#ee3d55", "#ee3d55", "#fabd57" , "#fabd57", "#4dab6d", "#4dab6d", "#4dab6d", "#4dab6d", "#4dab6d"]
    #values = [-40, -20, 0, 20, 40, 60, 80, 100]
    #color = ["#4dab6d", "#72c66e",  "#c1da64", "#f6ee54", "#fabd57", "#f36d54", "#ee3d55"]
    values = [80, 75, 70, 65, 60, 55, 50, 45 , 40]

    fig = plt.figure(figsize=(18, 18))

    ax = fig.add_subplot(projection="polar")
    ax.bar(x = [0, 0.385, 0.77, 1.155, 1.54, 1.925, 2.31, 2.695], width=0.42, height=0.5, bottom=2, 
          color=color, align="edge")

    for loc, val in zip([0, 0.385, 0.77, 1.155, 1.54, 1.925, 2.31, 2.695, 3.08, 3,465], values):
        plt.annotate(val, xy=(loc, 2.525), ha="right" if val<=55 else "left")

    numData = random.randrange(40, 80)
    xvalue = 3.465 - ((numData - 35) * 0.077)
    print(f"n = {numData} v = {xvalue}")

    if numData <= 60:
        colorLevel = "#4dab6d"
    elif numData >= 70:
        colorLevel = "#ee3d55"
    else:
        colorLevel = "#fabd57"

    plt.annotate(f"{numData}", xytext=(0,0), xy=(xvalue, 2.0),
                 arrowprops=dict(arrowstyle="wedge, tail_width= 0.5", color="black", shrinkA=0), 
                 bbox = dict(boxstyle="circle", facecolor="black", linewidth=2),
                 fontsize=25, color =f"{colorLevel}", ha = "center"
                )

    plt.title("Diâmetro da Lança", loc = "center", pad=20, fontsize=35, fontweight="bold")

    ax.set_axis_off()
    fig.show()

    return fig

### Inicialização
app = App()

app_width = 1000
app_height = 720

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x = (screen_width - app_width ) / 2
y = (screen_height - app_height ) / 2

print(x)
print(y)

print(app.winfo_screenwidth())
print(app.winfo_screenheight())

app.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
app.resizable(0, 0)
app.title("DashMedidor")
app.configure(bg='#ebebeb')
# Configurar a câmera para o seu uso
vid = ConfigurarCamera()
#GaugeGraph()

print(screen_width, screen_height)

# Frame central da tela
frameCentral = CTkFrame(app, fg_color='#f5f3ee')
frameCentral.place(relx=.5, rely=.5, anchor='center')

# Divisão da tela em duas partes (cima e baixo)
frameCima = CTkFrame(frameCentral, fg_color='#f5f3ee')
frameCima.grid(row=0, column=0, padx=10,  pady=10)

#frameBaixo = CTkFrame(frameCentral, fg_color='#f5f3ee')
frameBaixo = CTkFrame(frameCentral, fg_color='red')
frameBaixo.grid(row=1, column=0, padx=10,  pady=10)

# Criação dos frames da parte de cima
frameVideo = CTkFrame(frameCima, width=605, height=270, fg_color="white", border_color="gray", border_width=2, corner_radius=15)
frameVideo.grid(row=0, column=0, padx=10,  pady=5)
# Para frame do vídeo não adaptar tamanho aos componentes dentro
frameVideo.grid_propagate(False)

frameAlertGraph = CTkFrame(frameCima, width=285, height=270, fg_color="white", border_color="gray", border_width=2, corner_radius=15)
frameAlertGraph.grid(row=0, column=1, padx=10,  pady=5)
frameAlertGraph.grid_propagate(False)

# Criação dos frames da parte de baixo
frameDataGraph = CTkFrame(frameBaixo, width=1000, height=330, fg_color="white", border_color="gray", border_width=2, corner_radius=15)
#frameDataGraph = CTkFrame(frameBaixo, fg_color="white", border_color="gray", border_width=2, corner_radius=15)
frameDataGraph.grid(row=0, column=0, padx=10,  pady=5)
frameDataGraph.grid_propagate(False)

# Criar o label do texto do vídeo e colocar em cima dele
#video_text_label = CTkLabel(frameVideo, text="Imagem Segmentada", font=("Arial", 23))
#video_text_label.grid(row=0, pady=3, padx=20, sticky='W')
#video_text_label.place(relx=.5, rely=.5, anchor="w", x=10)

# Criar o label do vídeo e mostrar no app
video_widget = CTkLabel(frameVideo, text="")
#video_widget.grid(row=1, pady=3, padx=20)
video_widget.place(relx=.5, rely=.5, anchor="center")

#Função para abrir ativar câmera e encaixar ela no app
Open_Camera()

# Criação do gráfico e chamada da função para atualizá-la
fig, ax, queueDados, queueTempo, linha = CriacaoGrafico()
canvas = FigureCanvasTkAgg(fig, frameDataGraph)
canvas.draw()
#canvas.get_tk_widget().grid(pady=5, padx=5)

toolbar = NavigationToolbar2Tk(canvas, frameDataGraph, pack_toolbar=False)
toolbar.update()

#canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
canvas.get_tk_widget().place(relx=.5, rely=.5, anchor='center')

PlotarGraficoData(queueDados, queueTempo)

# Criação do gráfico de calibre e chamada da função para atualizá-la
coresGrafCal = ['#4dab6d', 'f6ee54', 'ee4d55']
valores = [0, 8, 15, 30]
#valor
# Função para rodar o app
app.mainloop()