from datetime import datetime
import _pickle as pickle
import sqlite3
import time


# Adding values to cascao table
def dbAdd(num_data, current_date, current_time):
    cursor.execute(f"INSERT INTO cascao (id_convertedor, id_lanca, diametro, data, horario) VALUES({1}, {1}, {num_data}, '{current_date}', '{current_time}')")   
    conn.commit()

# Print all values in cascao table
def dbShow():
    cursor.execute("SELECT rowid, * FROM cascao")
    results = cursor.fetchall()

    print(results)

# Delete all values in the database
def delete():
    cursor.execute("DELETE *")
    conn.commit()

# Loop for updating the database
while True:
    try:
        # Defining the db to connect
        conn =  sqlite3.connect('diametro_cascao.db')
        cursor = conn.cursor()

        # Creating the cascao table
        create_table = """CREATE TABLE IF NOT EXISTS cascao(
        id_convertedor INT,
        id_lanca INT,
        diametro FLOAT,
        data DATE,
        horario TIME)"""

        cursor.execute(create_table)
        conn.commit()

        # Loop to unpickle the data from the compacted files and save it on the database
        while True:
            try:
                #Loading pickled data
                with open('./dados_pickle/dadosPickle.pkl', 'rb') as f:
                    diameters = pickle.load(f)
                diameter = diameters[-1]
                with open('./dados_pickle/horaPickle.pkl', 'rb') as f:
                    times = pickle.load(f)
                time = times[-1]
                with open('./dados_pickle/dataPickle.pkl', 'rb') as f:
                    dates = pickle.load(f)
                date = dates[-1]

                # Inserting the values in the database
                dbAdd(diameter, date, time)
                
                # Waiting a second before reading again
                time.sleep(1)

            except Exception as e:
                # Treating error when reading or saving data
                print("Erro ao ler ou gravar dados:", str(e))

                # Waiting a second before trying again
                time.sleep(1)
                
                # Make a backup of the file after every hour
                if datetime.now().minute == 0:
                    backup_file = 'diametro_cascao_backup.db'
                    shutil.copyfile('diametro_cascao.db', backup_file)
                    print('Backup realizado com sucesso.')

    except Exception as e:
        # Treating error in the connection with the database
        print("Erro ao conectar ao banco de dados:", str(e))

        # Waiting 5 seconds before attempting to connect again
        time.sleep(5)




