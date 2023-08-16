import tkinter as tk
from customtkinter import *

import cv2
from PIL import Image, ImageTk

import random
import subprocess
import _pickle as pickle
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


class App(CTk):
    def __init__(self):
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - APP_WIDTH ) / 2
        y = (screen_height - APP_HEIGHT ) / 2

        ##### Configure window
        self.title("DashMedidor")
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{int(x)}+{int(y)}")
        self.minsize(1000, 720)
        self.resizable(1, 1)

        ##### Interface creation

        ### Configure grid layout 
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        ### Configure header
        self.frameHeader = CTkFrame(self, height=100, fg_color='#a4a8ad', corner_radius=0)
        self.frameHeader.grid(row=0, column=0, sticky='nsew')

        self.frameHeader.columnconfigure(0, weight=1)
        self.frameHeader.columnconfigure(1, weight=1)
        self.frameHeader.columnconfigure(2, weight=1)

        ### Configure logo images into header
        # Defining image variables and sizes
        photo_image_ifes_logo = CTkImage(light_image=Image.open('./imagens/IFES_horizontal_logo.png'),
                                        size=(215.46, 86.184)
                                        )
        photo_image_arcelor_logo = CTkImage(light_image=Image.open('./imagens/ArcelorMittal_logo.png'),
                                           size=(168, 69.12)
                                           )
        photo_image_oficinas_logo = CTkImage(light_image=Image.open('./imagens/Oficinas4-0_logo.png'),
                                            size=(163.84, 33.6)
                                             )

        # Configuring images
        self.image_ifes_logo_label = CTkLabel(self.frameHeader, image=photo_image_ifes_logo, text="")
        self.image_ifes_logo_label.grid(row=0, column=0, padx=(20, 0))
        
        self.image_arcelor_logo_label = CTkLabel(self.frameHeader, image=photo_image_arcelor_logo, text="")
        self.image_arcelor_logo_label.grid(row=0, column=1)
        
        self.image_oficinas_logo_label = CTkLabel(self.frameHeader, image=photo_image_oficinas_logo, text="")
        self.image_oficinas_logo_label.grid(row=0, column=2, padx=(0, 20))

        ### Configure main frame
        self.framePrincipal = CTkFrame(self, fg_color='#4f7d71', corner_radius=0)
        self.framePrincipal.grid(row=1, column=0, sticky='nsew')

        self.framePrincipal.rowconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(1, weight=1)
        self.framePrincipal.columnconfigure(0, weight=1)
        self.framePrincipal.columnconfigure(1, weight=0)

        # Configure top widgets
        self.frameVideo = CTkFrame(self.framePrincipal, fg_color="#a4a8ad", corner_radius=15)
        self.frameVideo.grid(row=0, column=0, padx=(30, 10), pady=(10, 10), sticky='nsew')
        
        imagem_video = CTkImage(light_image=Image.open('./imagens/Oficinas4-0_logo.png'))
        self.video_widget = CTkLabel(self.frameVideo, image=imagem_video, text="")
        self.video_widget.pack(padx=10, pady=10)

        self.frameAlertGraph = CTkFrame(self.framePrincipal, fg_color="#a4a8ad", corner_radius=15)
        self.frameAlertGraph.grid(row=0, column=1, padx=(0, 30), pady=(10, 10), sticky='nsew')

        AlertGraphImage = CTkImage(Image.open('./imagens/gaugeDiametro.png'),
                                  size=(400 * 0.7, 250 * 0.7)
                                   )
        self.AlertGraphLabel = CTkLabel(self.frameAlertGraph, image=AlertGraphImage, text="")
        self.AlertGraphLabel.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Configure bottom widgets
        self.frameDataGraph = CTkFrame(self.framePrincipal, fg_color="#a4a8ad", corner_radius=15)
        self.frameDataGraph.grid(row=1, columnspan=2, padx=30, pady=(0, 10), sticky='nsew')

        DataGraphImage = CTkImage(Image.open('./imagens/graphDiametro.png'),
                                 size=(400 * 0.7, 250 * 0.7)
                                 )
        self.DataGraphLabel = CTkLabel(self.frameDataGraph, image=DataGraphImage, text="")
        self.DataGraphLabel.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Rodar métodos continuamente de atualização de imagem, segmentação e dos plots de gráficos
        self.update_image()
        #self.update_plots()

    # PARA MEXER AINDA
    def update_image(self):
        try:
            # Load pickled PIL image
            f = open('./dados_pickle/framePickle1.pkl', 'rb')
            img_data = pickle.load(f)
            f.close()
            del f
            # Convert RGB image to BGR image
            img_data = cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR)
            # Convert numpy array to PIL image
            frame = Image.fromarray(img_data)
            #img_data = None
            del img_data
            self.imagem_video = CTkImage(light_image=frame, size=(960, 540))
            self.video_widget.configure(image=self.imagem_video)
            self.video_widget.pack(padx=10, pady=10)

        except Exception as e:
            print(e)
        self.after(30, self.update_image)

    def update_plots(self):
        try:
            # Load pickled data
            with open('./dados_pickle/dados/dadosPickle1.pkl', 'rb') as f:
                dados = pickle.load(f)
            distancia = dados[0]
            dados = dados[1:]
            tam_med = np.mean(dados)
            self.deque_med.append(tam_med)
            self.deque_time.append(datetime.now().strftime("%H:%M:%S"))
            # Clear the plot
            self.ax1.clear()
            self.ax2.clear()
            # Plot the data
            self.ax1.plot(self.deque_time, self.deque_med)
            self.ax1.set_ylim(0, 1000)
            self.ax1.tick_params(axis='x', rotation=45, labelsize=6)
            # Calcula a média e o desvio padrão dos dados
            mu, std = norm.fit(dados)
            x = np.linspace(4, 24, 100)
            p = norm.pdf(x, mu, std)
            # Define os parâmetros do histograma
            bins = 10
            range = (0, 1000)
            density = False
            color = 'blue'
            alpha = 1
            self.ax2.hist(dados, bins=bins, range=range, density=density, color=color, alpha=alpha)
            #self.ax2.hist(dados, bins=bins, range=range, density=True, color='red', alpha=0.5)
            #self.ax2.plot(x, p*dados.size, 'k', linewidth=2)
            self.ax2.plot(x, p, 'k', linewidth=2)
            self.ax2.set_ylim(0, 15)
            # Update the plot
            self.canvas1.draw()
            self.canvas2.draw()
            # Update label text
            self.tamMed.configure(text='Tamanho médio: '+ str(round(tam_med,1))+'mm')
            self.dist.configure(text='Distância: '+ str(round(distancia, 2))+'m')
        except Exception as e:
            print(e)
        # Schedule the next update
        self.after(200, self.update_plots)


