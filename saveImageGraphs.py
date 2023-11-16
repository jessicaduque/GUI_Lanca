import plotly.graph_objects as go
import plotly.express as px
from winsound import Beep
import _pickle as pickle
from PIL import Image
import pandas as pd
import numpy as np
import warnings
from time import sleep
import gc
import io 

warnings.filterwarnings("ignore")

gc.enable()

max_diameter = 0

# Defining global font
font = "Raleway"

#SAVE IMAGE DATA IN PICKLE FILE TO BE USED BY THE DASH PROGRAM.
def storeData(data, path):

    print("stored data 123456789")

    # initializing data to be stored in db 
    db = (data)

    # Its important to use binary mode 
    dbfile = open(path, 'wb') 

    # source, destination 
    pickle.dump(db, dbfile)         
    dbfile.close()

# Line graph to show all values inside the queues
def line_graph(queue_time, queue_data):

    # Dataframe dictionary with the xy values of the graph
    df = pd.DataFrame(dict(
        x_axis = list(queue_time),
        y_axis = list(queue_data)
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
def gauge_graph(num_data):

    # Changing the color of the graph's bar based on the diameter
    if num_data < 60:
        color_level = "#4dab6d"
    elif num_data >= 70:
        color_level = "#ee3d55"
    else:
        color_level = "#fabd57"

    # Plotting the figure of the gauge graph
    fig = go.Figure(

        # Defining type of graph and characteristics
        go.Indicator(
            mode = "gauge+number",
            value = num_data,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Diametro"},
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
                        'value': 79}

                    }
        )
    )
    # Setting gauge graph font size
    fig.update_traces(
        gauge_axis_tickfont = {
            'size': 15
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

# Function to store the data from both graphs
def graph_process(): 
    global max_diameter

    while True:
        try:

            # Load pickled data
            with open('./pickle_data/diameter_pickle.pkl', 'rb') as f:
                diameter = pickle.load(f)
            with open('./pickle_data/time_pickle.pkl', 'rb') as f:
                time = pickle.load(f)

            ## UPDATES

            #arr_gaugeimg = gauge_graph(diameter[-1])

            # Plotting images
            if(np.any(diameter)):
                if(diameter[-1] > max_diameter):

                    print("data -1: " + str(diameter[-1]))
                    max_diameter = diameter[-1] 
                    arr_gaugeimg = gauge_graph(max_diameter)


            arr_lineimg = line_graph(time, diameter)

            # Storing images in pickle files
            print("skjdkajdkasjdkajksdjakjdkdjaksd")
            storeData(arr_gaugeimg, './pickle_data/gaugeGraph_pickle.pkl')
            storeData(arr_lineimg, './pickle_data/lineGraph_pickle.pkl')
            
        except Exception as e:
            print(e)
            sleep(0.1)

if __name__ == '__main__':
    graph_process()
