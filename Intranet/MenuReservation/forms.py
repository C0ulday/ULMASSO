#Imports externes
from django import forms
from django.forms.widgets import Textarea,\
                                DateInput

from Intranet.models import OuiNon,\
                            Reservation
from Intranet.MenuReservation import config

class reservationForm(forms.Form):
    volChoices = (("Location", "Location"),
                  ("Instruction", "Instruction"),
                  ("Vol découverte", "Vol découverte"),
                  ("Maintenance", "Maintenance"))
    date = forms.CharField(widget = DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                                   label = "Date du vol ")
    hInit = forms.CharField(max_length = 5,
                            initial = '00:00',
                            label = "Heure début vol ")
    hEnd = forms.CharField(max_length = 5,
                           initial = '00:00',
                           label = "Heure fin vol ")
    textVol = forms.CharField(max_length = 1000,
                              initial = 'RAS',
                              label = "Commentaires ",
                              widget = Textarea(attrs={'cols':'35','rows':'2'}))
    typeVol = forms.ChoiceField(choices = volChoices,
                                initial = 1,
                                label = "typeVol")

class reservationListForm(forms.Form):
    reservation = forms.ModelChoiceField(queryset = Reservation.objects.all(),
                                         initial = 0,
                                         label = '')
