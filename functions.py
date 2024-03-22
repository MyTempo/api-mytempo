import json
import subprocess
import sys
import os
from datetime import datetime, timedelta

def w_json(path, dados):
    with open(path, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

def r_json(path):
    with open(path, 'r') as arquivo:
        dados = json.load(arquivo)
    return dados

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

def sanitizeTimeInput(calculo):
    try:
        #tira as pontuações
        calculo = calculo.replace('-','')
        calculo = calculo.replace(' ','')
        calculo = calculo.replace(':','')
        calculo = calculo.replace('.','')
        return calculo
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
