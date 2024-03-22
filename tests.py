from datetime import datetime, timedelta

while True:
    try:
        inicio = input('Informe o horario de inicio do experimento (formato Horas:Minutos:Segundos): ')
        data_inicio = datetime.strptime(inicio, "%H:%M:%S")
        break
    except ValueError:
        print('Não foi digitada uma data válida no formato hh:mm:ss')

while True:
    try:
        duracao = input('Quanto tempo durara o experimento (formato Horas:Minutos:Segundos): ')
        horas, minutos, segundos = map(int, duracao.split(':'))
        duracao = timedelta(hours=horas, minutes=minutos, seconds=segundos)
        break
    except ValueError:
        print('Não foi digitada uma duração no formato hh:mm:ss')

termino = data_inicio + duracao
print(termino.strftime('%H:%M:%S'))