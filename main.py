import tkinter as tk
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

from threading import Thread
from ultralytics import YOLO

import ctypes
plt.style.use("seaborn-v0_8-whitegrid")

# Chamando a janela do aplicativo
class App(CTk):
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.main_frame = CTkFrame(self)
        self.main_frame.pack(expand=True, fill=BOTH)

# Função que configura a câmera a ser usada
def ConfigurarCamera():
    # Define a video capture object
    vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
  
    # Declare the width and height in variables
    width, height = 1079, 365
  
    # Set the width and height
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    return vid
  
# Função de abrir a câmera e mostrar no video_widget do app
def Open_Camera():
    global segmentou_imagem

    # Captura do vídeo frame por frame
    _, frame = vid.read()
    # Conversão de imagem de uma espaço de cores para o outro
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
  
    # Captura do frame mais atual e transformação dela para imagem
    captured_image = Image.fromarray(opencv_image)

    
    if(segmentou_imagem == 2):
        # Conversão da imagem capturada para photoimage
        photo_image = CTkImage(imagem_segmentada, size = (w_img, h_img))
        video_widget.configure(image=photo_image)
        segmentou_imagem = 0
    elif(segmentou_imagem == 0):
        thread_segmentar = Thread(target=segmentar_imagem, args=[captured_image])
        thread_segmentar.start()

    # Repetição do mesmo processo após 10 milisegundos
    video_widget.after(10, Open_Camera)

def Imagem_Video(e):
    global w_img, h_img 

    w_img = e.width - 50
    h_img = e.height - 50

    vid.set(cv2.CAP_PROP_FRAME_WIDTH, w_img)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, h_img)

    imagem_segmentada_resized = imagem_segmentada.resize((w_img, h_img), Image.LANCZOS)

    photo_image = CTkImage(imagem_segmentada_resized, size = (w_img, h_img))
    video_widget.configure(image=photo_image)

# Thread
def segmentar_imagem(imagem):
    global segmentou_imagem, imagem_segmentada
    segmentou_imagem = 1
    print("haha")
    results = model(imagem, verbose=False)
    print("bro")
    imagem_segmentada_plot = results[0].plot()
    imagem_segmentada = Image.fromarray(cv2.cvtColor(imagem_segmentada_plot, cv2.COLOR_BGR2RGBA))
    segmentou_imagem = 2

def CriacaoGrafico():
    queueTempo = deque([], maxlen = 15)
    queueDados = deque([], maxlen = 15)

    queueDados.append(2) 
    queueTempo.append("0")

    # To run GUI event loops
    fig = Figure(dpi=ORIGINAL_DPI)
    fig.set_size_inches(9.2, 3.2)
    ax = fig.add_subplot()

    fig.autofmt_xdate()
    linhaLineGraph, = ax.plot(list(queueTempo), list(queueDados))
    #plt.title("Diâmetro do cascão", fontsize=20)
    ax.set_xlabel("Horas")
    ax.set_ylabel("Diâmetro [mm]")

    
    return fig, ax, queueDados, queueTempo, linhaLineGraph

def GaugeGraph():
    color = ["#ee3d55", "#ee3d55", "#fabd57" , "#fabd57", "#4dab6d", "#4dab6d", "#4dab6d", "#4dab6d", "#4dab6d"]
    #values = [-40, -20, 0, 20, 40, 60, 80, 100]
    #color = ["#4dab6d", "#72c66e",  "#c1da64", "#f6ee54", "#fabd57", "#f36d54", "#ee3d55"]
    values = [80, 75, 70, 65, 60, 55, 50, 45, 40]

    fig = plt.figure(figsize=(4, 4))

    ax = fig.add_subplot(projection="polar")
    ax.bar(x = [0, 0.385, 0.77, 1.155, 1.54, 1.925, 2.31, 2.695], width=0.42, height=0.5, bottom=2, 
          color=color, align="edge")

    for loc, val in zip([0, 0.385, 0.77, 1.155, 1.54, 1.925, 2.31, 2.695, 3.08, 3,465], values):
        plt.annotate(val, xy=(loc, 2.525), ha="right" if val<=55 else "left")

    ax.set_axis_off()

    linhaGaugeGraph = ax.annotate("0", xytext=(0,0), xy=(0, 2.0),
                 arrowprops=dict(arrowstyle="wedge, tail_width= 0.5", color="black", shrinkA=0), 
                 bbox = dict(boxstyle="circle", facecolor="black", linewidth=2),
                 fontsize=25, color ="red", ha = "center"
                )

    #plt.title("Diâmetro da Lança", loc = "center", pad=20, fontsize=35, fontweight="bold")

    return fig, linhaGaugeGraph, ax

