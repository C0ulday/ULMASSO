from decimal import Decimal
from datetime import datetime

def defineCodeOperation(OpList, ligne):
    myOpNb = []
    for Op in OpList:
        code = Op.code
        myOpNb.append(int(code[6:10]))
    myOpNb.sort(reverse = True)
    if myOpNb:
        maxNb = myOpNb[0]
    else:
        maxNb = 0
    newNum = str(maxNb+1)
    if len(newNum) == 1:
        newNum = '000' + newNum
    if len(newNum) == 2:
        newNum = '00' +  newNum
    if len(newNum) == 3:
        newNum = '0' +  newNum
    newCode = ligne.code + '-' + newNum
    return newCode

#Ajoute (si i = 2) ou soustrait (si i = 1) les montant de l'opération aux ligne, projet et section quand nouvelle opération
#On soustrait auparavant en cas de modification ou de suppression
def CalcAddBudget(activeOp):
    activeBudget = activeOp.budget
    activeLigne = activeOp.ligne
    activeProjet = activeLigne.projet
    activeSection = activeProjet.section
    #charges
    activeLigne.charge = Decimal(activeLigne.charge) + Decimal(activeOp.charge)
    activeProjet.charge = Decimal(activeProjet.charge) + Decimal(activeOp.charge)
    activeSection.charge = Decimal(activeSection.charge) + Decimal(activeOp.charge)
    activeBudget.charge = Decimal(activeBudget.charge) + Decimal(activeOp.charge)
    #produits
    activeLigne.produit = Decimal(activeLigne.produit) + Decimal(activeOp.produit)
    activeProjet.produit = Decimal(activeProjet.produit) + Decimal(activeOp.produit)
    activeSection.produit = Decimal(activeSection.produit) + Decimal(activeOp.produit)
    activeBudget.produit = Decimal(activeBudget.produit) + Decimal(activeOp.produit)
    #Sauvegardes
    activeLigne.save()
    activeProjet.save()
    activeSection.save()
    activeBudget.save()
    
def CalcSubBudget(activeOp):
    activeBudget = activeOp.budget
    activeLigne = activeOp.ligne
    activeProjet = activeLigne.projet
    activeSection = activeProjet.section
    #charges
    activeLigne.charge = Decimal(activeLigne.charge) - Decimal(activeOp.charge)
    activeProjet.charge = Decimal(activeProjet.charge) - Decimal(activeOp.charge)
    activeSection.charge = Decimal(activeSection.charge) - Decimal(activeOp.charge)
    activeBudget.charge = Decimal(activeBudget.charge) - Decimal(activeOp.charge)
    #produits
    activeLigne.produit = Decimal(activeLigne.produit) - Decimal(activeOp.produit)
    activeProjet.produit = Decimal(activeProjet.produit) - Decimal(activeOp.produit)
    activeSection.produit = Decimal(activeSection.produit) - Decimal(activeOp.produit)
    activeBudget.produit = Decimal(activeBudget.produit) - Decimal(activeOp.produit)
    #Sauvegardes
    activeLigne.save()
    activeProjet.save()
    activeSection.save()
    activeBudget.save()
    
def defineCodeCompteEpargneOperation(OpList):
    myOpNb = []
    for Op in OpList:
        code = Op.code
        myOpNb.append(int(code[3:7]))
    myOpNb.sort(reverse = True)
    maxNb = myOpNb[0]
    newNum = str(maxNb+1)
    if len(newNum) == 1:
        newNum = '000' + newNum
    if len(newNum) == 2:
        newNum = '00' +  newNum
    if len(newNum) == 3:
        newNum = '0' +  newNum
    newCode = 'CE-' + newNum
    return newCode

def CalcSubCompteEpargne(activeOp):
    activeCompteEpargne = activeOp.compteEpargne
    #charges
    activeCompteEpargne.charge = Decimal(activeCompteEpargne.charge) - Decimal(activeOp.charge)
    #produits
    activeCompteEpargne.produit = Decimal(activeCompteEpargne.produit) - Decimal(activeOp.produit)
    #Sauvegardes
    activeCompteEpargne.save()
    
def CalcAddCompteEpargne(activeOp):
    activeCompteEpargne = activeOp.compteEpargne
    #charges
    activeCompteEpargne.charge = Decimal(activeCompteEpargne.charge) + Decimal(activeOp.charge)
    #produits
    activeCompteEpargne.produit = Decimal(activeCompteEpargne.produit) + Decimal(activeOp.produit)
    #Sauvegardes
    activeCompteEpargne.save()
    
def defineCodeFacture(factureList):
    myFactureNb = []
    for facture in factureList:
        code = facture.code
        myFactureNb.append(int(code[9:13]))
    myFactureNb.sort(reverse = True)
    if myFactureNb:
        maxNb = myFactureNb[0]
    else:
        maxNb = 0
    newNum = str(maxNb+1)
    if len(newNum) == 1:
        newNum = '000' + newNum
    if len(newNum) == 2:
        newNum = '00' +  newNum
    if len(newNum) == 3:
        newNum = '0' +  newNum
    newCode = 'AUV-' + str(datetime.now().year) + '-' + newNum
    return newCode