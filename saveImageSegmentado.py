from multiprocessing import Process
from datetime import datetime
from threading import Timer
from collections import deque
from ultralytics import YOLO
from threading import Timer
import _pickle as pickle
from numpy import asarray
from PIL import Image
import numpy as np
import pyautogui
import warnings
import random
import time
import cv2 as cv
import gc

import platform
import torch
import math
import csv

import mainFullScreen

warnings.filterwarnings("ignore")

gc.enable()
global model
# Resize para salvar imagens
tamanho_imagem = (1920, 1080)
diametroCM = 0
WIDTH, HEIGHT = pyautogui.size()

Y, YX, HX, WX = 300, int(200*(HEIGHT/384)), round((HEIGHT/384), 3), round((WIDTH/640), 3)

#SAVE IMAGE DATA IN PICKLE FILE TO BE USED BY THE DASH PROGRAM.
def storeData(data, path):
    # initializing data to be stored in db 
    db = (data)
    # Its important to use binary mode 
    dbfile = open(path, 'wb') 
    # source, destination 
    pickle.dump(db, dbfile)         
    dbfile.close()
 
def calibracao(result, frame):
    global tam
    mask = result.masks.data
    mask = mask.cpu()
    mask = np.squeeze(np.array(mask))[Y]
    diametro = int(np.count_nonzero(mask)*WX)
    inicial = int(np.argmax(mask)*WX)
    tam = round(40 / (diametro), 2)
    img = cv.line(frame, (inicial, YX), ((inicial + diametro), YX), (0, 0, 255), 4)
    img = cv.putText(img, '40 cm', (560, (YX - 40)), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv.LINE_AA)
    return img

#def medicao(result, frame):
#    mask = np.squeeze(np.array(result.masks.data))
#    if mask.shape[0] > 200:
#        mask = np.squeeze(np.array(mask))
#        dimen = np.array(result.boxes.xyxy)
#        mask = mask[(int(dimen[0, 1]//HX)):(int(dimen[0, 3]//HX)), (int(dimen[0, 0]//WX)):(int(dimen[0, 2]//WX))]
#        n0 = np.count_nonzero(mask, axis=1, keepdims=True)
#        ind = (np.where(n0 == np.max(n0))[0])[-1]
#        diametroCM = int((n0[ind])*WX)
#        inicial = int(((np.argmax(mask[ind]))*WX)+dimen[0, 0])
#        tamanho2 = int(n0[Y]*WX)
#        inicial2 = int(((np.argmax(mask[Y]))*WX)+dimen[0, 0])
#        y_vid2 = int(Y*HX)
#        y_vid = int(ind*HX)
#        x_vid = int(dimen[0, 2] + 40)
#        frame = cv.line(frame, (inicial2, y_vid2), ((inicial2 + tamanho2), y_vid2), (0, 0, 255), 4)
#        frame = cv.putText(frame, (str(int(diametroCM * tam)) + ' cm'), (x_vid, (y_vid2 + 20)), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv.LINE_AA)
#        frame = cv.line(frame, (inicial, y_vid), ((inicial + tamanho), y_vid), (0, 0, 255), 4)
#        frame = cv.putText(frame, (str(int(tamanho * tam)) + ' cm'), (x_vid, (y_vid + 20)), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv.LINE_AA)
#        return frame

def medicao(result, frame):
    global diametroCM

    mask = result.masks.data
    mask = mask.cpu()
    if mask.shape[1] > 200:
        mask = np.squeeze(np.array(mask))[Y]
        diametro = int(np.count_nonzero(mask)*WX)
        inicial = int(np.argmax(mask)*WX)
        diametroCM = int(diametro * tam)
        frameNovo = cv.line(frame, (inicial, YX), ((inicial + diametro), YX), (0, 0, 255), 4)
        frameNovo = cv.putText(frame, str(diametroCM) + ' cm', (inicial, YX - 50), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv.LINE_AA)
        return frameNovo
    
def ImageProcess():

    #model = YOLO("best.pt")
    model = YOLO("yolov8n-seg.pt")
    model.conf = 0.45  # NMS confidence threshold
    model.iou = 0.65  # NMS IoU threshold
    model.agnostic = True  # NMS class-agnostic
    
    # Configure camera
    # Define a video capture object
    vid = cv.VideoCapture(0, cv.CAP_DSHOW)
  
    # Set the width and height
    vid.set(cv.CAP_PROP_FRAME_WIDTH, tamanho_imagem[0])
    vid.set(cv.CAP_PROP_FRAME_HEIGHT, tamanho_imagem[1])

    queueHoras = deque([], maxlen = 20)
    queueDados = deque([], maxlen = 20)
    queueDias = deque([], maxlen = 20)
    time_matrix = []

    jaCalibrou = False
    
    while True:
        try:
            # Captura do vídeo frame por frame
            _, frame = vid.read()

            # Conversão de imagem de uma espaço de cores para o outro
            opencv_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            
            frameNovo = cv.resize(opencv_image, (WIDTH, HEIGHT))
            
            # Captura do frame mais atual e transformação dela para imagem
            captured_image = Image.fromarray(frameNovo)

            results = model(captured_image, verbose=False, max_det = 1)
            

            if(results != None):
                for result in results:
                    frameNovo = result.plot()
                    if(result.masks != None and jaCalibrou):
                        imagem = medicao(result, frameNovo)
                    elif(result.masks != None and jaCalibrou == False):
                        imagem = calibracao(result, frameNovo)
                        jaCalibrou = True
            elif(jaCalibrou):
                print("aqui")
                mainFullScreen.app.button_event_reset_diametro_gauge()
            else:
                imagem = frameNovo

            img_array = imagem


           # Dados

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_date = now.strftime("%D")

            if len(time_matrix) > 0:

                if time_matrix[-1][1] != current_time:

                    cont = int(0)
                    media_diametro = int(0)

                    for i in range(0, len(time_matrix)):

                        media_diametro += time_matrix[i][0]
                        cont += 1
        
                    media = float(f"{media_diametro/cont:.2f}")
                    #print(f"media_diametro = {media_diametro}")
                    #print(f"cont = {cont}")
                    #print(f"media = {media}")

                    queueDados.append(media)
                    queueHoras.append(time_matrix[1][1])
                    queueDias.append(current_date)

                    time_matrix.clear()

            time_matrix.append([diametroCM, current_time])

            outputArrayTempoHora = np.array([])
            outputArrayTempoHora = np.append(outputArrayTempoHora, queueHoras)
            outputArrayTempoData = np.array([])
            outputArrayTempoData = np.append(outputArrayTempoData, queueDias)

            outputArrayDados = np.array([])
            outputArrayDados = np.append(outputArrayDados, queueDados)

            storeData(img_array, './dados_pickle/framePickle.pkl')
            storeData(outputArrayDados, './dados_pickle/dadosPickle.pkl')
            storeData(outputArrayTempoHora, './dados_pickle/horaPickle.pkl')
            storeData(outputArrayTempoData, './dados_pickle/dataPickle.pkl')

        except Exception as e:
            print(e)
            time.sleep(0.015)

if __name__ == '__main__':
    ImageProcess()
