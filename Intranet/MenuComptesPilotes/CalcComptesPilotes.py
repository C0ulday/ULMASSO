from math import floor
from decimal import Decimal

def calcDureeVol(horoInit, horoFin):
    horoInitMin = floor(horoInit)*60+(horoInit%1)*100
    horoFinMin = floor(horoFin)*60+(horoFin%1)*100
    return horoFinMin-horoInitMin

def calcPrixVol(dureeVol,instructeur,aeronef):
    if instructeur:
        prix = float(dureeVol*aeronef.tarifElevePilote)
    else:
        prix = float(dureeVol*aeronef.tarifPilote)
    if dureeVol >= 120 and dureeVol < 180 : #si temps de vol compris entre 2:00 et 3:00
        return prix * .9
    elif dureeVol > 180 : #si temps de vol supérieur à 3:00
        return prix * .85
    else :
        return Decimal(prix)

def calcTarifInstruction(dureeVol, instructeur, indemInstructeur):
    if instructeur:
        if indemInstructeur.value == "NON":
            if dureeVol < 30:
                tarif = 20
            else:
                tarif = 35
        else:
            tarif = 0
    else:
        tarif = 0
    return Decimal(tarif)

def calcChargeComptePilote(pilote, volAll):
    charge = Decimal(0)
    for vol in volAll:
        prixVol = vol.prixVol + vol.tarifInstruction - vol.remise
        charge += prixVol 
    report = pilote.reportComptePilote2024
    if report < 0:
        charge = charge - report
    return charge