# from django.contrib.auth.models import User
# User.objects.create_superuser(username = 'LegreneurP', email='pierre.legreneur@wanadoo.fr', password='093838_VdH')
#Imports externes
from django.db import models
from datetime import datetime, date

#Imports internes
from Intranet.MenuComptesPilotes.CalcComptesPilotes import calcDureeVol,\
                                                            calcPrixVol
                                                            
class OuiNon(models.Model):
    def __str__(self):
        text = self.value
        return text
    value = models.CharField(max_length = 3) 
#*****************************************************************************************
#Membres
    #Membres
class Member(models.Model):
    def __str__(self):
        return self.name + " " + self.vorname
    statut = models.ForeignKey('Statut',
                               on_delete=models.CASCADE,
                               default = 5)
    name = models.CharField(max_length = 50)
    vorname = models.CharField(max_length = 50)
    password = models.CharField(max_length = 20,
                                default = '0000')
    genre = models.ForeignKey('Sex',
                               on_delete=models.CASCADE,
                               default = 1)
    birthday = models.DateField(blank = True,
                                null = True)
    phone = models.CharField(max_length = 14,
                             blank=True,
                             null = True)
    email = models.EmailField(max_length = 50,
                              blank=True,
                              null = True)
    zip = models.CharField(max_length = 5,
                           blank=True,
                           null = True)
    city = models.CharField(max_length = 50,
                            blank=True,
                            null = True)
    adress = models.CharField(max_length = 200,
                              blank=True,
                              null = True)
    licenceFFPLUM = models.CharField(max_length = 6,
                                     blank = True,
                                     null = True)
    licenceAUV = models.ForeignKey(OuiNon,
                                on_delete=models.CASCADE,
                                related_name='licenceAUVOuiNon',
                                default = 1)
    brevetInstructeur = models.ForeignKey(OuiNon,
                                on_delete=models.CASCADE,
                                related_name='brevetInstructeurOuiNon',
                                default = 1)  
    datePiloteC2 = models.DateField(blank = True,
                                null = True)
    datePiloteC3 = models.DateField(blank = True,
                                null = True)
    datePiloteC4 = models.DateField(blank = True,
                                null = True)
    dateEmportC2 = models.DateField(blank = True,
                                null = True)
    dateEmportC3 = models.DateField(blank = True,
                                null = True)
    dateEmportC4 = models.DateField(blank = True,
                                null = True)
    dateBaptemeC2 = models.DateField(blank = True,
                                null = True)
    dateBaptemeC3 = models.DateField(blank = True,
                                null = True)
    dateBaptemeC4 = models.DateField(blank = True,
                                null = True)
    reportComptePilote2024 = models.DecimalField(decimal_places = 2,
                                                 max_digits = 8,
                                                 default = 00.00)
    produitComptePilote = models.DecimalField(decimal_places = 2,
                                            max_digits = 8,
                                            default = 00.00)
    chargeComptePilote = models.DecimalField(decimal_places = 2,
                                            max_digits = 8,
                                            default = 00.00)
    @property
    def bilanComptePilote(self):
        return self.produitComptePilote - self.chargeComptePilote
    def age(self):
        age = date.today()-self.birthday
        return int((age).days/365.25)
    
    class Meta:
        ordering = ['name','vorname']

        #Genre
class Sex(models.Model):
    def __str__(self):
        return self.genre
    genre = models.CharField(max_length = 1,
                             default = 'M')

    #Statut dans l'association
class Statut(models.Model):
    def __str__(self):
        return self.value
    value = models.CharField(max_length = 30)
#*****************************************************************************************

#Budget Budget->Section->Projet->Ligne->Opération
    #Budget
class BudgetBudget(models.Model):
    def __str__(self):
        text = 'Budget ' + self.year
        return text
    year = models.CharField(max_length = 4,
                            default = datetime.now().year)
    charge = models.DecimalField(decimal_places = 2,
                                 max_digits = 8,
                                 default = 00.00)
    produit = models.DecimalField(decimal_places = 2,
                                max_digits = 8,
                                default = 00.00)
    @property
    def resultat(self):
        return self.produit - self.charge
    
    class Meta:
        ordering = ['year']
    
    #Section
