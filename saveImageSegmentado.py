from datetime import datetime
from collections import deque
from ultralytics import YOLO
import _pickle as pickle
from PIL import Image
import numpy as np
import cv2 as cv
import pyautogui
import warnings
import time
import gc

warnings.filterwarnings("ignore")

gc.enable()

global model

# Resize to save the images
tamanho_imagem = (1920, 1080)
diametroCM = 0
WIDHT, HEIGHT = pyautogui.size()
Y, YX, WX = 200, int(200*(HEIGHT/384)), round(WIDHT/640, 2)

#SAVE IMAGE DATA IN PICKLE FILE TO BE USED BY THE PROGRAM.
def storeData(data, path):

    # initializing data to be stored in db 
    db = (data)

    # Its important to use binary mode 
    dbfile = open(path, 'wb') 

    # source, destination 
    pickle.dump(db, dbfile)         
    dbfile.close()
 
#####

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
 
#####

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

    # Initializing the queue variables
    queue_time = deque([], maxlen = 20)
    queue_diameter = deque([], maxlen = 20)
    queue_date = deque([], maxlen = 20)

    # Initializing matrix for all values obtained in one second
    timeData_matrix = []

    #####

    jaCalibrou = False
    
    while True:
        try:
            # Captura do vídeo frame por frame
            _, frame = vid.read()

            # Conversão de imagem de uma espaço de cores para o outro
            #opencv_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            
            frameNovo = cv.resize(frame, (WIDHT, HEIGHT))
            # Captura do frame mais atual e transformação dela para imagem
            captured_image = Image.fromarray(frameNovo)

            results = model(captured_image, verbose=False, max_det = 1)
            
            for result in results:
                if(result.masks != None and jaCalibrou):
                    imagem = medicao(result, frameNovo)
                elif(result.masks != None and jaCalibrou == False):
                    print("Reconheceu e calibrou!")
                    imagem = calibracao(result, frameNovo)
                    jaCalibrou = True
                else:
                    print("Não reconheceu nada")
                    imagem = results[0].plot()

            img_array = imagem

    #####

            # Data
            # Getting the time of each measurement of the program
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_date = now.strftime("%D")
            
            # Only executes if the matrix isnt empty
            if len(timeData_matrix) > 0:

                # If the last time on the matrix is different from current it starts the update of the queues
                if timeData_matrix[-1][0] != current_time:

                    # Initializing variables before loop
                    cont = int(0)
                    avg_diameter = int(0)

                    # Loop for the index of every value on the matrix
                    for i in range(0, len(timeData_matrix)):

                        # Sum of all the values obtained in one second of the program
                        avg_diameter += timeData_matrix[i][1]

                        # Amount of values obtained in one second of the program
                        cont += 1
                    
                    # Calculating the average of the values obtained
                    avg = float(f"{avg_diameter/cont:.2f}")

                    #print(f"avg_diameter = {avg_diameter}")
                    #print(f"cont = {cont}")
                    #print(f"avg = {avg}")

                    # Adds the updated values to the queue
                    queue_diameter.append(avg)
                    queue_time.append(timeData_matrix[1][0])
                    queue_date.append(current_date)

                    # Empties the matrix to be used on the next second
                    timeData_matrix.clear()

            # Appends the diameter and time values obtained in the matrix
            timeData_matrix.append([current_time, diametroCM])

            # Initializing numpy arrays with the queues to pickle the data
            outputArray_time = np.array([])
            outputArray_time = np.append(outputArray_time, queue_time)
            outputArray_date = np.array([])
            outputArray_date = np.append(outputArray_date, queue_date)
            outputArray_diameter = np.array([])
            outputArray_diameter = np.append(outputArray_diameter, queue_diameter)

            # Pickling the data so the code is lighter, pkl files are lighter to load
            storeData(img_array, './dados_pickle/framePickle.pkl')
            storeData(outputArray_diameter, './dados_pickle/dadosPickle.pkl')
            storeData(outputArray_time, './dados_pickle/horaPickle.pkl')
            storeData(outputArray_date, './dados_pickle/dataPickle.pkl')

        except Exception as e:
            print(e)
            time.sleep(0.015)

if __name__ == '__main__':
    ImageProcess()
