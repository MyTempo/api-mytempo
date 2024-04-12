# API-MyTempo - Reader Connection Interface
<sub><sup><div style="opacity:0.5">
  Aplicação em fase de Desenvolvimento
</div></sup></sub>

## Nota importante ⚠️
### A aplicação está em fase inicial de desenvolvimento e qualquer falha ou bug devem ser contatadas ao desenvolvedor 

#### - Kerlon

---

## | System Routes

### | Obtendo dados do Equipamento
1. **Status**
   - Rota: `/status`
   - Método: `GET`

2. **Dados do Equipamento**
   - Rota: `/dados_equipamento`
   - Método: `GET`

3. **Status do Leitor**
   - Rota: `/reader_status`
   - Método: `GET`


### | Configurando Equipamento
1. **Configurar Equipamento**
   - Rota: `/configurar/equipamento/`
   - Método: `POST`
   - Dados Requeridos 
   ```json
   "nome_equipamento":  "EXEMPLO LEITOR RFID999"
   ```

2. **Atualizar dados do Equipamento**
   - Rota: `/atualizar_equipamento`
   - Método: `POST`

### | Obtendo Dados e Processando os arquivos 
1. **Listar arquivos Brutos**
   - Rota: `/listar_arquivos/brutos/`
   - Métodos: `POST` `GET`

2. **Listar arquivos Refinados**
   - Rota: `/listar_arquivos/refinados/`
   - Métodos: `POST` `GET`

3. **Buscar Arquivo Bruto**
   - Considerando mais recente no servidor
   - Rota: `/buscar_arquivo/bruto/`
   - Método: `POST` `GET`

4. **Buscar Arquivo Bruto pelo nome**
   - Considerando mais recente no servidor
   - Rota: `/buscar_arquivo/bruto/<string:session>`
   - Método: `POST` `GET`

5. **Buscar Arquivo Refinado**
   - Considerando mais recente no servidor
   - Rota: `/buscar_arquivo/refinado/`
   - Método: `POST` `GET`

6. **Buscar Arquivo Refinado pelo nome**
   - Considerando mais recente no servidor
   - Rota: `/buscar_arquivo/refinado/<string:session>`
   - Método: `POST` `GET`

7. **Pegar os primeiros tempos e atletas pelo arquivo mais recente**
   - Considerando mais recente no servidor
   - Rota: `/pegar/primeiros-tempos`
   - Método: `POST`

### | Operações do leitor

1. **Iniciar o leitor e gravar o arquivo**
   - Rota: `/start_reader/`
   - Método: `POST`

2. **Para o leitor e todos os processos**
   - Rota: `/stop_reader/`
   - Método: `POST`