class BudgetSection(models.Model):
    def __str__(self):
        text = self.code + " - " + self.name
        if len(text) > 30:
            text = text[0:30] + '...'
        return text
    name = models.CharField(max_length = 100)
    code = models.CharField(max_length = 5)
    charge = models.DecimalField(decimal_places = 2,
                                 max_digits = 8,
                                 default = 00.00)
    produit = models.DecimalField(decimal_places = 2,
                                max_digits = 8,
                                default = 00.00)
    @property
    def resultat(self):
        return self.produit - self.charge
    
    class Meta:
        ordering = ['code']
    
    #Projet
class BudgetProjet(models.Model):
    def __str__(self):
        text = self.code + " - " + self.name
        if len(text) > 30:
            text = text[0:30] + '...'
        return text
    name = models.CharField(max_length = 100)
    code = models.CharField(max_length = 5)
    section = models.ForeignKey('BudgetSection',
                               on_delete=models.CASCADE,
                               default = 0,
                               null=True)
    charge = models.DecimalField(decimal_places = 2,
                                 max_digits = 8,
                                 default = 00.00)
    produit = models.DecimalField(decimal_places = 2,
                                max_digits = 8,
                                default = 00.00)
    @property
    def resultat(self):
        return self.produit - self.charge
    
    class Meta:
        ordering = ['code']

    #Ligne
class BudgetLigne(models.Model):
    def __str__(self):
        text = self.code + " - " + self.name
        if len(text) > 30:
            text = text[0:30] + '...'
        return text
    name = models.CharField(max_length = 100)
    code = models.CharField(max_length = 5)
    projet = models.ForeignKey('BudgetProjet',
                               on_delete=models.CASCADE,
                               default=0,
                               null=True)
    charge = models.DecimalField(decimal_places = 2,
                                 max_digits = 8,
                                 default = 00.00)
    produit = models.DecimalField(decimal_places = 2,
                                max_digits = 8,
                                default = 00.00)
    @property
    def resultat(self):
        return self.produit - self.charge
    
    class Meta:
        ordering = ['code']
    
class BudgetOperation(models.Model):
    def __str__(self):
        text = self.code + " - " + self.name
        if len(text) > 30:
            text = text[0:30] + '...'
        return text
    date = models.DateField(blank = True,
                            null = True)
    name = models.CharField(max_length = 100)
    code = models.CharField(max_length = 10,
                            default = "PXXXX-0000")
    budget = models.ForeignKey('BudgetBudget',
                               on_delete=models.CASCADE,
                               default = 0)
    ligne = models.ForeignKey('BudgetLigne',
                              on_delete = models.CASCADE,
                              blank = True,
                              null = True)
    beneficiaire = models.ForeignKey('Member',
                                     on_delete = models.CASCADE,
                                     blank = True,
                                     null = True)
    aeronef = models.ForeignKey('Aeronef',
                                 on_delete = models.CASCADE,
                                 blank = True,
                                 null = True)
    charge = models.DecimalField(decimal_places = 2,
                                 max_digits = 8,
                                 default = 00.00)
    produit = models.DecimalField(decimal_places = 2,
                                  max_digits = 8,
                                  default = 00.00)
    @property
    def resultat(self):
        return self.produit - self.charge
    
    class Meta:
        ordering = ['-date','code']

#Compte Epargne
class CompteEpargne(models.Model):
    def __str__(self):
        text = self.name
        return text
    name = models.CharField(max_length = 50)
    charge = models.DecimalField(decimal_places = 2,
                                 max_digits = 8,
                                 default = 00.00)
    produit = models.DecimalField(decimal_places = 2,
                                max_digits = 8,
                                default = 00.00)
    @property
    def resultat(self):
        return self.produit - self.charge
        
