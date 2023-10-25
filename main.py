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

    # Generating test values for the diameter and current time
    numData = random.randrange(40, 80)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%D")

    # Manipulating the database
    dbAdd(numData, current_date, current_time)
    #dbShow()

    # Calling the Line graph function to add onto the queues and generate the line graph image
    LineGraph(numData, current_time, queueTempo, queueDados)

    # Updating the line graph label every loop
    LineGraphImage = CTkImage(Image.open('./imagens/graphDiametro.png'), size=(1300 * 0.7, 450 * 0.7))
    LineGraphLabel.configure(image=LineGraphImage)

    # Calling the gauge graph function to generate the gauge graph image
    GaugeGraph(numData)

    # Updating the gauge graph label every loop
    GaugeGraphImage = CTkImage(Image.open('./imagens/gaugeDiametro.png'), size=(400 * 0.7, 250 * 0.7))
    GaugeGraphLabel.configure(image=GaugeGraphImage)

    # Chamando a função recursiva de segundo em segundo para rodar a função novamente e continuar atualizando o gráfico
    GaugeGraphLabel.after(1000, CriacaoGrafico, queueTempo, queueDados)

def GaugeGraph(numData):

    # Colors for each of the zones in the graph
    color = ["#ee3d55", "#ee3d55", "#fabd57" , "#fabd57", "#4dab6d", "#4dab6d", "#4dab6d", "#4dab6d", "#4dab6d"]

    # Values displayed around the gauge graph from highest to lowest
    values = [80, 75, 70, 65, 60, 55, 50, 45, 40]

    # ALtering the color of the arrow pointer text depending on the diameter displayed
    if numData < 60:
        colorLevel = "#4dab6d"
    elif numData >= 70:
        colorLevel = "#ee3d55"
    else:
        colorLevel = "#fabd57"

    # Calculating the angle of the arrow pointer to accurately display the value on the graph
    xvalue = 3.465 - ((numData - 35) * 0.077)

    # Setting plot size
    fig = plt.figure(figsize=(4, 4))

    # layout of the plot
    axGauge = fig.add_subplot(projection="polar")
    axGauge.bar(x = [0, 0.385, 0.77, 1.155, 1.54, 1.925, 2.31, 2.695], width=0.42, height=0.5, bottom=2, 
          color=color, align="edge")

    # Positioning the values in the graph
    for loc, val in zip([0, 0.385, 0.77, 1.155, 1.54, 1.925, 2.31, 2.695, 3.08, 3,465], values):

        # Aligning values depending on their angle
        if val <= 55:
            align = "right"
        elif val == 60:
            align = "center"
        else:
            align = "left"

        plt.annotate(val, xy=(loc, 2.525), fontsize=15,  ha=f"{align}")

    # Hiding the polar projection in the background
    axGauge.set_axis_off()

    # Creating the arrow pointer
    axGauge.annotate(f"{numData}", xytext=(0,0), xy=(xvalue,2.0),
                 arrowprops=dict(arrowstyle="wedge, tail_width= 0.5", color="black", shrinkA=0), 
                 bbox = dict(boxstyle="circle", facecolor="black", linewidth=2,),
                 fontsize=25, color =f"{colorLevel}", ha = "center"
                )

    # Saving the plot as an image
    plt.savefig("imagens\gaugeDiametro.png")
    # Getting the saved image into a variable to crop
    img = cv2.imread('imagens\gaugeDiametro.png')
    # Cropping the image
    cropped_image = img[0:250, 0:400]
    # Saving the cropped image
    cv2.imwrite("imagens\gaugeDiametro.png", cropped_image)

    # Closing the plot to avoid conflict
    plt.close()

