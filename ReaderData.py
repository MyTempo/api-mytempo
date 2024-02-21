import requests
from config import *
import json
from datetime import datetime
from functions import *

class ReaderData:
    def __init__(self) -> None:
        pass

    def ReaderStatus(url=""):
        response = requests.post(url=url)
        

