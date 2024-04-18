import subprocess

def get_localtunnel_url(port):
    try:
        result = subprocess.run(['lt', '--port', str(port)], capture_output=True, text=True, check=True)
        url = result.stdout.strip().split()[-1]
        return url
    except subprocess.CalledProcessError as e:
        print("Erro ao executar o comando lt:", e)
    except Exception as e:
        print("Ocorreu um erro:", e)

port = 3000

url = get_localtunnel_url(port)
print("URL do LocalTunnel:", url)
