#Imports externes
from zoneinfo import ZoneInfo
from datetime import datetime

#Date et Heure fuseau Paris
def dateTimeParis():
    now = datetime.now(tz = ZoneInfo("Europe/Paris"))
    return now.strftime("%d/%m/%Y %H:%M")