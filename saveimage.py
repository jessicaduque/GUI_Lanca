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

gc.enable()

import os

global model
# Resize para salvar imagens
tamanho_imagem = (1920, 1080)


####### PARA IGNORAR TEMPORARIAMENTE
#SAVE IMAGE DATA IN PICKLE FILE TO BE USED BY THE DASH PROGRAM.
def storeData(data, path): 
    # initializing data to be stored in db 
    db = (data)
    # Its important to use binary mode 
    dbfile = open(path, 'wb') 
    # source, destination 
    pickle.dump(db, dbfile)         
    dbfile.close()
   
#STORE OUTPUT DATA IN CSV FILE.
def storeCSV(arc):
    dateTime = datetime.now()
    dateTime2 = dateTime.strftime("%Y-%m-%d %H:%M:%S")
    #PATH OF CSF TO BE SAVED
    if(int(dateTime.day)>9):
        if(int(dateTime.month)>9):
            path = 'data/cam0'+str(arc)+'/'+str(dateTime.year)+'-'+str(dateTime.month)+'-'+str(dateTime.day)+'.csv'
        else:
            path = 'data/cam0'+str(arc)+'/'+str(dateTime.year)+'-0'+str(dateTime.month)+'-'+str(dateTime.day)+'.csv'
    else:
        if(int(dateTime.month)>9):
            path = 'data/cam0'+str(arc)+'/'+str(dateTime.year)+'-'+str(dateTime.month)+'-0'+str(dateTime.day)+'.csv' 
        else:
            path = 'data/cam0'+str(arc)+'/'+str(dateTime.year)+'-0'+str(dateTime.month)+'-0'+str(dateTime.day)+'.csv' 
    dataFile = open('./assets/dados/dadosPickle'+str(arc)+'.pkl', 'rb')
    data = pickle.load(dataFile)
    dataFile.close()
    csvData = str(dateTime2)+' '+str(data)
    # open the file in the write mode
    f = open(path, 'a')
    # write a row to the csv file
    f.write(csvData+'\n')
    # close the file
    f.close()
     

def ImageProcess():

    model = YOLO("yolov8m-seg.pt")
    model.conf = 0.45  # NMS confidence threshold
    model.iou = 0.65  # NMS IoU threshold
    model.agnostic = True  # NMS class-agnostic
    model.max_det = 10  # maximum number of detections per image
    

    # Configure camera
    # Define a video capture object
    vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
  
    # Set the width and height
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, tamanho_imagem[0])
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, tamanho_imagem[1])

    queueTempo = deque([], maxlen = 15)
    queueDados = deque([], maxlen = 15)
     
    while True:
        try:
            # Captura do vídeo frame por frame
            _, frame = vid.read()
            # Conversão de imagem de uma espaço de cores para o outro
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Captura do frame mais atual e transformação dela para imagem
            captured_image = Image.fromarray(opencv_image)
            results = model(captured_image, verbose=False)

            imagem_segmentada_plot = results[0].plot()
            imagem_segmentada = Image.fromarray(cv2.cvtColor(imagem_segmentada_plot, cv2.COLOR_BGR2RGB))

            img_array = results[0].plot(line_width=3, labels=0, boxes=1, probs=1)
            #img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

            ### CÓDIGO DOS MENINOS PARA RECONHECER DIÂMETRO DO CASCÃO E OBTER NÚMEROS
            #try:
            #    xyxy = results[0].boxes.xyxy.cpu()
            #    print(xyxy.shape[0])
            #    outputArray = np.array([])
            #    outputArray = np.append(outputArray, distancia)
            #    if(xyxy.shape[0]>=1):
            #        cv2.imwrite('./saved-images/'+str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+'.jpg', color_image, [cv2.IMWRITE_JPEG_QUALITY, 60])
            #        print("Objeto detectado!")
            #    for i in range(xyxy.shape[0]):
            #        c1, c2 = (int(xyxy[i,0]), int(xyxy[i,1])), (int(xyxy[i,2]), int(xyxy[i,3]))
            #        diametro_pixel =(((int(xyxy[i,2])-int(xyxy[i,0]))+(int(xyxy[i,3])-int(xyxy[i,1])))/2)
            #        diametro_mm = diametro_pixel
            #        cv2.putText(img_array, str(round(diametro_mm, 1)), (int((c1[0]+c2[0])/2)-20, int((c1[1]+c2[1])/2)+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255), thickness=1, lineType=cv2.LINE_AA)
            #        outputArray = np.append(outputArray, diametro_mm)
            #    print("N de detecções: ", outputArray.size-1)
            #except Exception as e:
            #    print(e)
            #    outputArray = 0

            ### CÓDIGO TEMPORÁRIO ALEATÓRIO ENQUANTO MENINOS NÃO TEM ALGORITMO
            # Dados
            numData = random.randrange(40, 80)
            queueDados.append(numData)

            # Horário
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            queueTempo.append(current_time)

            outputArray = np.array([])
            outputArray = np.append(outputArray, [queueTempo, queueDados])

            storeData(img_array, './dados_pickle/framePickle1.pkl')
            storeData(outputArray, './dados_pickle/dadosPickle'+'.pkl')
        except Exception as e:
            print(e)
            time.sleep(0.015)

if __name__ == '__main__':
    ImageProcess()
