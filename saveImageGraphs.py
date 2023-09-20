from multiprocessing import Process
from datetime import datetime
from collections import deque
from ultralytics import YOLO
import _pickle as pickle
from numpy import asarray
from PIL import Image
import numpy as np
import warnings
import platform
import random
import torch
import time
import math
import csv
import cv2
import gc
warnings.filterwarnings("ignore")

import plotly.graph_objects as go
import plotly.express as px
import io 
import pandas as pd

gc.enable()
global model
# Resize para salvar imagens
#tamanho_imagem = (1920, 1080)
#ORIGINAL_DPI = 96.09458128078816


#SAVE IMAGE DATA IN PICKLE FILE TO BE USED BY THE DASH PROGRAM.
def storeData(data, path): 
    # initializing data to be stored in db 
    db = (data)
    # Its important to use binary mode 
    dbfile = open(path, 'wb') 
    # source, destination 
    pickle.dump(db, dbfile)         
    dbfile.close()

def LineGraph(queueTempo, queueDados):
    df = pd.DataFrame(dict(
        x = list(queueTempo),
        y = list(queueDados)
    ))
    fig = px.line(df, x="x", y="y", title='Medida Cascão')
    fig_bytes = fig.to_image(format="png")
    buf = io.BytesIO(fig_bytes)
    img = Image.open(buf)
    return np.asarray(img)


def GaugeGraph(numData):

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 270,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Speed"}
    ))

    fig_bytes = fig.to_image(format="png")
    buf = io.BytesIO(fig_bytes)
    img = Image.open(buf)
    return np.asarray(img)


    
def graphProcess(): 

    while True:
        try:
            # Load pickled data
            with open('./dados_pickle/dadosPickle.pkl', 'rb') as f:
                dados = pickle.load(f)
            with open('./dados_pickle/horaPickle.pkl', 'rb') as f:
                tempo = pickle.load(f)
            with open('./dados_pickle/dataPickle.pkl', 'rb') as f:
                data = pickle.load(f)
            ## ATUALIZAÇÃO
            ## Gerando imagem de gauge
            arr_gaugeimg = GaugeGraph(dados)
            storeData(arr_gaugeimg, './dados_pickle/gaugeGraphPickle.pkl')
            # Gerando imagem de line
            arr_lineimg = LineGraph(tempo, dados)
            storeData(arr_lineimg, './dados_pickle/lineGraphPickle.pkl')
            
            time.sleep(1)
            
        except Exception as e:
            print(e)
            time.sleep(0.1)

if __name__ == '__main__':
    graphProcess()
