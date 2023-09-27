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
global model
# Resize para salvar imagens
tamanho_imagem = (1920, 1080)


#SAVE IMAGE DATA IN PICKLE FILE TO BE USED BY THE DASH PROGRAM.
def storeData(data, path): 
    # initializing data to be stored in db 
    db = (data)
    # Its important to use binary mode 
    dbfile = open(path, 'wb') 
    # source, destination 
    pickle.dump(db, dbfile)         
    dbfile.close()
 
def ImageProcess():

    #model = YOLO("best.pt")
    model = YOLO("yolov8n-seg.pt")
    model.conf = 0.45  # NMS confidence threshold
    model.iou = 0.65  # NMS IoU threshold
    model.agnostic = True  # NMS class-agnostic
    
    # Configure camera
    # Define a video capture object
    vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
  
    # Set the width and height
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, tamanho_imagem[0])
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, tamanho_imagem[1])

    queueHoras = deque([], maxlen = 15)
    queueDias = deque([], maxlen = 15)
    queueDados = deque([], maxlen = 15)
     
    y, height, width = 200, 320, 640

    jaCalibrou = False

    while True:
        try:
            # Captura do vídeo frame por frame
            _, frame = vid.read()
            # Conversão de imagem de uma espaço de cores para o outro
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Captura do frame mais atual e transformação dela para imagem
            captured_image = Image.fromarray(opencv_image)
            results = model(captured_image, verbose=False, max_det = 1)
            
            for result in results:
                if(result.masks != None and jaCalibrou):
                    mask = result.masks.data
                    mask = mask.cpu()
                    mask = np.squeeze(np.array(mask))
                    npmask = np.count_nonzero(mask, axis=1)
                    if mask.shape[0] > 200:
                        tamanho = npmask[y]
                        inicial = np.argmax(mask[y])
                        height1, width1 = mask.shape
                        imagem = results[0].plot(line_width=3, labels=0, boxes=1, probs=1)
                        imagem = cv2.line(imagem, (inicial, y), ((inicial + tamanho), y), (0, 0, 255), 2)
                        diametro = int(tamanho * tam)
                        imagem = cv2.putText(imagem, (str(diametro) + ' cm'), (280, (y - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
                        imagem = cv2.resize(imagem, (1920, 1080))
                elif(result.masks != None and jaCalibrou == False):
                    print("calibracao!")
                    mask2 = results[0].masks.data
                    mask2 = mask2.cpu()
                    mask2 = np.squeeze(np.array(mask2))
                    npmask = np.count_nonzero(mask2, axis=1)
                    tamanho = npmask[y]
                    inicial = np.argmax(mask2[y])
                    height1, width1 = mask2.shape
                    calibracao = cv2.resize(opencv_image, (width1, height1))
                    calibracao = cv2.line(calibracao, (inicial, y), ((inicial + tamanho), y), (0, 0, 255), 2)
                    calibracao = cv2.putText(calibracao, '40 cm', (280, (y - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
                    tam = (int) (4 / (tamanho))
                    jaCalibrou = True
                else:
                    imagem = results[0].plot()

            img_array = imagem
            #imagem_segmentada_plot = results[0].plot()
            #imagem_segmentada = Image.fromarray(cv2.cvtColor(imagem_segmentada_plot, cv2.COLOR_BGR2RGB))

            #img_array = results[0].plot(line_width=3, labels=0, boxes=1, probs=1)
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
            current_date = now.strftime("%D")
            queueHoras.append(current_time)
            queueDias.append(current_date)

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
