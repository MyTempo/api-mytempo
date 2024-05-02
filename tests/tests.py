import requests

# URL da sua rota
url = 'http://localhost:3000/leitura/'

data = {'tag': 'exemplo'}


response = requests.post(url, data=data)

# Verificar a resposta
if response.status_code == 200:
    print("Requisição bem-sucedida!")
    print("Resposta do servidor:")
    print(response.json())
else:
    print("Erro:", response.status_code)
