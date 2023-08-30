import tkinter as tk
from customtkinter import *

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from database import dbAdd, dbShow
from PIL import Image, ImageTk
from collections import deque
from ultralytics import YOLO
import _pickle as pickle
import subprocess
import random
import ctypes
import cv2
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
        #photo_image_empresa_logo = CTkImage(light_image=Image.open('./imagens/ArcelorMittal_logo.png'),
        #                                   size=(168, 69.12)
        #                                   )

        photo_image_empresa_logo = CTkImage(light_image=Image.open('./imagens/LumarMetals_Logo.jpg'),
                                           size=(265, 56)
                                           )

        photo_image_oficinas_logo = CTkImage(light_image=Image.open('./imagens/Oficinas4-0_logo.png'),
                                            size=(163.84, 33.6)
                                             )

        # Configuring images
        self.image_ifes_logo_label = CTkLabel(self.frameHeader, image=photo_image_ifes_logo, text="")
        self.image_ifes_logo_label.grid(row=0, column=0, padx=(20, 0))
        
        self.image_empresa_logo_label = CTkLabel(self.frameHeader, image=photo_image_empresa_logo, text="")
        self.image_empresa_logo_label.grid(row=0, column=1)
        
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
        self.video_widget.pack(padx=10, pady=10, fill=BOTH, expand=True)

        self.frameGaugeGraph = CTkFrame(self.framePrincipal, fg_color="#a4a8ad", corner_radius=15)
        self.frameGaugeGraph.grid(row=0, column=1, padx=(0, 30), pady=(10, 10), sticky='nsew')

        GaugeGraphImage = CTkImage(Image.open('./imagens/gaugeDiametro.png'),
                                  size=(400 * 0.7, 250 * 0.7)
                                   )
        self.GaugeGraphLabel = CTkLabel(self.frameGaugeGraph, image=GaugeGraphImage, text="")
        self.GaugeGraphLabel.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Configure bottom widgets
        self.frameLineGraph = CTkFrame(self.framePrincipal, fg_color="#a4a8ad", corner_radius=15)
        self.frameLineGraph.grid(row=1, columnspan=2, padx=30, pady=(0, 10), sticky='nsew')

        LineGraphImage = CTkImage(Image.open('./imagens/graphDiametro.png'),
                                 size=(400 * 0.7, 250 * 0.7)
                                 )
        self.LineGraphLabel = CTkLabel(self.frameLineGraph, image=LineGraphImage, text="")
        self.LineGraphLabel.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Rodar métodos continuamente de atualização de imagem, segmentação e dos plots de gráficos
        self.update_image()
        self.update_plots()

    # FEITO, MAS IMAGEM NÃO REDIMENSIONA
    def update_image(self):
        try:
            # Load pickled PIL image
            f = open('./dados_pickle/framePickle.pkl', 'rb')
            img_data = pickle.load(f)
            f.close()
            del f
            # Convert RGB image to BGR image
            img_data = cv2.cvtColor(img_data, cv2.COLOR_BGR2RGB)
            # Convert numpy array to PIL image
            frame = Image.fromarray(img_data)
            #img_data = None
            del img_data
            self.imagem_video = CTkImage(light_image=frame, size=(480, 270))
            self.video_widget.configure(image=self.imagem_video)
            self.video_widget.pack(padx=10, pady=10, fill=BOTH, expand=True)

        except Exception as e:
            print(e)
        self.after(30, self.update_image)

    def update_plots(self):
        try:
            f = open('./dados_pickle/gaugeGraphPickle.pkl', 'rb')
            img_data_gauge_graph = pickle.load(f)
            f.close()
            del f
            img_data = cv2.cvtColor(img_data_gauge_graph, cv2.COLOR_BGR2RGB)
            frameGaugeGraph = Image.fromarray(img_data)
            del img_data

            f = open('./dados_pickle/lineGraphPickle.pkl', 'rb')
            img_data_line_graph = pickle.load(f)
            f.close()
            del f
            img_data = cv2.cvtColor(img_data_line_graph, cv2.COLOR_BGR2RGB)
            frameLineGraph = Image.fromarray(img_data)
            del img_data
        except Exception as e:
            print(e)
        self.after(1000, self.update_plots)
    
if __name__ == "__main__":
    print("aasdad")
    app = App()
    ### Variables
    # Defining original DPI being used
    ORIGINAL_DPI = 96.09458128078816
    APP_WIDTH = 1000
    APP_HEIGHT = 720
    w_img, h_img = 30, 30

    print("1")
    processSalvarImageGraphs = subprocess.Popen(['python', 'saveImageGraphs.py'], stdout=None, stderr=None)
    print("2")
    processSalvarImageSegmentado = subprocess.Popen(['python', 'saveImageSegmentado.py'], stdout=None, stderr=None)
    print("3")
    processDataBase = subprocess.Popen(['python', 'database.py'], stdout=None, stderr=None)
    print("4")

    
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

    def on_closing():# Parando o subprocess de imagens ao fechar o app
        processSalvarImagem.kill()

        # Deletando os arquivos pickle ao fechar o app
        os.remove(os.path.join(os.path.dirname(__file__), 'dados_pickle/dadosPickle.pkl'))
        os.remove(os.path.join(os.path.dirname(__file__), 'dados_pickle/dataPickle.pkl'))
        os.remove(os.path.join(os.path.dirname(__file__), 'dados_pickle/horaPickle.pkl'))
        os.remove(os.path.join(os.path.dirname(__file__), 'dados_pickle/framePickle.pkl'))

        # Deletando a janela do app
        app.destroy()

    # Protocolo para executar funcao on_closing ao clickar no X do app
    app.protocol("WM_DELETE_WINDOW", on_closing)
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

    # Generating test values for the diameter and current time
    numData = random.randrange(40, 80)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    # Manipulating the database
    dbAdd(numData, current_time)
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
