import os
from datetime import datetime, timezone
from API.config.config import *
import pytz
import random

class Helpers:
    def __init__(self) -> None:
        self.created_at= ""

    def mount_url(protocol="http", mid_of_url="", route="/"):
        return f"{protocol}://{mid_of_url}{route}"
    
    def is_num(n):
        if isinstance(n, (int, float)):
            return True
        elif isinstance(n, str) and n.isnumeric():
            return True
        else:
            return False
        
    @staticmethod
    def get_file_timestamp_TmzBr(file_path):

        timestamp = os.path.getmtime(file_path)

        data_utc = datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)

        fuso_horario = pytz.timezone('America/Sao_Paulo')
        data_formatada = data_utc.astimezone(fuso_horario)

        return {'utc_file_timestamp': data_utc, 'formated_file_timestamp': data_formatada}
    
    @staticmethod
    def generateRandomNum(qtd):
        random_nums = [str(random.random()) for _ in range(qtd)]
        return ', '.join(random_nums)

    @staticmethod
    def generateRandomNum_int(qtd):
        return ''.join(str(random.randint(1, 9)) for _ in range(qtd))

    def FormatDeviceParams(deviceParams, hComm=""):
        formatted_data = {
            "hComm": hComm,
            "ACSADDR": deviceParams.get("ACSADDR"),
            "ACSDATALEN": deviceParams.get("ACSDATALEN"),
            "ANT": deviceParams.get("ANT"),
            "BAUDRATE": deviceParams.get("BAUDRATE"),
            "BUZZERTIME": deviceParams.get("BUZZERTIME"),
            "CN": deviceParams.get("CN"),
            "DEVICEARRD": deviceParams.get("DEVICEARRD"),
            "FILTERTIME": deviceParams.get("FILTERTIME"),
            "INTERNELTIME": deviceParams.get("INTERNELTIME"),
            "INTERFACE": deviceParams.get("INTERFACE"),
            "INVENTORYAREA": deviceParams.get("INVENTORYAREA"),
            "QVALUE": deviceParams.get("QVALUE"),
            "REGION": deviceParams.get("REGION"),
            "RFIDPOWER": deviceParams.get("RFIDPOWER"),
            "RFIDPRO": deviceParams.get("RFIDPRO"),
            "SESSION": deviceParams.get("SESSION"),
            "STEPFRE": deviceParams.get("STEPFRE"),
            "STRATFREI": deviceParams.get("STRATFREI"),
            "TRIGGLETIME": deviceParams.get("TRIGGLETIME"),
            "WGSET": deviceParams.get("WGSET"),
            "WORKMODE": deviceParams.get("WORKMODE"),
        }
        return formatted_data

    def generateTagFileName(self, session, tag_type="refined", created_at=TIME_FORMAT_2, file_type="json"):
        if(tag_type == "brute"):
            file_name = f'MyTempo-Bruto-Sess-{session} T-{created_at}.{file_type}'
        elif(tag_type == "refined"):
            file_name = f'MyTempo-Ref-Sess-{session} T-{created_at}.{file_type}'
        else:
            file_name = tag_type
        return file_name
    
