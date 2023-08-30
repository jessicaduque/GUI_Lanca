import sqlite3
import random
from datetime import datetime

# Definindo conexao
connection =  sqlite3.connect('diametro_cascao.db')

cursor = connection.cursor()

# Criando tabela do Cascao 
create_table = """CREATE TABLE IF NOT EXISTS cascao(
id_convertedor INT,
id_lanca INT,
diametro FLOAT,
data DATE,
horario TIME)"""

cursor.execute(create_table)

#adicionando valores na tabela cascao
def dbAdd(numData, current_date, current_time):
    cursor.execute(f"INSERT INTO cascao (id_convertedor, id_lanca, diametro, data, horario) VALUES({1}, {1}, {numData}, '{current_date}', '{current_time}')")   
    connection.commit()

'''
for i in range(1, 6):
    numData = random.randrange(40, 80)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    databaseAdd(numData, current_time)
'''

def dbShow():
    cursor.execute("SELECT rowid, * FROM cascao")

    results = cursor.fetchall()

    print(results)

def delete():
    cursor.execute("DELETE *")
    connection.commit
