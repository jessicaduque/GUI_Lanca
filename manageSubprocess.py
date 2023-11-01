import subprocess
import os
import signal

def StartSubprocess_Graphs():
    global processSalvarImageGraphs

    try:
        processSalvarImageGraphs = subprocess.Popen(['python', 'saveImageGraphs.py'], stdout=None, stderr=None)
        print(processSalvarImageGraphs)
    except subprocess.SubprocessError as e:
        print(e)

def StartSubprocess_Segmentation():
    global processSalvarImageSegmentado

    try:
        processSalvarImageSegmentado = subprocess.Popen(['python', 'saveImageSegmentado.py'], stdout=None, stderr=None)
    except subprocess.SubprocessError as e:
        print(e)

def StartSubprocess_Database():
    global processDataBase

    try:
        processDataBase = subprocess.Popen(['python', 'database.py'], stdout=None, stderr=None)
    except subprocess.SubprocessError as e:
        print(e)

def StartSubprocess_All():
    StartSubprocess_Segmentation()
    StartSubprocess_Graphs()
    StartSubprocess_Database()

def KillSubprocess_All():
    KillSubprocess_Database()
    KillSubprocess_Graphs()
    KillSubprocess_Segmentation()

def KillSubprocess_Graphs():
    try:
        os.kill(processSalvarImageGraphs.pid, signal.SIGTERM)
        print(processSalvarImageGraphs)
    except subprocess.SubprocessError as e:
        print(e)

def KillSubprocess_Segmentation():
    try:
        os.kill(processSalvarImageSegmentado.pid, signal.SIGTERM)
    except subprocess.SubprocessError as e:
        print(e)

def KillSubprocess_Database():
    try:
        os.kill(processDataBase.pid, signal.SIGTERM)
    except subprocess.SubprocessError as e:
        print(e)
   
def ChecarSubprocessesDone():
    return (processSalvarImageGraphs != None and processSalvarImageSegmentado != None and processDataBase != None)
