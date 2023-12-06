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

import main
warnings.filterwarnings("ignore")

gc.enable()
global model

# Resize to save the images
img_size = (1920, 1080)
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
 
def calibracao(result):
    global tam
    mask = result.cpu().masks.data
    mask = np.squeeze(np.array(mask))[Y]
    diametro = int(np.count_nonzero(mask)*WX)
    print(diametro)
    inicial = int(np.argmax(mask)*WX)
    tam = round(40 / (diametro), 2)

def medicao(result, frame):
    global diametroCM
    mask = result.cpu().masks.data
    mask = np.squeeze(np.array(mask))
    boxes = result.boxes.xyxy.cpu()
    dimen = np.array(boxes)
    mask = mask[int(dimen[0, 1]//HX):int(dimen[0, 3]//HX), int(dimen[0, 0]//WX):int(dimen[0, 2]//WX)]
    n0 = np.count_nonzero(mask, axis=1, keepdims=True)
    ind = (np.unravel_index(np.argmax(n0, axis=0), n0.shape))[0]
    if(len(ind) == 1):
        ind = ind[0]
        tamanho = int((n0[ind])*WX)
        #print("tamanho", tamanho)
        inicial = int(((np.argmax(mask[ind]))*WX)+dimen[0, 0])
        #print("inicial", inicial)
        y_vid = int(ind*HX)
        #print("y_vid", y_vid)
        diametroCM = int(tamanho * tam)
        #print("diam", diametroCM)


        #tamanho2 = int(n0[Y]*WX)
        #inicial2 = int(((np.argmax(mask[Y]))*WX)+dimen[0, 0])
        #y_vid2 = int(Y*HX)
        
        x_vid = int(dimen[0, 2] + 40)
        #frame = cv.line(frame, (inicial2, y_vid2), ((inicial2 + tamanho2), y_vid2), (0, 0, 255), 4)
        #frame = cv.putText(frame, (str(int(tamanho2 * tam)) + ' cm'), (x_vid, (y_vid2 + 20)), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv.LINE_AA)
        frame = cv.line(frame, (inicial, y_vid), ((inicial + tamanho), y_vid), (0, 0, 255), 4)
        frame = cv.putText(frame, (str(diametroCM) + ' cm'), (x_vid, (y_vid + 20)), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv.LINE_AA)
    
    return frame

#def medicao(result, frame):
#    global diametroCM

#    mask = result.masks.data
#    mask = mask.cpu()

#    if mask.shape[1] > 200:
#        mask = np.squeeze(np.array(mask))
#        boxes = result.boxes.xyxy.cpu()
#        dimen = np.array(boxes)
#        mask = mask[(int(dimen[0, 1]//HX)):(int(dimen[0, 3]//HX)), (int(dimen[0, 0]//WX)):(int(dimen[0, 2]//WX))]
#        n0 = np.count_nonzero(mask, axis=1, keepdims=True)
#        ind = (np.where(n0 == np.max(n0))[0])[-1]
#        tamanho = int((n0[ind])*WX)
#        inicial = int(((np.argmax(mask[ind]))*WX)+dimen[0, 0])
#        diametroCM = int(tamanho * tam)
#        #tamanho2 = int(n0[Y]*WX)
#        #inicial2 = int(((np.argmax(mask[Y]))*WX)+dimen[0, 0])
#        #y_vid2 = int(Y*HX)
#        y_vid = int(ind*HX)
#        x_vid = int(dimen[0, 2] + 40)
#        #frame = cv.line(frmae, (inicial2, y_vid2), ((inicial2 + tamanho2), y_vid2), (0, 0, 255), 4)
#        #frame = cv.putText(frame, (str(int(tamanho2 * tam)) + ' cm'), (x_vid, (y_vid2 + 20)), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv.LINE_AA)
#        frame = cv.line(frame, (inicial, y_vid), ((inicial + tamanho), y_vid), (0, 0, 255), 4)
#        frame = cv.putText(frame, (str(diametroCM) + ' cm'), (x_vid, (y_vid + 20)), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv.LINE_AA)
#        return frame

#def medicao(result, frame):
#    global diametroCM

#    mask = result.masks.data
#    mask = mask.cpu()

#    print(mask)
#    print(type(mask))
#    if mask.shape[1] > 200:
#        mask = np.squeeze(np.array(mask))[Y]
#        diametro = int(np.count_nonzero(mask)*WX)
#        inicial = int(np.argmax(mask)*WX)
#        diametroCM = int(diametro * tam)
#        frameNovo = cv.line(frame, (inicial, YX), ((inicial + diametro), YX), (0, 0, 255), 4)
#        frameNovo = cv.putText(frame, str(diametroCM) + ' cm', (inicial, YX - 50), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv.LINE_AA)
#        return frameNovo
    
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
    vid.set(cv.CAP_PROP_FRAME_WIDTH, img_size[0])
    vid.set(cv.CAP_PROP_FRAME_HEIGHT, img_size[1])

    # Initializing the queue variables
    queue_time = deque([], maxlen = 20)
    queue_diameter = deque([], maxlen = 20)
    queue_date = deque([], maxlen = 20)

    # Initializing matrix for all values obtained in one second
    timeData_matrix = []

    jaCalibrou = False
    
    while True:
        try:
            # Captura do vídeo frame por frame
            _, frame = vid.read()

            # Conversão de imagem de uma espaço de cores para o outro
            opencv_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            
            frameNovo = cv.resize(frame, (WIDTH, HEIGHT))
            
            # Captura do frame mais atual e transformação dela para imagem
            captured_image = Image.fromarray(opencv_image)

            results = model(captured_image, verbose=False, max_det = 1)
            
            img_array = frameNovo 

            if(results[0].cpu().masks != None):
                frameNovo = results[0].plot()
                if(results[0].masks != None and jaCalibrou):
                    img_array = np.asarray(medicao(results[0], frameNovo))
                elif(results[0].masks != None and jaCalibrou == False):
                    calibracao(results[0])
                    jaCalibrou = True
            elif(jaCalibrou):
                print("aqui")
                img_array = np.array([0, 1, 2, 3])


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
            storeData(img_array, './pickle_data/frame_pickle.pkl')
            storeData(outputArray_diameter, './pickle_data/diameter_pickle.pkl')
            storeData(outputArray_time, './pickle_data/time_pickle.pkl')
            storeData(outputArray_date, './pickle_data/date_pickle.pkl')

        except Exception as e:
            print(e)
            time.sleep(0.015)

if __name__ == '__main__':
    ImageProcess()