class CompteEpargneOperation(models.Model):
    def __str__(self):
        text = self.code + " - " + self.name
        if len(text) > 30:
            text = text[0:30] + '...'
        return text
    date = models.DateField(blank = True,
                            null = True)
    name = models.CharField(max_length = 100)
    code = models.CharField(max_length = 9,
                            default = "CE-0000")
    compteEpargne = models.ForeignKey('CompteEpargne',
                               on_delete=models.CASCADE,
                               default = 1)
    charge = models.DecimalField(decimal_places = 2,
                                 max_digits = 8,
                                 default = 00.00)
    produit = models.DecimalField(decimal_places = 2,
                                max_digits = 8,
                                default = 00.00)
    @property
    def resultat(self):
        return self.produit - self.charge

    class Meta:
        ordering = ['-date','code']

#Générateur facture
    #Facture
class Facture(models.Model):
    def __str__(self):
        text = self.code + " - " + self.clientName
        return text
    code = models.CharField(max_length = 13,
                            default = 'AUV-2025-0000')
    date = models.DateField(blank = True,
                            null = True)
    acquite = models.ForeignKey(OuiNon,
                                on_delete=models.CASCADE,
                                related_name='acquiteOuiNon',
                                default = 1)
    clientName = models.CharField(max_length = 50)
    clientVorname = models.CharField(max_length = 50,
                                     blank = True,
                                     null = True)
    clientZip = models.CharField(max_length = 5,
                                 blank = True,
                                 null = True)
    clientCity = models.CharField(max_length = 50,
                                  blank = True,
                                  null = True)
    clientAdress = models.CharField(max_length = 200,
                                    blank = True,
                                    null = True)
    clientCountry = models.CharField(max_length = 50,
                                     default = 'FRANCE')
    class Meta:
        ordering = ['-date', 'code']
    
    #Client facture
class OperationFacture(models.Model):
    ligne = models.ForeignKey('BudgetLigne',
                              on_delete = models.CASCADE,
                              default = 0)
    code = models.CharField(max_length = 10,
                            default = 'PXXXX-XXXX')
    objet = models.CharField(max_length = 150)
    prixHT = models.DecimalField(decimal_places= 2,
                                 max_digits= 8,
                                 default = 00.00)
    nb = models.IntegerField(default = 1)
    facture = models.ForeignKey('Facture',
                                on_delete = models.CASCADE,
                                blank = True,
                                null = True)
    @property
    def prixTotalHT(self):
        return self.prixHT * self.nb

    
#*****************************************************************************************
#Compte pilote
class Vol(models.Model):
    def __str__(self):
        text = self.aeronef.type + ' - ' + str(self.date)
        return text
    pilote = models.ForeignKey('Member',
                               on_delete=models.CASCADE,
                               blank = True,
                               null = True)
    date = models.DateField(blank = True,
                            null = True)
    aeronef = models.ForeignKey('Aeronef',
                                on_delete=models.CASCADE,
                                default = 1)
    textVVent = models.CharField(max_length = 1000,
                             blank = True,
                             default = 'RAS')
    textAltitude = models.CharField(max_length = 1000,
                             blank = True,
                             default = 'RAS')
    textStress = models.CharField(max_length = 1000,
                             blank = True,
                             default = 'RAS')
    textDecollage = models.CharField(max_length = 1000,
                             blank = True,
                             default = 'RAS')
    textVol = models.CharField(max_length = 1000,
                             blank = True,
                             default = 'RAS')
    textNav = models.CharField(max_length = 1000,
                             blank = True,
                             default = 'RAS')
    textRadio = models.CharField(max_length = 1000,
                             blank = True,
                             default = 'RAS')
    textAtterrissage = models.CharField(max_length = 1000,
                             blank = True,
                             default = 'RAS')
    textTdp = models.CharField(max_length = 1000,
                             blank = True,
                             default = 'RAS')
    textBaseULM = models.CharField(max_length = 1000,
                             blank = True,
                             default = 'RAS')
    textCommentaire = models.CharField(max_length = 1000,
                             blank = True,
                             default = 'RAS')
    instructeur = models.CharField(max_length = 50,
                                   default = None,
                                   blank = True,
                                   null = True)
    indemInstructeur = models.ForeignKey(OuiNon,
                                         on_delete=models.CASCADE,
                                         related_name='idemInstructeurOuiNon',
                                         default = 1)
    bapteme = models.ForeignKey(OuiNon,
                                on_delete=models.CASCADE,
                                related_name='baptemeOuiNon',
                                default = 1)
    maintenance = models.ForeignKey(OuiNon,
                                    on_delete=models.CASCADE,
                                    related_name='maintenanceOuiNon',
                                    default = 1)
    horoInit = models.DecimalField(decimal_places = 2,
                                   max_digits = 7,
                                   default = 00.00)
    horoFin = models.DecimalField(decimal_places = 2,
                                  max_digits = 7,
                                  default = 00.00)
    prixVol = models.DecimalField(decimal_places = 2,
                                  max_digits = 7,
                                  default = 00.00)
    tarifInstruction = models.DecimalField(decimal_places = 2,
                                           max_digits = 7,
                                           default = 00.00)
    remise = models.DecimalField(decimal_places = 2,
                                 max_digits = 7,
                                 default = 00.00)
    class Meta:
        ordering = ['-date']
    @property
    def dureeVol(self):
        return int(calcDureeVol(self.horoInit,self.horoFin))
    def prixTotal(self):
        return self.prixVol + self.tarifInstruction - self.remise

