#Imports externes
from django import forms
from django.forms.widgets import RadioSelect,\
                                DateInput

#Imports internes
from Intranet.models import Member

#Modifier mot de passe
class loggedMemberPasswordModifyForm(forms.ModelForm):
    class Meta:
        model = Member
        fields =('password',
            )
        labels = {'password' : 'Mot de passe ',
            }

#Gérer membres
class memberForm(forms.ModelForm):
    class Meta :
        model = Member
        fields = ('name',
                  'vorname',
                  'statut',
                  'genre',
                  'birthday',
                  'phone',
                  'email',
                  'zip',
                  'city',
                  'adress',
                  'licenceFFPLUM',
                  'licenceAUV',
                  'brevetInstructeur',
                  'datePiloteC2',
                  'datePiloteC3',
                  'datePiloteC4',
                  'dateEmportC2',
                  'dateEmportC3',
                  'dateEmportC4',
                  'dateBaptemeC2',
                  'dateBaptemeC3',
                  'dateBaptemeC4',
                  'reportComptePilote2024')
        labels = {'name' : 'Nom ', 
                  'vorname' : 'Prénom ',
                  'statut' : 'Fonction ',
                  'genre' : 'Genre ',
                  'birthday' : 'Date de naissance ',
                  'phone' : 'Portable ',
                  'email' : 'Courriel ',
                  'zip' : 'Code postal ',
                  'city' : 'Ville ',
                  'adress' : 'Adresse ',
                  'licenceFFPLUM' : 'Licence FFPLUM ',
                  'licenceAUV': 'Licence au sein d\'AUV ',
                  'brevetInstructeur' : 'Instructeur ',
                  'datePiloteC2' : 'Brevet pilote Classe2 ',
                  'datePiloteC3': 'Brevet pilote Classe3 ',
                  'datePiloteC4': 'Brevet pilote Classe4 ',
                  'dateEmportC2': 'Brevet emport Classe2 ',
                  'dateEmportC3': 'Brevet emport Classe3 ',
                  'dateEmportC4': 'Brevet emport Classe4 ',
                  'dateBaptemeC2':'Vol découverte Classe2 ',
                  'dateBaptemeC3': 'Vol découverte Classe3 ',
                  'dateBaptemeC4': 'Vol découverte Classe4 ',
                  'reportComptePilote2024' : 'Compte pilote - report 2024 (€)'}
        widgets = {'birthday' : DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                   'datePiloteC2' : DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                   'datePiloteC3' : DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                   'datePiloteC4' : DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                   'dateEmportC2' : DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                   'dateEmportC3' : DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                   'dateEmportC4' : DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                   'dateBaptemeC2' : DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                   'dateBaptemeC3' : DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                   'dateBaptemeC4' : DateInput(format="%Y-%m-%d", attrs={"type": "date"})}

#Voir membres
class memberListForm(forms.Form):
    memberSelect = forms.ModelChoiceField(queryset = Member.objects.all(),
                    initial = 0,
                    label = '')