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
from database import dbAdd, dbShow
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

    video_path = 'video_sample.mp4'
    cap = cv2.VideoCapture(video_path)


    #return cap
    return vid
  
# Função de abrir a câmera e mostrar no video_widget do app
def Open_Camera():
    
    thread_segmentar = Thread(target=segmentar_imagem)
    thread_segmentar.daemon
    thread_segmentar.start()
    # Espera thread terminar
    thread_segmentar.join()
    photo_image = CTkImage(imagem_segmentada, size = (w_img, h_img))
    video_widget.configure(image=photo_image)
    # Repetição do mesmo processo após 10 milisegundos
    video_widget.after(10, Open_Camera)

def Imagem_Video(e):
    global w_img, h_img 

    w_img = e.width - 50
    h_img = e.height - 50

    imagem_segmentada_resized = imagem_segmentada.resize((w_img, h_img), Image.LANCZOS)

    photo_image = CTkImage(imagem_segmentada_resized, size = (w_img, h_img))
    video_widget.configure(image=photo_image)


    thread_res_cam = Thread(target=redefinir_res_cam)
    thread_res_cam.daemon
    thread_res_cam.start()

def CriacaoGrafico(queueTempo, queueDados):

    numData = random.randrange(40, 80)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    dbAdd(numData, current_time)
    #dbShow()

    LineGraph(numData, current_time, queueTempo, queueDados)

    DataGraphImage = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), 'imagens/graphDiametro.png')), size=(1300 * 0.7, 450 * 0.7))
    DataGraphLabel.configure(image=DataGraphImage)

    GaugeGraph(numData)

    AlertGraphImage = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), 'imagens/gaugeDiametro.png')), size=(400 * 0.7, 250 * 0.7))
    AlertGraphLabel.configure(image=AlertGraphImage)

    # Chamando a função recursiva de segundo em segundo para rodar a função novamente e continuar atualizando o gráfico
    AlertGraphLabel.after(1000, CriacaoGrafico, queueTempo, queueDados)

def GaugeGraph(numData):
    os.remove("imagens\gaugeDiametro.png")
    color = ["#ee3d55", "#ee3d55", "#fabd57" , "#fabd57", "#4dab6d", "#4dab6d", "#4dab6d", "#4dab6d", "#4dab6d"]
    #values = [-40, -20, 0, 20, 40, 60, 80, 100]
    #color = ["#4dab6d", "#72c66e",  "#c1da64", "#f6ee54", "#fabd57", "#f36d54", "#ee3d55"]
    values = [80, 75, 70, 65, 60, 55, 50, 45, 40]

    colorLevel = ""

    if numData < 60:
        colorLevel = "#4dab6d"
    elif numData >= 70:
        colorLevel = "#ee3d55"
    else:
        colorLevel = "#fabd57"

    xvalue = 3.465 - ((numData - 35) * 0.077)

    fig = plt.figure(figsize=(4, 4))

    axGauge = fig.add_subplot(projection="polar")
    axGauge.bar(x = [0, 0.385, 0.77, 1.155, 1.54, 1.925, 2.31, 2.695], width=0.42, height=0.5, bottom=2, 
          color=color, align="edge")

    for loc, val in zip([0, 0.385, 0.77, 1.155, 1.54, 1.925, 2.31, 2.695, 3.08, 3,465], values):
        plt.annotate(val, xy=(loc, 2.525), ha="right" if val<=55 else "left")

    axGauge.set_axis_off()

    linhaGaugeGraph = axGauge.annotate(f"{numData}", xytext=(0,0), xy=(xvalue,2.0),
                 arrowprops=dict(arrowstyle="wedge, tail_width= 0.5", color="black", shrinkA=0), 
                 bbox = dict(boxstyle="circle", facecolor="black", linewidth=2,),
                 fontsize=25, color =f"{colorLevel}", ha = "center"
                )

    plt.savefig("imagens\gaugeDiametro.png")

    img = cv2.imread('imagens\gaugeDiametro.png')
 
    # Cropping an image
    cropped_image = img[0:250, 0:400]
 
    # Save the cropped image
    cv2.imwrite("imagens\gaugeDiametro.png", cropped_image)
    plt.close()