#*****************************************************************************************
#Aéronef   
class Aeronef(models.Model):
    def __str__(self):
        text = self.type
        return text
    type = models.CharField(max_length = 20)
    classeULM = models.ForeignKey('ClasseULM',
                                  on_delete=models.CASCADE,
                                  default = 3)
    immatriculation = models.CharField(max_length = 6,
                                       default = 'XXXXX')
    indicatifRadio = models.CharField(max_length = 6,
                                       default = 'F-JXXX')
    limiteAptitudeVol = models.DateField(blank = True,
                            null = True)
    limiteLSA = models.DateField(blank = True,
                            null = True)
    limiteParachute = models.DateField(blank = True,
                            null = True)
    date = models.DateField(blank = True,
                            null = True)
    tarifPilote = models.DecimalField(decimal_places = 2,
                                      max_digits = 5,
                                      default = 00.00)
    tarifElevePilote = models.DecimalField(decimal_places = 2,
                                      max_digits = 5,
                                      default = 00.00)
    
class ClasseULM(models.Model):
    def __str__(self):
        text = 'classe' + self.number + ' - ' + self.name
        return text
    number = models.CharField(max_length = 1)
    name = models.CharField(max_length = 20)

#*****************************************************************************************
class Reservation(models.Model):
    def __str__(self):
        text = str(self.aeronef) + ' - ' + str(self.date) + ' ' + str(self.hInit)
        return text
    pilote = models.ForeignKey('Member',
                               on_delete=models.CASCADE,
                               blank = True,
                               null = True)
    aeronef = models.ForeignKey('Aeronef',
                                on_delete=models.CASCADE,
                                default = 1)
    # instruction = models.ForeignKey(OuiNon,
    #                             on_delete=models.CASCADE,
    #                             related_name='ReservationInstructionOuiNon',
    #                             default = 1)
    typeVol = models.CharField(max_length = 20,
                               null = True)
    # location = models.ForeignKey(OuiNon,
    #                                 on_delete=models.CASCADE,
    #                                 related_name='ReservationLocationOuiNon',
    #                                 default = 1)
    # bapteme = models.ForeignKey(OuiNon,
    #                             on_delete=models.CASCADE,
    #                             related_name='ReservationBaptemeOuiNon',
    #                             default = 1)
    # maintenance = models.ForeignKey(OuiNon,
    #                                 on_delete=models.CASCADE,
    #                                 related_name='ReservationMaintenanceOuiNon',
    #                                 default = 1)
    date = models.DateField(blank = True,
                            null = True)
    hInit = models.CharField(max_length = 5,
                                   default = '00:00')
    hEnd = models.CharField(max_length = 5,
                                   default = '00:00')
    textVol = models.CharField(max_length = 1000,
                             blank = True,
                             default = 'RAS')
    class Meta:
        ordering = ['-date','hInit']

class City(models.Model):
    def __str__(self):
        return self.name
    name  = models.CharField(max_length=20)
    lat = models.DecimalField(decimal_places = 15,
                                      max_digits = 19,
                                      null = True)
    long = models.DecimalField(decimal_places = 2,
                                      max_digits = 19,
                                      null = True)
    class Meta:
        ordering = ['name']