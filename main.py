from config import *
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS  
import requests

from system import System
from get_data import GetWebData
from readfiles import Intern
from helpers import Helpers
from ReaderData import *


app = Flask(__name__)
CORS(app)  # Configurações do CORS
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def template():
    return render_template('index.html', no_cache=True)

@app.route('/configurar/view/')
def template_configurar():
    return render_template('configurar.html')

@app.route('/actions/view/')
def template_acoes():
    return render_template('actions.html')


@app.route('/status', methods=['GET'])
def status_equip():
    return System.checkInternet();

@app.route('/dados_equipamento', methods=['GET'])
def equip_data():
    sys = System()
    return sys.getEquipInfo();

@app.route("/atualizar_equipamento", methods=['POST'])
def atualiza_equipamento():
    sys = System()
    upd_eqp = GetWebData()
    equip_info_response = sys.getEquipInfo()
    equip_info_data = json.loads(equip_info_response)  # Converte a string JSON em um objeto Python
    equip_model = equip_info_data.get("modelo")  # Acessa a chave "modelo" nos dados JSON

    result = upd_eqp.update_equip(equip_model, URL_DADOS_EQUIPAMENTO)

    if result['status'] == 'success':
        return jsonify(result), 200  
    else:
        return jsonify(result), 500

@app.route("/configurar/equipamento/", methods=["POST"])
def configurar_equipamento():
    if request.method == "POST":
        equip_data = request.json
        if(equip_data): 
            equip_name = equip_data.get("nome_equipamento")
            if(equip_name):
               equip_name = equip_data.get("nome_equipamento")
               dados_request = {
                   "nome_equipamento": equip_name
               }
               try:
                   response = requests.post(URL_DADOS_EQUIPAMENTO, json=dados_request)
                   dados = response.json()[0]
               
                   
                   gwt = GetWebData()
                   gwt.config_equip(dados)  
                    
                   return jsonify({
                        'data': dados,
                        'status': 'success',
                        'message': 'Sucesso ao configurar equipamento',
                        'erro': 0,
                        'retornomsg': "Equipamento configurado com sucesso!",
                        }) 
               except:
                    return jsonify({
                        'status': 'error',
                        'message': 'Falha ao configurar equipamento',
                        'erro': 1,
                        'retornomsg': "Falha ao configurado configurar equipamento!",
                        }) 
            else:
                        return jsonify({
                            "Message": "Parâmetros não passados corretamente."
                        })
            # response = requests.post(URL_DADOS_EQUIPAMENTO, json={
            #     "nome_equipamento": equip_name
            # })
            
            # return response
            

@app.route("/verifica_coleta")
def verificar_coleta():
    pass


@app.route("/buscar_arquivo/bruto/", methods=['POST', 'GET'])
def buscar_arquivo_bruto_last(session=None):
    Files = Intern()
    file_txt = None 
    try:
        file_txt = Files.getFileBySession(type_f=1)


        if file_txt is not None:
            msg = f"Sucesso ao buscar arquivo {file_txt}"
            return jsonify({
                'file_txt': file_txt,
                'status': 'success',
                'message': 'Sucesso ao buscar arquivo',
                'erro': 0,
                'retornomsg': msg,
                'considered_by': 'last_modified'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Não foi possível encontrar o arquivo',
                'erro': 1,
                'retornomsg': 'Arquivo não encontrado.',
                'considered_by': 'last_modified'

            })
    except:
        return jsonify({
            'status': 'error',
            'message': 'Ocorreu um erro crítico',
            'erro': 1,
            'retornomsg': 'Ocorreu um erro ao buscar arquivo.'
        })

@app.route("/buscar_arquivo/bruto/<string:session>", methods=['POST', 'GET'])
def buscar_arquivo_bruto(session):
    Files = Intern()
    file_txt = ""
    try:
        file_txt = Files.searchFileBySession(session, type_f=1)    
        if(file_txt is not None):
            msg = f"Sucesso ao buscar arquivo {file_txt}"
            return jsonify({
                'file_txt': file_txt,
                'status': 'success',
                'message': 'Sucesso ao buscar arquivo',
                'erro': 0,
                'retornomsg': msg,
                'considered_by': 'search_param'
                })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Não foi possível encontrar o arquivo',
                'erro': 1,
                'retornomsg': 'Arquivo não encontrado.',
                'considered_by': 'search_param'

            })
        
    except:
        return jsonify({
            'status': 'error',
            'message': 'Ocorreu um erro crítico',
            'erro': 1,
            'retornomsg': 'Ocorreu um erro ao buscar arquivo.'
        })
    
@app.route("/pegar/primeiros-tempos", methods=["POST"])
def refinar_arquivo():
    if(request.method == "POST"):
        r = ReaderData()
        return jsonify(r.getCompressedData())
    