def LineGraph(numData, current_time, queueTempo, queueDados):
    os.remove("imagens\graphDiametro.png")

    queueDados.append(numData) 
    queueTempo.append(current_time)

    # To run GUI event loops
    figLineGraph = plt.figure(dpi=ORIGINAL_DPI)
    figLineGraph.set_size_inches(9.2, 3.2)
    ax = figLineGraph.add_subplot()
    figLineGraph.autofmt_xdate()

    ax.plot(list(queueTempo), list(queueDados))
    ax.set_ylim(min(list(queueDados)) - 2, max(list(queueDados)) + 2)
    ax.set_xlim(list(queueTempo)[0], list(queueTempo)[-1])
    ax.set_xlabel("Horas")
    ax.set_ylabel("Diâmetro [mm]")

    #linhaLineGraph.set_data(list(queueTempo), list(queueDados))
    plt.savefig("imagens\graphDiametro.png")
    plt.close()

### THREADS
def segmentar_imagem():
    global imagem_segmentada

    # Captura do vídeo frame por frame
    ### TIRAR COMENTÁRIO A SEGUIR QUANDO USANDO CAMERA
    _, frame = vid.read()
    ### PARA VIDEO
    #success, frame = cap.read()
    # Conversão de imagem de uma espaço de cores para o outro
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    # Captura do frame mais atual e transformação dela para imagem
    captured_image = Image.fromarray(opencv_image)
    results = model(captured_image, verbose=False, max_det=10)

    imagem_segmentada_plot = results[0].plot()
    imagem_segmentada = Image.fromarray(cv2.cvtColor(imagem_segmentada_plot, cv2.COLOR_BGR2RGBA))

def redefinir_res_cam():
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, w_img * 2)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, h_img * 2)

# Variáveis
# Definição do DPI original utilizado
ORIGINAL_DPI = 96.09458128078816
APP_WIDTH = 1000
APP_HEIGHT = 720
w_img, h_img = 30, 30
model = YOLO("yolov8m-seg.pt")

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
#cap = ConfigurarCamera()

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
photo_image_ifes_logo = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), 'imagens/IFES_horizontal_logo.png')), size=(215.46, 86.184))
image_ifes_logo_label = CTkLabel(frameLogos, image=photo_image_ifes_logo, text="")
image_ifes_logo_label.grid(row=0, column=0)

photo_image_arcelor_logo = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), 'imagens/ArcelorMittal_logo.png')), size=(168, 69.12))
image_arcelor_logo_label = CTkLabel(frameLogos, image=photo_image_arcelor_logo, text="")
image_arcelor_logo_label.grid(row=0, column=1)

photo_image_oficinas_logo = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), 'imagens/Oficinas4-0_logo.png')), size=(163.84, 33.6))
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
frameVideo.bind('<Configure>', Imagem_Video)

frameAlertGraph = CTkFrame(frameCentral, fg_color="#a4a8ad", border_width=2, corner_radius=15)
frameAlertGraph.grid(row=0, column=1, padx=(0, 20), pady=(10, 10), sticky='nsew')

AlertGraphImage = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), 'imagens/gaugeDiametro.png')), size=(400 * 0.7, 250 * 0.7))
AlertGraphLabel = CTkLabel(frameAlertGraph, image=AlertGraphImage, text="")
AlertGraphLabel.pack(fill=BOTH, expand=True, padx=10, pady=10)

#Criação dos frames da parte de baixo
frameDataGraph = CTkFrame(frameCentral, fg_color="#a4a8ad", border_width=2, corner_radius=15)
frameDataGraph.grid(row=1, columnspan=2, padx=(20, 20), pady=(10, 10), sticky='nsew')

DataGraphImage = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), 'imagens/graphDiametro.png')), size=(400 * 0.7, 250 * 0.7))
DataGraphLabel = CTkLabel(frameDataGraph, image=DataGraphImage, text="")
DataGraphLabel.pack(fill=BOTH, expand=True, padx=10, pady=10)


# Criar o label do texto do vídeo e colocar em cima dele
#video_text_label = CTkLabel(frameVideo, text="Imagem Segmentada", font=("Arial", 23))
#video_text_label.grid(row=0, pady=3, padx=20, sticky='W')
#video_text_label.place(relx=.5, rely=.5, anchor="w", x=10)

# Criar o label do vídeo e mostrar no app
video_widget = CTkLabel(frameVideo, text="")
video_widget.pack(fill=BOTH, expand=True, padx=10, pady=10)

#Função para abrir ativar câmera e encaixar ela no app
Open_Camera()

#Inicializacao das variaveis dos dados
queueTempo = deque([], maxlen = 15)
queueDados = deque([], maxlen = 15)
#dbCreate()

#Chamada da função para atualzar as imagems dos graficos
CriacaoGrafico(queueTempo, queueDados)

# Função para rodar o app
app.mainloop()