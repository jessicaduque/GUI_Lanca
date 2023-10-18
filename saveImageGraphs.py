from multiprocessing import Process
from datetime import datetime
from collections import deque
from ultralytics import YOLO
import _pickle as pickle
from numpy import asarray
from PIL import Image
import numpy as np
import warnings
import time
import gc

import platform
import random
import torch
import math
import csv
import cv2

import plotly.graph_objects as go
import plotly.express as px
import io 
import pandas as pd

from winsound import Beep

warnings.filterwarnings("ignore")

gc.enable()

maiorDiametro = 0

notes = {'C': 1635,
         'D': 1835,
         'E': 2060,
         'S': 1945,
         'F': 2183,
         'G': 2450,
         'A': 2750,
         'B': 3087,
         ' ': 37}


melodie = 'CDEFG G AAAAG AAAAG FFFFE E DDDDC'

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
    fig = px.line(df, x="x", y="y", text="y", markers=True, template="seaborn", 
                  labels = dict(x = "Horário", y = "Diâmetro (mm)"))

    fig.update_layout(paper_bgcolor = "#a4a8ad")

    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )

    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )

    fig.update_traces(line_color='#E0165C'),

    fig_bytes = fig.to_image(format="png", width=1000, height=400)
    buf = io.BytesIO(fig_bytes)
    img = Image.open(buf)
    return np.asarray(img)

def GaugeGraph(numData):

    if numData < 60:
        colorLevel = "#4dab6d"
    elif numData >= 70:
        colorLevel = "#ee3d55"
    else:
        colorLevel = "#fabd57"

    fig = go.Figure(

        go.Indicator(
            mode = "gauge+number",
            value = numData,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Diametro"},
            gauge = {

                    'axis': {'range': [40, 80], 'tickwidth': 1},

                    'bar': {'color': f"{colorLevel}"},

                    'steps': [
                        {'range': [40, 60], 'color': 'white'},
                        {'range': [60, 70], 'color': 'white'},
                        {'range': [70, 80], 'color': 'white'}],

                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 79}

                    }
        )
    )
    fig.update_layout(
        paper_bgcolor='#a4a8ad',

        shapes=[go.layout.Shape(
        fillcolor = '#EAEAF2',
        layer='below',
        type='rect',
        xref='paper',
        yref='paper',
        x0=-0.1,
        y0=-0.1,
        x1=1.1,
        y1=1.1,
        line={'width': 1, 'color': 'black'}
        )]
    )

    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
    )

    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
    )


    fig_bytes = fig.to_image(format="png")
    buf = io.BytesIO(fig_bytes)
    img = Image.open(buf)
    return np.asarray(img)


    
def graphProcess(): 
    global maiorDiametro

    while True:
        try:
            # Load pickled data
            with open('./dados_pickle/dadosPickle.pkl', 'rb') as f:
                dados = pickle.load(f)
            with open('./dados_pickle/horaPickle.pkl', 'rb') as f:
                tempo = pickle.load(f)
            with open('./dados_pickle/dataPickle.pkl', 'rb') as f:
                data = pickle.load(f)

            ## UPDATES

            # Plotting images
            if(len(dados) > 0):
                if(dados[-1] > maiorDiametro):
                    maiorDiametro = dados[-1] 
                    arr_gaugeimg = GaugeGraph(maiorDiametro)
                    if(dados[-1] > 80):
                        for note in melodie:
                            Beep(notes[note], 100)

            arr_lineimg = LineGraph(tempo, dados)

            # Storing images in pickle files
            storeData(arr_gaugeimg, './dados_pickle/gaugeGraphPickle.pkl')
            storeData(arr_lineimg, './dados_pickle/lineGraphPickle.pkl')
            
        except Exception as e:
            print(e)
            time.sleep(0.1)

if __name__ == '__main__':
    graphProcess()
