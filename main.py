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

from detect import segmentar_imagem

import ctypes
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
    width, height = 585, 220
  
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

    imagem_segmentada = Image.fromarray(cv2.cvtColor(segmentar_imagem(captured_image), cv2.COLOR_BGR2RGBA))

    # Converção da imagem capturada para photoimage
    photo_image = CTkImage(imagem_segmentada, size=(585,220))

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

    # To run GUI event loops
    fig = Figure(dpi=ORIGINAL_DPI)
    fig.set_size_inches(9.2, 3.2)
    ax = fig.add_subplot()

    fig.autofmt_xdate()
    linha, = ax.plot(list(queueTempo), list(queueDados))
    #plt.title("Diâmetro do cascão", fontsize=20)
    ax.set_xlabel("Horas")
    ax.set_ylabel("Diâmetro [mm]")

    
    return fig, ax, queueDados, queueTempo, linha

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
    ax.set_ylim(min(list(y)) - 2, max(list(y)) + 2)
    ax.set_xlim(list(x)[0], list(x)[-1])

    linha.set_data(list(x), list(y))

    # Desenhando o novo gráfico
    canvas.draw()
    
    # Chamando a função recursiva de segundo em segundo para rodar a função novamente e continuar atualizando o gráfico
    canvas.get_tk_widget().after(1000, PlotarGraficoData, y, x)

# Definição do DPI original utilizado
ORIGINAL_DPI = 96.09458128078816

ctypes.windll.shcore.SetProcessDpiAwareness(2)

app_width = 1000
app_height = 720

### Inicialização do app
app = App()

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

start_app_x = (screen_width - app_width) / 2
start_app_y = (screen_height - app_height ) / 2

print(start_app_x)
print(start_app_y)

print(app.winfo_screenwidth())
print(app.winfo_screenheight())

app.geometry(f"{app_width}x{app_height}+{int(start_app_x)}+{int(start_app_y)}")
app.minsize(1000, 720)
app.resizable(1, 1)
app.title("DashMedidor")

# Configurar a câmera para o seu uso
vid = ConfigurarCamera()

app.columnconfigure(0, weight=1)
app.rowconfigure(1, weight=1)

### Frame header da tela
frameHeader = CTkFrame(app, height=100, fg_color='#a4a8ad', corner_radius=0)
frameHeader.grid(row=0, sticky='ewn')

frameLogos = CTkFrame(frameHeader, fg_color='#a4a8ad', corner_radius=0)
frameLogos.pack(fill=X, expand=True, padx=100)

frameLogos.columnconfigure(0, weight=1)
frameLogos.columnconfigure(1, weight=1)
frameLogos.columnconfigure(2, weight=1)

# As imagens das 3 logos sendo encaixadas no header
photo_image_ifes_logo = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), 'IFES_horizontal_logo.png')), size=(283.5 * 0.8, 113.4 * 0.8))
image_ifes_logo_label = CTkLabel(frameLogos, image=photo_image_ifes_logo, text="")
image_ifes_logo_label.grid(row=0, column=0)

photo_image_arcelor_logo = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), 'ArcelorMittal_logo.png')), size=(210 * 0.8, 86.40 * 0.8))
image_arcelor_logo_label = CTkLabel(frameLogos, image=photo_image_arcelor_logo, text="")
image_arcelor_logo_label.grid(row=0, column=1)

photo_image_oficinas_logo = CTkImage(Image.open(os.path.join(os.path.dirname(__file__), 'Oficinas4-0_logo.png')), size=(204.8 * 0.8, 42 * 0.8))
image_oficinas_logo_label = CTkLabel(frameLogos, image=photo_image_oficinas_logo, text="")
image_oficinas_logo_label.grid(row=0, column=2)


### Frame principal da tela
framePrincipal = CTkFrame(app, fg_color='#4f7d71', corner_radius=0)
framePrincipal.grid(row=1, sticky='nsew')

# Frame com widgets do frame principal da tela
frameCentral = CTkFrame(framePrincipal, fg_color='red')
frameCentral.pack(fill=BOTH, expand=True, padx=20, pady=20)

frameCentral.rowconfigure(0, weight=1)
frameCentral.rowconfigure(1, weight=1)
frameCentral.columnconfigure(0, weight=2)
frameCentral.columnconfigure(1, weight=1)

# Criação dos frames da parte de cima
frameVideo = CTkFrame(frameCentral, fg_color="#a4a8ad", border_width=2, corner_radius=15)
frameVideo.grid(row=0, column=0, padx=(20, 20), pady=(0, 10), sticky='ew')
# Para frame do vídeo não adaptar tamanho aos componentes dentro
#frameVideo.grid_propagate(False)

frameAlertGraph = CTkFrame(frameCentral, fg_color="#a4a8ad", border_width=2, corner_radius=15)
frameAlertGraph.grid(row=0, column=1, padx=(0, 20), pady=(0, 10), sticky='ew')
#frameAlertGraph.grid_propagate(False)

# Criação dos frames da parte de baixo
frameDataGraph = CTkFrame(frameCentral, fg_color="#a4a8ad", border_width=2, corner_radius=15)
frameDataGraph.grid(row=1, columnspan=2, padx=(20, 20), pady=(10, 0), sticky='ew')
#frameDataGraph.grid_propagate(False)

# Criar o label do texto do vídeo e colocar em cima dele
#video_text_label = CTkLabel(frameVideo, text="Imagem Segmentada", font=("Arial", 23))
#video_text_label.grid(row=0, pady=3, padx=20, sticky='W')
#video_text_label.place(relx=.5, rely=.5, anchor="w", x=10)

# Criar o label do vídeo e mostrar no app
video_widget = CTkLabel(frameVideo, text="")
#video_widget.grid(row=1, pady=3, padx=20)
#video_widget.place(relx=.5, rely=.5, anchor="center")

#Função para abrir ativar câmera e encaixar ela no app
#Open_Camera()

# Criação do gráfico e chamada da função para atualizá-la
fig, ax, queueDados, queueTempo, linha = CriacaoGrafico()
canvas = FigureCanvasTkAgg(fig, frameDataGraph)
canvas.draw()

toolbar = NavigationToolbar2Tk(canvas, frameDataGraph, pack_toolbar=False)
toolbar.update()
canvas.get_tk_widget().place(relx=.5, rely=.5, anchor='center')

#PlotarGraficoData(queueDados, queueTempo)

# Função para rodar o app
app.mainloop()