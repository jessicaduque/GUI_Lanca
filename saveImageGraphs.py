import plotly.graph_objects as go
import plotly.express as px
from winsound import Beep
import _pickle as pickle
from PIL import Image
import pandas as pd
import numpy as np
import warnings
import time
import gc
import io 

warnings.filterwarnings("ignore")

gc.enable()

maior_diametro = 0

# Defining global font
font = "Raleway"

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

#SAVE IMAGE DATA IN PICKLE FILE TO BE USED BY THE PROGRAM.
def storeData(data, path): 
    # initializing data to be stored in db 
    db = (data)

    # Its important to use binary mode 
    dbfile = open(path, 'wb') 

    # source, destination 
    pickle.dump(db, dbfile)         
    dbfile.close()

# Line graph to show all values inside the queues
def lineGraph(queue_time, queue_diameter):

    # Dataframe dictionary with the xy values of the graph
    df = pd.DataFrame(dict(
        x_axis = list(queue_time),
        y_axis = list(queue_diameter)
    ))

    # PLotting the figure of the graph
    fig = px.line(df, x="x_axis", y="y_axis", text="y_axis", markers=True, template="seaborn", 
                  labels = dict(x = "", y = "Diâmetro (mm)"))

    # Updating layout background to be the same as the frame and font style
    fig.update_layout(
        paper_bgcolor = "#a4a8ad", 
        font_family = f"{font}"
    )

    # Updating axes to make a border around the graph
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

    # Updating traces line color to contrast with UI
    fig.update_traces(line_color='#E0165C'),

    # Turning plot into image, then turning the image into a numpy array to pickle
    fig_bytes = fig.to_image(format="png", width=1000, height=400)
    buf = io.BytesIO(fig_bytes)
    img = Image.open(buf)
    return np.asarray(img)

# Gauge graph to show the highest diameter recorded
def gaugeGraph(num_data):

    # Changing the color of the graph's bar based on the diameter
    if num_data < 60:
        color_level = "#4dab6d"

    elif num_data >= 70:
        color_level = "#ee3d55"

    else:
        color_level = "#fabd57"

    if num_data < 40:
        num_data = 40

    elif num_data > 80:
        num_data = 80

    # Plotting the figure of the gauge graph
    fig = go.Figure(

        # Defining type of graph and characteristics
        go.Indicator(
            mode = "gauge+number",
            value = num_data,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': ""},
            gauge = {

                    # limits for the gauge graphs min and max values
                    'axis': {'range': [40, 80], 'tickwidth': 1},

                    # color based on diameter to represent danger
                    'bar': {'color': f"{color_level}"},

                    # Dividing the graph in sectors GOOD/WORRY/CRITICAL
                    'steps': [
                        {'range': [40, 60], 'color': 'white'},
                        {'range': [60, 70], 'color': 'white'},
                        {'range': [70, 80], 'color': 'white'}],

                    # Treshold to alarm when diameter levels are critical 
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 70}

                    }
        )
    )

    # Setting gauge graph font size
    fig.update_traces(
        gauge_axis_tickfont = {
            'size': 25
        }
    )
    # Updating layout background to be the same as the frame, change font style and make a border around graph
    fig.update_layout(
        paper_bgcolor='#a4a8ad',
        font_family = f"{font}",

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

    # using update axes to format
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

    # Turning plot into image, then turning the image into a numpy array to pickle
    fig_bytes = fig.to_image(format="png")
    buf = io.BytesIO(fig_bytes)
    img = Image.open(buf)
    return np.asarray(img)


    
def graphProcess(): 
    global maior_diametro

    while True:
        try:
            # Loading pickled data
            with open('./dados_pickle/dadosPickle.pkl', 'rb') as f:
                dados = pickle.load(f)
            with open('./dados_pickle/horaPickle.pkl', 'rb') as f:
                tempo = pickle.load(f)

            ## UPDATES

            arr_gaugeimg = np.array([])

            # Plotting images
            if(np.any(dados) > 0):
                if(dados[-1] > maior_diametro):

                    maior_diametro = dados[-1] 
                    arr_gaugeimg = gaugeGraph(maior_diametro)

                    # Plays a sound after the diameter reaches a threshold
                    if(dados[-1] >= 80):
                        for note in melodie:
                            Beep(notes[note], 200)

            arr_lineimg = lineGraph(tempo, dados)

            # Storing images in pickle files
            storeData(arr_gaugeimg, './dados_pickle/gaugeGraphPickle.pkl')
            storeData(arr_lineimg, './dados_pickle/lineGraphPickle.pkl')
            
        except Exception as e:
            print(e)
            time.sleep(0.1)

if __name__ == '__main__':
    graphProcess()
