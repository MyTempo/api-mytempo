import json
import subprocess
import sys
import os

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