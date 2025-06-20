import io
import os 
from datetime import date
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

from Intranet.models import Member,\
                            BudgetOperation,\
                            Vol
from ULMASSO.settings import BASE_DIR
from Internet.views import dateTimeParis

def genererBufferComptePilote(idPilote):
    myPilote = Member.objects.get(pk = idPilote)
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    width, height = A4
    p = Canvas(buffer, pagesize = A4, bottomup=1)
    #Logo AUV
    p.drawImage(os.path.join(BASE_DIR, "ULMASSO/static/img/logo_AUV.png"), 30, height - 110, width = 100, height = 100, preserveAspectRatio = True, mask='auto')
    #Nom du pilote et date
    p.setFont("Helvetica-Bold", 14)
    p.drawString(140, height - 30, "Compte Pilote de " + str(myPilote))
    p.setFont("Helvetica", 12)
    p.drawString(140, height - 50, str(dateTimeParis()))
    #Résumùé compte
    lines = [['Total des virements à AUV', str(myPilote.produitComptePilote) + ' €'],
             ['Total des vols', str(myPilote.chargeComptePilote) + ' €'],
             ['Bilan', str(myPilote.bilanComptePilote) + ' €']
             ]
    t = Table(lines)
    listStyle = TableStyle([('ALIGN', (-1,1),(-1,-1),'RIGHT'),
                            ('BOX', (0,0), (-1,-1), 1, colors.black),
                            ('FONT', (0,0), (-1,-1), 'Helvetica', 10),
                            ])
    if myPilote.bilanComptePilote < 0:
        listStyle.add('BACKGROUND',(-1,-1), (-1,-1), colors.lightcoral)
    else:
        listStyle.add('BACKGROUND',(-1,-1), (-1,-1), colors.lightgreen)    
    t.setStyle(listStyle)
    t.wrapOn(p,width,height)
    t.drawOn(p,width - 220 ,height - 100)
    #ligne de séparation
    dHeight = 120
    p.line(30, height-dHeight, width-30, height-dHeight)
    #Carnet de vol (10 derniers vols) - Titre
    p.setFont("Helvetica-Bold", 12)
    dHeight = dHeight + 30
    p.drawString(30, height - dHeight, "Carnet de vol (10 derniers vols)")
    #Carnet de vol (10 derniers vols) - Tableau
    lines = [['date', 'Aeronef', 'Horo début', 'Horo fin', 'Durée (mn)', 'Tarif vol', 'Instruction','Remise','Prix total']
            ]
    allVol = Vol.objects.filter(pilote = myPilote)
    myVol = []
    for vol in allVol:
        myVol.append(vol)   
    if len(myVol) < 10:
        ind = len(myVol)
    else:
        ind = 10
    for i in range(ind):
        lines.append([str(myVol[i].date.strftime("%d/%m/%y")),
                      str(myVol[i].aeronef),
                      str(myVol[i].horoInit),
                      str(myVol[i].horoFin),
                      str(myVol[i].dureeVol),
                      str(myVol[i].prixVol) + ' €',
                      str(myVol[i].tarifInstruction) + ' €',
                      str(myVol[i].remise) + ' €',
                      str(myVol[i].prixVol + vol.tarifInstruction - vol.remise) + ' €'])
    t = Table(lines)
    listStyle = TableStyle([('ALIGN',(2,1),(-1,-1),'RIGHT'),
                            ('ALIGN',(0,0),(-1,0),'CENTER'),
                            ('GRID', (0,0), (-1,-1), 1, colors.black),
                            ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 9),
                            ('FONT', (0,1), (-1,-1), 'Helvetica', 9),
                            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                            ])
    t.setStyle(listStyle)
    t.wrapOn(p,width,height)
    dHeight = dHeight + 20 + (ind+1)*18
    t.drawOn(p,50 ,height - dHeight)
    #Virements aux titre de l'instruction ou de la location (10 derniers virements) - Titre
    p.setFont("Helvetica-Bold", 12)
    dHeight = dHeight + 30
    p.drawString(30, height - dHeight, "Virements aux titre de l'instruction ou de la location (10 derniers virements)")
    #Virements aux titre de l'instruction ou de la location (10 derniers virements) - Tableau
    lines = [['date', 'Produits', 'Charge']
             ]
    allOp = BudgetOperation.objects.filter(beneficiaire = myPilote)
    myOp = []
    for Op in allOp:
        myOp.append(Op)
    if len(myOp) < 10:
        if myPilote.reportComptePilote2024 < 0:
            lines.append([str(date(2025,1,1).strftime("%d/%m/%y")),
                          str(0.00) + ' €',
                          str(myPilote.reportComptePilote2024*(-1))])
        else:
            lines.append([str(date(2025,1,1).strftime("%d/%m/%y")),
                          str(myPilote.reportComptePilote2024),
                          str(0.00) + ' €'])
        ind = len(myOp)
    else:
        ind = 10
    for i in range(ind):
        lines.append([str(myOp[i].date.strftime("%d/%m/%y")),
                      str(myOp[i].produit) + ' €',
                      str(myOp[i].charge) + ' €'])
    t = Table(lines)
    listStyle = TableStyle([('ALIGN',(1,1),(-1,-1),'RIGHT'),
                            ('ALIGN',(0,0),(-1,0),'CENTER'),
                            ('GRID', (0,0), (-1,-1), 1, colors.black),
                            ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 9),
                            ('FONT', (0,1), (-1,-1), 'Helvetica', 9),
                            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                            ])
    t.setStyle(listStyle)
    t.wrapOn(p,width,height)
    dHeight = dHeight + 20 + (ind+1)*18
    t.drawOn(p,50 ,height - dHeight)
    #Signature Trésorier
    p.setFont("Helvetica-Oblique", 12)
    dHeight = dHeight + 30
    p.drawString(width - 150, height - dHeight, "Édité à Chabeuil")
    p.drawString(width - 150, height - dHeight-20, "Le " + str(date.today().strftime("%d/%m/%y")))
    p.drawString(width - 150, height - dHeight-40, "Le trésorier d'AUV")
    #ligne de séparation
    dHeight = 750
    p.line(30, height-dHeight, width-30, height-dHeight)
    #Adresse AUV
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(30, height - dHeight - 20, "Aéro-ULM-Valence, Pôle Aviation Légère, 730 Chemin du Vol à Voile, 26120 Chabeuil - 06 66 65 23 39 - aero-ulm-valence@orange.fr")

    p.showPage()
    p.save()
    
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return buffer
    