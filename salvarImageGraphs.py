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

   

    while True:
        try:
             # Load pickled data
            with open('./dados_pickle/dadosPickle.pkl', 'rb') as f:
                dados = pickle.load(f)
            with open('./dados_pickle/tempoPickle.pkl', 'rb') as f:
                tempo = pickle.load(f)
            # CONFIGURAR


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

     
    while True:
        try:
            
        except Exception as e:
            print(e)
            time.sleep(0.015)

if __name__ == '__main__':
    ImageProcess()
