import subprocess
import os
import signal

class SubprocessManager():
    def StartSubprocess_Graphs(self):
        try:
            self.processSalvarImageGraphs = subprocess.Popen(['python', 'saveImageGraphs.py'], stdout=None, stderr=None)
        except subprocess.SubprocessError as e:
            print(e)

    def StartSubprocess_Segmentation(self):
        try:
            self.processSalvarImageSegmentado = subprocess.Popen(['python', 'saveImageSegmentado.py'], stdout=None, stderr=None)
        except subprocess.SubprocessError as e:
            print(e)

    def StartSubprocess_Database(self):
        try:
            self.processDataBase = subprocess.Popen(['python', 'database.py'], stdout=None, stderr=None)
        except subprocess.SubprocessError as e:
            print(e)

    def StartSubprocess_All(self):
        self.StartSubprocess_Segmentation()
        self.StartSubprocess_Graphs()
        self.StartSubprocess_Database()

    def KillSubprocess_All(self):
        self.KillSubprocess_Database()
        self.KillSubprocess_Graphs()
        self.KillSubprocess_Segmentation()

    def KillSubprocess_Graphs(self):
        try:
            os.kill(self.processSalvarImageGraphs.pid, signal.SIGTERM)
        except subprocess.SubprocessError as e:
            print(e)

    def KillSubprocess_Segmentation(self):
        try:
            os.kill(self.processSalvarImageSegmentado.pid, signal.SIGTERM)
        except subprocess.SubprocessError as e:
            print(e)

    def KillSubprocess_Database(self):
        try:
            os.kill(self.processDataBase.pid, signal.SIGTERM)
        except subprocess.SubprocessError as e:
            print(e)
   
    def ChecarSubprocessesDone(self):
        return (self.processSalvarImageGraphs != None and self.processSalvarImageSegmentado != None and self.processDataBase != None)