def LineGraph(numData, current_time, queueTempo, queueDados):

    # Adding the new data to the queues every loop
    queueDados.append(numData) 
    queueTempo.append(current_time)

    # To run GUI event loops
    figLineGraph = plt.figure(dpi=ORIGINAL_DPI)
    figLineGraph.set_size_inches(9.2, 3.2)
    ax = figLineGraph.add_subplot()
    figLineGraph.autofmt_xdate()

    # Making the plot with the data and setting the vertical(diameter) limit on the graph
    ax.plot(list(queueTempo), list(queueDados))
    ax.set_ylim(min(list(queueDados)) - 2, max(list(queueDados)) + 2)
    ax.set_xlabel("Horas")
    ax.set_ylabel("Diâmetro [mm]")

    # Setting general fontsyle for pyplot
    plt.rcParams['font.family'] = 'Eras Medium ITC'

    # Saving the plot as an image
    plt.savefig("imagens\graphDiametro.png")
    # Getting the saved image into a variable to crop
    img = cv2.imread('imagens\graphDiametro.png')
    # Cropping the image
    cropped_image = img[17:307, 0:815]
    cropped_image = cropped_image[0:290, 60:815]
    # Saving the cropped image
    cv2.imwrite("imagens\graphDiametro.png", cropped_image)

    # closing the plot to avoid conflict
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
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Captura do frame mais atual e transformação dela para imagem
    captured_image = Image.fromarray(opencv_image)
    results = model(captured_image, verbose=False, max_det=10)

    print(results)

    imagem_segmentada_plot = results[0].plot()
    imagem_segmentada = Image.fromarray(cv2.cvtColor(imagem_segmentada_plot, cv2.COLOR_BGR2RGB))

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
frameHeader.grid(row=0, column=0, sticky='nsew')

frameHeader.columnconfigure(0, weight=1)
frameHeader.columnconfigure(1, weight=1)
frameHeader.columnconfigure(2, weight=1)

# As imagens das 3 logos sendo encaixadas no header
photo_image_ifes_logo = CTkImage(Image.open('./imagens/IFES_horizontal_logo.png'), size=(215.46, 86.184))
image_ifes_logo_label = CTkLabel(frameHeader, image=photo_image_ifes_logo, text="")
image_ifes_logo_label.grid(row=0, column=0, padx=(20, 0))

#photo_image_empresa_logo = CTkImage(Image.open('./imagens/ArcelorMittal_logo.png'), size=(168, 69.12))
photo_image_empresa_logo = CTkImage(Image.open('./imagens/LumarMetals_Logo.jpg'), size=(265, 56))
image_empresa_logo_label = CTkLabel(frameHeader, image=photo_image_empresa_logo, text="")
image_empresa_logo_label.grid(row=0, column=1)

photo_image_oficinas_logo = CTkImage(Image.open('./imagens/Oficinas4-0_logo.png'), size=(163.84, 33.6))
image_oficinas_logo_label = CTkLabel(frameHeader, image=photo_image_oficinas_logo, text="")
image_oficinas_logo_label.grid(row=0, column=2, padx=(0, 20))


### FRAME PRINCIPAL DA TELA
framePrincipal = CTkFrame(app, fg_color='#4f7d71', corner_radius=0, border_width=0)
framePrincipal.grid(row=1, column=0, sticky='nsew')

framePrincipal.rowconfigure(0, weight=1)
framePrincipal.rowconfigure(1, weight=1)
framePrincipal.columnconfigure(0, weight=2)
framePrincipal.columnconfigure(1, weight=1)

# Criação dos frames da parte de cima
frameVideo = CTkFrame(framePrincipal, fg_color="#a4a8ad", border_width=0, corner_radius=15)
frameVideo.grid(row=0, column=0, padx=(30, 20), pady=(10, 10), sticky='nsew')
frameVideo.pack_propagate(False)
frameVideo.bind('<Configure>', Imagem_Video)

frameGaugeGraph = CTkFrame(framePrincipal, fg_color="#a4a8ad", border_width=0, corner_radius=15)
frameGaugeGraph.grid(row=0, column=1, padx=(0, 30), pady=(10, 10), sticky='nsew')

GaugeGraphImage = CTkImage(Image.open('./imagens/gaugeDiametro.png'),
                          size=(400 * 0.7, 250 * 0.7)
                           )
GaugeGraphLabel = CTkLabel(frameGaugeGraph, image=GaugeGraphImage, text="")
GaugeGraphLabel.pack(fill=BOTH, expand=True, padx=10, pady=10)

#Criação dos frames da parte de baixo
frameLineGraph = CTkFrame(framePrincipal, fg_color="#a4a8ad", border_width=0, corner_radius=15)
frameLineGraph.grid(row=1, columnspan=2, padx=30, pady=(0, 10), sticky='nsew')

LineGraphImage = CTkImage(Image.open('./imagens/graphDiametro.png'),
                         size=(400 * 0.7, 250 * 0.7)
                         )
LineGraphLabel = CTkLabel(frameLineGraph, image=LineGraphImage, text="")
LineGraphLabel.pack(fill=BOTH, expand=True, padx=10, pady=10)


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