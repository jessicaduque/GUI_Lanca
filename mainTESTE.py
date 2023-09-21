import tkinter as tk
from customtkinter import *
import signal
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
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
<<<<<<< Updated upstream
            img_data = cv2.cvtColor(img_data_gauge_graph, cv2.COLOR_BGR2RGB)
            frameGaugeGraph = Image.fromarray(img_data)
            del img_data
=======
            frameGaugeGraph = Image.fromarray(img_data_gauge_graph)
>>>>>>> Stashed changes
            self.GaugeGraphImage = CTkImage(light_image=frameGaugeGraph, size=(400 * 0.7, 250 * 0.7))
            self.GaugeGraphLabel.configure(image=self.GaugeGraphImage)
            self.GaugeGraphLabel.pack(fill=BOTH, expand=True, padx=10, pady=10)


            f = open('./dados_pickle/lineGraphPickle.pkl', 'rb')
            img_data_line_graph = pickle.load(f)
            f.close()
            del f
            img_data = cv2.cvtColor(img_data_line_graph, cv2.COLOR_BGR2RGB)
            frameLineGraph = Image.fromarray(img_data)
            del img_data
            self.LineGraphImage = CTkImage(light_image=frameLineGraph, size=(400 * 0.7, 250 * 0.7))
            self.LineGraphLabel.configure(image=self.LineGraphImage)
            self.LineGraphLabel.pack(fill=BOTH, expand=True, padx=10, pady=10)

        except Exception as e:
            print(e)
        self.after(1000, self.update_plots)
    
if __name__ == "__main__":
    ### Variables
    # Defining original DPI being used
    ORIGINAL_DPI = 96.09458128078816
    APP_WIDTH = 1000
    APP_HEIGHT = 720
    w_img, h_img = 30, 30

    app = App()
    processSalvarImageGraphs = subprocess.Popen(['python', 'saveImageGraphs.py'], stdout=None, stderr=None)
    processSalvarImageSegmentado = subprocess.Popen(['python', 'saveImageSegmentado.py'], stdout=None, stderr=None)
    processDataBase = subprocess.Popen(['python', 'database.py'], stdout=None, stderr=None)

    
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

    def on_closing():# Parando o subprocess de imagens ao fechar o app
        os.kill(processSalvarImageGraphs.pid, signal.SIGTERM)
        os.kill(processSalvarImageSegmentado.pid, signal.SIGTERM)
        os.kill(processDataBase.pid, signal.SIGTERM)

        # Deletando os arquivos pickle ao fechar o app
        os.remove(os.path.join(os.path.dirname(__file__), 'dados_pickle/dadosPickle.pkl'))
        os.remove(os.path.join(os.path.dirname(__file__), 'dados_pickle/dataPickle.pkl'))
        os.remove(os.path.join(os.path.dirname(__file__), 'dados_pickle/horaPickle.pkl'))
        os.remove(os.path.join(os.path.dirname(__file__), 'dados_pickle/framePickle.pkl'))
        os.remove(os.path.join(os.path.dirname(__file__), 'dados_pickle/gaugeGraphPickle.pkl'))
        os.remove(os.path.join(os.path.dirname(__file__), 'dados_pickle/lineGraphPickle.pkl'))

        # Deletando a janela do app
        app.destroy()

    # Protocolo para executar funcao on_closing ao clickar no X do app
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()

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