# Função para plot do gráfico de acordo com dados recebidos
def PlotarGraficoData(queueDados, queueTempo):

    # Declaração variáveis
    x = queueTempo
    y = queueDados
    
    # Gerãção e adição na lista de dados para teste
    numData = random.randrange(40, 80)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    colorLevel = ""
    if numData <= 60:
        colorLevel = "#4dab6d"
    elif numData >= 70:
        colorLevel = "#ee3d55"
    else:
        colorLevel = "#fabd57"

    xvalue = 3.465 - ((numData - 35) * 0.077)

    x.append(current_time)
    y.append(numData)

    # Atualização do range dos eixos x e y
    ax.set_ylim(min(list(y)) - 2, max(list(y)) + 2)
    ax.set_xlim(list(x)[0], list(x)[-1])

    linhaLineGraph.set_data(list(x), list(y))
    #linhaGaugeGraph.set(text=numData, color=colorLevel, arrowprops=dict(arrowstyle="wedge, tail_width= 0.5", color="black", shrinkA=0), x=xvalue)
    #axTESTE.annotate("0", xytext=(0,0), xy=(numData, 2.0),
    #             arrowprops=dict(arrowstyle="wedge, tail_width= 0.5", color="black", shrinkA=0), 
    #             bbox = dict(boxstyle="circle", facecolor="black", linewidth=2),
    #             fontsize=25, color =f"{colorLevel}", ha = "center"
    #            )

    #linhaGaugeGraph.set_position((xvalue, 2.0))

    # Desenhando o novo gráfico
    canvasLineGraph.draw()
    canvasGaugeGraph.draw()

    # Chamando a função recursiva de segundo em segundo para rodar a função novamente e continuar atualizando o gráfico
    canvasLineGraph.get_tk_widget().after(1000, PlotarGraficoData, y, x)

# Variáveis
# Definição do DPI original utilizado
ORIGINAL_DPI = 96.09458128078816
APP_WIDTH = 1000
APP_HEIGHT = 720
w_img, h_img = 30, 30
model = YOLO("yolov8m-seg.pt")
segmentou_imagem = 0

### Inicialização do app
app = App()

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x = (screen_width - APP_WIDTH ) / 2
y = (screen_height - APP_HEIGHT ) / 2

app.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{int(x)}+{int(y)}")

app.minsize(1000, 720)
app.resizable(1, 1)
app.title("DashMedidor")

ctypes.windll.shcore.SetProcessDpiAwareness(2)

# Configurar a câmera para o seu uso
vid = ConfigurarCamera()

app.columnconfigure(0, weight=1)
app.rowconfigure(1, weight=1)

### FRAME HEADER DA TELA
frameHeader = CTkFrame(app, height=100, fg_color='#a4a8ad', corner_radius=0, border_width=0)
frameHeader.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)

frameLogos = CTkFrame(frameHeader, fg_color='#a4a8ad', corner_radius=0, border_width=0)
frameLogos.pack(fill=X, expand=True, padx=100, pady=0)

frameLogos.columnconfigure(0, weight=1)
frameLogos.columnconfigure(1, weight=1)
frameLogos.columnconfigure(2, weight=1)

