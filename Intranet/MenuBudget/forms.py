#Imports externes
from django import forms
from django.forms.widgets import RadioSelect,\
                                    DateInput,\
                                    HiddenInput

#Imports internes
from Intranet.models import BudgetSection,\
                            BudgetProjet,\
                            BudgetLigne,\
                            BudgetOperation,\
                            CompteEpargne,\
                            CompteEpargneOperation,\
                            Facture,\
                            OperationFacture,\
                            Aeronef
from crispy_forms.bootstrap import TabHolder

#Budget/Gérer Sections       
class budgetGererSectionForm(forms.ModelForm):
    class Meta:
        model = BudgetSection
        fields = ('code',
                  'name',)
        labels = {'code' : 'Code ',
                  'name' : 'Section ',}
    
#Budget/Gérer Projets    
class budgetGererProjetForm(forms.ModelForm):
    class Meta:
        model = BudgetProjet
        fields = ('section', 
                  'code',
                  'name',)
        labels = {'section' : 'Section ',
                  'code' : 'Code ', 
                  'name' : 'Projet '}
#Budget/Gérer Lignes    
class budgetGererLigneForm(forms.ModelForm):
    class Meta:
        model = BudgetLigne
        fields = ('projet',
                  'code',
                  'name',)
        labels = {'projet' : 'Projet ',
                  'code' : 'Code ',
                  'name' : 'Ligne '}
 
#Budget/Gérer Opérations
    #Choix de la Ligne où créer l'opération
class budgetLigneChoiceForm(forms.Form):
    ligne = forms.ModelChoiceField(queryset = BudgetLigne.objects.all(),
                    required = False,
                    initial = 1,
                    label = 'Ligne ',
                    )

    #Créer l'opération
class budgetGererOperationForm(forms.ModelForm):
    class Meta:
        model = BudgetOperation
        fields = ('budget',
                  'code',
                  'name',
                  'date',
                  'beneficiaire',
                  'aeronef',
                  'charge',
                  'produit')
        labels = {'budget' : 'Budget ',
                  'name' : 'Opération ',
                  'date' : 'date ',
                  'aeronef' : 'Aeronef',
                  'charge' : 'charge (€) ',
                  'produit' : 'produit (€) '}
        widgets = {'date' : DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                   'code' : HiddenInput,
                   'beneficiaire' : HiddenInput}
        
        
#Créer l'opération pour location et instruction
class budgetGererOperationLocInstForm(forms.ModelForm):
    class Meta:
        model = BudgetOperation
        fields = ('budget',
                  'code',
                  'name',
                  'date',
                  'beneficiaire',
                  'aeronef',
                  'charge',
                  'produit')
        labels = {'budget' : 'Budget ',
                  'name' : 'Opération ',
                  'date' : 'date ',
                  'beneficiaire' : 'Pilote ',
                  'aeronef' : 'Aeronef ',
                  'charge' : 'charge (€) ',
                  'produit' : 'produit (€) '}
        widgets = {'date' : DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                   'code' : HiddenInput}
    
#Budget/Budget Année courante par ligne
class budgetLigneListForm(forms.Form):
    ligneList = BudgetLigne.objects.all()
    if ligneList:
        id = 0
        for ligne in ligneList:
            idLigne = ligne.id
            if idLigne > id:
                id = idLigne
        ligneSelect = forms.ModelChoiceField(queryset = BudgetLigne.objects.all(),
                        required = False,
                        label = '',
                        initial = id,
                        widget = RadioSelect())
    else:
        ligneSelect = forms.CharField(default = 'Aucune Ligne dans la base',
                        label = '')

#Budget/Budget Année courante par aeronef
class budgetAeronefListForm(forms.Form):
    aeronefList = Aeronef.objects.all()
    aeronefSelect = forms.ModelChoiceField(queryset = Aeronef.objects.all(),
                        required = False,
                        label = '',
                        initial = 0,
                        widget = RadioSelect())

#Budget/Gérer comptes épargnes    
class gererCompteEpargneForm(forms.ModelForm):
    class Meta:
        model = CompteEpargne
        fields = ('name',)
        labels = {'name' : 'Compte épargne '}
        
#Budget/Compte épargne
class compteEpargneChoiceForm(forms.Form):
    compteEpargne = forms.ModelChoiceField(queryset = CompteEpargne.objects.all(),
                    required = False,
                    initial = 1,
                    label = 'Compte Épargne ',
                    )
    
class compteEpargneOperationForm(forms.ModelForm):
    class Meta:
        model = CompteEpargneOperation
        fields = ('compteEpargne',
                  'code',
                  'name',
                  'date',
                  'charge',
                  'produit')
        labels = {'compteEpargne' : 'Compte Épargne ',
                  'name' : 'Opération ',
                  'date' : 'Date ',
                  'charge' : 'Charge (€) ',
                  'produit' : 'Produit (€) '}
        widgets = {'date' : DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                   'code' : HiddenInput}

#Budget/Bilan comptes épargne
class compteEpargneListForm(forms.Form):
    compteEpargneList = CompteEpargne.objects.all()
    if compteEpargneList:
        id = 0
        for compteEpargne in compteEpargneList:
            idCompteEpargne = compteEpargne.id
            if idCompteEpargne > id:
                id = idCompteEpargne
        compteEpargneSelect = forms.ModelChoiceField(queryset = CompteEpargne.objects.all(),
                        required = False,
                        label = '',
                        initial = id,
                        widget = RadioSelect())
    else:
        compteEpargneSelect = forms.CharField(default = 'Aucun compte Epargne dans la base',
                        label = '')

#Budget/Générateur de facture
class budgetGenFactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ('code',
                  'date',
                  'acquite')
        labels = {'date' : 'Date',
                  'acquite' : 'Acquitée '}
        widgets = {'date' : DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                   'code' : HiddenInput}   

class budgetGenFactureClientForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = (
                  'clientName',
                  'clientVorname',
                  'clientAdress',
                  'clientZip',
                  'clientCity',
                  'clientCountry')
        labels = { 
                  'clientName' : 'Nom ',
                  'clientVorname' : 'Prénom ',
                  'clientAdress' : 'Adresse ',
                  'clientZip' : 'Code postal ',
                  'clientCity' : 'Ville ',
                  'clientCountry' : 'Pays '}

class budgetGenFactureOpForm(forms.ModelForm):
    class Meta:
        model = OperationFacture
        fields = ('ligne',
                  'code',
                  'objet',
                  'prixHT',
                  'nb')
        labels = {'ligne' : 'Ligne budgétaire ',
                  'objet' : 'Objet ',
                  'prixHT' : 'Prix unitaire HT ',
                  'nb' : 'Quantité '}
        widgets = {'code' : HiddenInput}