# @app.route("/refinar/arquivo/<string:session>", methods=["GET"])
# def refinar_arquivo(session):
#     return jsonify({"session": session})

@app.route("/buscar_arquivo/refinado/", methods=['POST', 'GET'])
def buscar_arquivo_refinado_last():
    Files = Intern()
    file_txt = None 
    try:
        file_txt = Files.getFileBySession(type_f=0)


        if file_txt is not None:
            msg = f"Sucesso ao buscar arquivo {file_txt}"
            return jsonify({
                'file_txt': file_txt,
                'status': 'success',
                'message': 'Sucesso ao buscar arquivo',
                'erro': 0,
                'retornomsg': msg,
                'considered_by': 'last_modified'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Não foi possível encontrar o arquivo',
                'erro': 1,
                'retornomsg': 'Arquivo não encontrado.',
                'considered_by': 'last_modified'

            })
    except:
        return jsonify({
            'status': 'error',
            'message': 'Ocorreu um erro crítico',
            'erro': 1,
            'retornomsg': 'Ocorreu um erro ao buscar arquivo.'
        })



@app.route("/buscar_arquivo/refinado/<string:session>", methods=['POST', 'GET'])
def buscar_arquivo_refinado(session):
    Files = Intern()
    file_txt = ""
    try:
        file_txt = Files.searchFileBySession(session, type_f=0)    
        if(file_txt is not None):
            msg = f"Sucesso ao buscar arquivo {file_txt}"
            return jsonify({
                'file_txt': file_txt,
                'status': 'success',
                'message': 'Sucesso ao buscar arquivo',
                'erro': 0,
                'retornomsg': msg,
                'considered_by': 'search_param'
                })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Não foi possível encontrar o arquivo',
                'erro': 1,
                'retornomsg': 'Arquivo não encontrado.',
                'considered_by': 'search_param'

            })
        
    except:
        return jsonify({
            'status': 'error',
            'message': 'Ocorreu um erro crítico',
            'erro': 1,
            'retornomsg': 'Ocorreu um erro ao buscar arquivo.'
        })

@app.route("/listar_arquivos/brutos/", methods=['POST', 'GET'])
def listar_arquivos_brutos():
    f = Intern() 
    return f.listFilesDiff(type_f="brute")

@app.route("/listar_arquivos/refinados/", methods=['POST', 'GET'])
def listar_arquivos_refinados():
    f = Intern() 
    files = f.listFilesDiff(type_f="refined")
    return jsonify(files)

@app.route("/reader_status/", methods=['GET'])
def reader_status():
    R = ReaderData()
    return jsonify(R.ReaderStatus())

@app.route("/start_reader/", methods=['POST'])
def start_reader():
    Reader = ReaderData()
    return jsonify(Reader.Start_Reader())

@app.route("/stop_reader/", methods=['POST'])
def stop_reader():
    Reader = ReaderData()
    return jsonify(Reader.Stop_Reader())

@app.route("/iniciar/comunicacao/", methods=['POST'])
def iniciar_envio():
    if(request.method == "POST"):
        r = ReaderData()
        # return jsonify()
        r.uploadPrimeirosTempos()
        return jsonify({
                "status": "success",
                "message": "Comunicando!"
            })
    
# @app.route("/insert/tempos", methods=["POST"])
# def insere_na_tabela():
#     data = request.json  
#     if data and "acao" in data:
#         acao = data["acao"]
#         if acao == "ligar":
#             # r.toggleEnvio(True)
            
            
#             return jsonify({
#                 "status": "success",
#                 "message": "Comunicando!"
#             })
#         elif acao == "desligar":
#             # r.toggleEnvio(False)
#             return jsonify({
#                 "status": "success",
#                 "message": "Comunicação pausada com sucesso!"
#             })
#         else:
#             return "Ação desconhecida", 400
#     else:
#         return "Dados inválidos", 400

@app.route("/limpar/atletas_local", methods=["POST"])
def apagar_atletas():
    from MyTempo import MyTempo
    m = MyTempo()
    m.emptyAthletesTable()
    return jsonify({
        "status": "success",
        "message": "Atletas do equipamento apagados com sucesso!"
    })

@app.route("/atletas_chegaram", methods=["GET"])
def atletas_chegaram():
    server = r_json(path=SERVER_CONFIG_FILE_PATH)
    response = requests.get(Helpers.mount_url("http", f"{server['server_ip']}:{server['port']}", "/dados_equipamento"))
    dados = response.json()
    idprova = dados.get('idprova')
    equip = dados.get('equipamento')
    db = Database()
    results = db.executeQuery(f"SELECT DISTINCT * FROM tempos WHERE idprova = {idprova} AND idequipamento = {equip}")
    return jsonify({
        "status": "success",
        "message": "",
        "data": results
    })