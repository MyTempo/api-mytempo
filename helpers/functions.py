import json
import subprocess
import sys
import os
from datetime import datetime, timedelta
import sqlite3

def w_json(path, dados):
    with open(path, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

def r_json(path):
    with open(path, 'r') as arquivo:
        dados = json.load(arquivo)
    return dados

def w_json_if_not_exists(path, dados):
    if not os.path.exists(path):
        with open(path, 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)


def update_json_value(path, key, new_value):
    try:
        with open(path, 'r+') as arquivo:
            dados = json.load(arquivo)
            dados[key] = new_value
            arquivo.seek(0)
            json.dump(dados, arquivo, indent=4)
            arquivo.truncate()
    except FileNotFoundError:
        print(f"O arquivo '{path}' não foi encontrado.")

def a_json(path, dados):
    with open(path, 'a') as arquivo:
        json.dump(dados, arquivo, indent=4)

def verify_and_create(dir_):
    if not os.path.exists(dir_):
        os.makedirs(dir_)

def restart_server():
        try:
            current_script = sys.argv[0]
            subprocess.Popen([sys.executable, current_script])
            sys.exit()
        except Exception as e:
            print(f"Erro ao reiniciar o servidor: {e}")

def sanitizeTimeInput(string_):
    try:
        #tira as pontuações
        string_ = string_.replace('-','')
        string_ = string_.replace(' ','')
        string_ = string_.replace(':','')
        string_ = string_.replace('.','')
        return string_
    except Exception as e:
        print(f"Erro ao formatar tempo: err -> {e}")


def formatar_tempo(delta):
    if delta is None:
        return None
    
    horas, segundos = divmod(delta.seconds, 3600)
    minutos, segundos = divmod(segundos, 60)
    return '{:02}:{:02}:{:02}'.format(horas, minutos, segundos)

def sum_time(tempo_inicial_str, intervalo_str):
    tempo_inicial = datetime.strptime(tempo_inicial_str, "%H:%M:%S")
    intervalo_tempo = timedelta(hours=intervalo_str.split(':')[0], minutes=intervalo_str.split(':')[1], seconds=intervalo_str.split(':')[2])

    tempo_final = tempo_inicial + intervalo_tempo
    
    tempo_final_str = tempo_final.strftime("%H:%M:%S")
    
    return tempo_final_str

def get_sys_db_schemas(database):
    conn = sqlite3.connect(database)

    cursor = conn.cursor()

    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")

    create_commands = cursor.fetchall()

    for command in create_commands:
        print(command[0])

    conn.close()