if __name__ == "__main__":
    ### Variables
    # Defining original DPI being used
    ORIGINAL_DPI = 96.09458128078816
    APP_WIDTH = 1000
    APP_HEIGHT = 720
    w_img, h_img = 30, 30

    
    app = App()
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    #process2 = subprocess.Popen(['python', 'dashBt.py'], stdout=None, stderr=None)
    processSalvarImagem = subprocess.Popen(['python', 'saveimage.py'], stdout=None, stderr=None)
    #process3 = subprocess.Popen(['python', 'db.py'], stdout=None, stderr=None)
    app.mainloop()

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

    img = cv2.imread('imagens\graphDiametro.png')
 
    # Cropping an image
    cropped_image = img[17:307, 0:815]
    cropped_image = cropped_image[0:290, 60:815]
 
    # Save the cropped image
    cv2.imwrite("imagens\graphDiametro.png", cropped_image)
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



############### Configurar a câmera para o seu uso
#vid = ConfigurarCamera()
###cap = ConfigurarCamera()

############### Função para abrir ativar câmera e encaixar ela no app
#Open_Camera()

############### Inicializacao das variaveis dos dados
#queueTempo = deque([], maxlen = 15)
#queueDados = deque([], maxlen = 15)
#dbCreate()

################ Chamada da função para atualzar as imagems dos graficos
#CriacaoGrafico(queueTempo, queueDados)
