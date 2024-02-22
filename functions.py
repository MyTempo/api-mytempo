import json

def w_json(path, dados):
    with open(path, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

def r_json(path):
    with open(path, 'r') as arquivo:
        dados = json.load(arquivo)
    return dados