# As imagens das 3 logos sendo encaixadas no header
photo_image_ifes_logo = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), 'IFES_horizontal_logo.png')), size=(215.46, 86.184))
image_ifes_logo_label = CTkLabel(frameLogos, image=photo_image_ifes_logo, text="")
image_ifes_logo_label.grid(row=0, column=0)

photo_image_arcelor_logo = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), 'ArcelorMittal_logo.png')), size=(168, 69.12))
image_arcelor_logo_label = CTkLabel(frameLogos, image=photo_image_arcelor_logo, text="")
image_arcelor_logo_label.grid(row=0, column=1)

photo_image_oficinas_logo = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), 'Oficinas4-0_logo.png')), size=(163.84, 33.6))
image_oficinas_logo_label = CTkLabel(frameLogos, image=photo_image_oficinas_logo, text="")
image_oficinas_logo_label.grid(row=0, column=2)


### FRAME PRINCIPAL DA TELA
framePrincipal = CTkFrame(app, fg_color='#4f7d71', corner_radius=0, border_width=0)
framePrincipal.grid(row=1, column=0, sticky='nsew', padx=0, pady=0)

# Frame com widgets do frame principal da tela
frameCentral = CTkFrame(framePrincipal, fg_color='#4f7d71')
frameCentral.pack(fill=BOTH, expand=True, padx=10, pady=10)

frameCentral.rowconfigure(0, weight=1)
frameCentral.rowconfigure(1, weight=1)
frameCentral.columnconfigure(0, weight=2)
frameCentral.columnconfigure(1, weight=1)

# Criação dos frames da parte de cima
frameVideo = CTkFrame(frameCentral, fg_color="#a4a8ad", border_width=0, corner_radius=15)
frameVideo.grid(row=0, column=0, padx=(20, 20), pady=(0, 10), sticky='nsew')
frameVideo.pack_propagate(False)
#frameVideo.bind('<Configure>', Imagem_Video)

frameAlertGraph = CTkFrame(frameCentral, fg_color="#a4a8ad", border_width=0, corner_radius=15)
frameAlertGraph.grid(row=0, column=1, padx=(0, 20), pady=(0, 10), sticky='nsew')

# Criação dos frames da parte de baixo
frameDataGraph = CTkFrame(frameCentral, fg_color="#a4a8ad", border_width=0, corner_radius=15)
frameDataGraph.grid(row=1, columnspan=2, padx=(20, 20), pady=(10, 0), sticky='nsew')

# Criar o label do texto do vídeo e colocar em cima dele
#video_text_label = CTkLabel(frameVideo, text="Imagem Segmentada", font=("Arial", 23))
#video_text_label.grid(row=0, pady=3, padx=20, sticky='W')
#video_text_label.place(relx=.5, rely=.5, anchor="w", x=10)

# Criar o label do vídeo e mostrar no app
video_widget = CTkLabel(frameVideo, text="")
video_widget.pack(fill=BOTH, expand=True, padx=10, pady=10)

#Função para abrir ativar câmera e encaixar ela no app
#Open_Camera()

# Criação do gráfico e chamada da função para atualizá-la
figLineGraph, ax, queueDados, queueTempo, linhaLineGraph = CriacaoGrafico()
canvasLineGraph = FigureCanvasTkAgg(figLineGraph, frameDataGraph)
canvasLineGraph.draw()

toolbar = NavigationToolbar2Tk(canvasLineGraph, frameDataGraph, pack_toolbar=False)
toolbar.update()
canvasLineGraph.get_tk_widget().place(relx=.5, rely=.5, anchor='center')

figGaugeGraph, linhaGaugeGraph, axTESTE = GaugeGraph()
canvasGaugeGraph = FigureCanvasTkAgg(figGaugeGraph, frameAlertGraph)
canvasGaugeGraph.draw()
canvasGaugeGraph.get_tk_widget().place(relx=.5, rely=.5, anchor='center')

PlotarGraficoData(queueDados, queueTempo)

# Função para rodar o app
app.mainloop()