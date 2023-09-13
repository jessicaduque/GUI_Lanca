import sqlite3
import random
from datetime import datetime
import time
import _pickle as pickle

# Adicionando valores na tabela cascao
def dbAdd(numData, current_date, current_time):
    cursor.execute(f"INSERT INTO cascao (id_convertedor, id_lanca, diametro, data, horario) VALUES({1}, {1}, {numData}, '{current_date}', '{current_time}')")   
    conn.commit()

def dbShow():
    cursor.execute("SELECT rowid, * FROM cascao")

    results = cursor.fetchall()

    print(results)

def delete():
    cursor.execute("DELETE *")
    conn.commit()


while True:
    try:
        # Definindo conexao
        conn =  sqlite3.connect('diametro_cascao.db')
        cursor = conn.cursor()

        # Criando tabela do Cascao 
        create_table = """CREATE TABLE IF NOT EXISTS cascao(
        id_convertedor INT,
        id_lanca INT,
        diametro FLOAT,
        data DATE,
        horario TIME)"""

        cursor.execute(create_table)
        conn.commit()

        # Loop para realizar a medição e salvar os dados no banco de dados
        while True:
            try:
                #Load pickled data
                with open('./dados_pickle/dadosPickle.pkl', 'rb') as f:
                    dados = pickle.load(f)
                diametro = dados[0]

                with open('./dados_pickle/horaPickle.pkl', 'rb') as f:
                    horas = pickle.load(f)
                hora = horas[-1]

                with open('./dados_pickle/dataPickle.pkl', 'rb') as f:
                    datas = pickle.load(f)
                data = datas[-1]

                # Inserir os dados no banco de dados
                dbAdd(diametro, data, hora)
                
                #print("Dados atuais gravados no database. Tam_med: ", tam_med)
                
                # Aguardar um segundo antes da próxima leitura
                time.sleep(1)

            except Exception as e:
                # Tratar exceção de falha na leitura ou gravação de dados
                print("Erro ao ler ou gravar dados:", str(e))
                time.sleep(1)  # Aguardar 1 segundo antes de tentar novamente
                
                # Fazer backup do arquivo a cada hora
                if datetime.now().minute == 0:
                    backup_file = 'diametro_cascao_backup.db'
                    shutil.copyfile('diametro_cascao.db', backup_file)
                    print('Backup realizado com sucesso.')

    except Exception as e:
        # Tratar exceção de falha na conexão com o banco de dados
        print("Erro ao conectar ao banco de dados:", str(e))
        time.sleep(5)  # Aguardar 5 segundos antes de tentar reconectar




