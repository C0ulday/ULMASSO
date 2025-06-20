#Imports externes
from django import forms
from django.forms.widgets import DateInput,\
                                RadioSelect

#imports internes
from Intranet.models import Aeronef

#Aeronefs/paramètres
class gererAeronefForm(forms.ModelForm):
    class Meta:
        model = Aeronef
        fields = ('type',
                  'classeULM',
                  'immatriculation',
                  'indicatifRadio',
                  'limiteAptitudeVol',
                  'limiteLSA',
                  'limiteParachute',
                  'tarifPilote',
                  'tarifElevePilote',
                  )
        labels = {'type'        : 'Type ULM ' ,
                  'classeULM'   : 'classe ULM ',
                  'immatriculation' : 'Immatriculation ',
                  'indicatifRadio' : 'Indicatif radio ',
                  'limiteAptitudeVol' : "Limite Aptitude Vol ",
                  'limiteLSA' : "Limite LSA ",
                  'limiteParachute' : "Limite Parachute ",
                  'tarifPilote' : 'Prix Location (€/min) ',
                  'tarifElevePilote' : 'Prix instruction (€/min) ',
                  'prout' : 'prout '
                  }
        widgets = {'limiteAptitudeVol' : DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                   'limiteLSA' : DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                   'limiteParachute' : DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                   }

#Aeronefs/Statistiques
class aeronefListForm(forms.Form):
    aeronefList = Aeronef.objects.all()
    aeronefSelect = forms.ModelChoiceField(queryset = Aeronef.objects.all(),
                        required = False,
                        label = '',
                        initial = 0,
                        widget = RadioSelect())
    
    