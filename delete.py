import sqlite3
import random
from datetime import datetime
import time
import _pickle as pickle
import os


# Definindo conexao
conn =  sqlite3.connect(os.path.join(os.path.dirname(__file__), 'diametro_cascao.db'))
cursor = conn.cursor()

#cursor.execute("DELETE FROM cascao")

print(cursor.fetchall())
