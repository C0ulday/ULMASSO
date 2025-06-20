from math import floor

def calcTpsHHMM(tps):
    if int(tps) > 0:
        tpsHeure = floor(tps/60)
        tpsMinute = tps - tpsHeure*60
        if tpsMinute >= 60:
            tpsHeure += 1
            tpsMinute -= 60
    else:
        tpsHeure = 0
        tpsMinute = 0
    return [round(tpsHeure,2), round(tpsMinute,2)]


def calcTpsVol(allVol):
    tpsVol = 0
    for vol in allVol:
        tpsVol += vol.dureeVol
    return calcTpsHHMM(tpsVol)

def calcTpsTypeVol(allVol):
    tpsVolMaintenance = 0
    tpsVolDecouverte = 0
    tpsVolLocation = 0
    tpsVolInstruction = 0
    for vol in allVol:
        if vol.maintenance.id == 2:
            tpsVolMaintenance += vol.dureeVol
        elif vol.bapteme.id == 2:
            tpsVolDecouverte += vol.dureeVol
        elif vol.instructeur :
            tpsVolInstruction += vol.dureeVol
        else:
            tpsVolLocation += vol.dureeVol
       
    return [tpsVolMaintenance,
            tpsVolDecouverte,
            tpsVolInstruction,
            tpsVolLocation
            ]

def calcVolEssence(allOpCarburant):
    volume = 0
    for op in allOpCarburant:
        allText = op.name.split()
        for text in allText:
            if ("l" in text) and ("." in text):
                text = text.strip('l')
                volume = volume + float(text)
    return round(volume,2)

def calcConsommation(tpsVol, volume):
    tpsVolHeure = tpsVol[0]+(tpsVol[1]/60)
    if tpsVolHeure > 0:
        consommation = round(volume/tpsVolHeure,2)
    else:
        consommation = 0
    return round(consommation,2)