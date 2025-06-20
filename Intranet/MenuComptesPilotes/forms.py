#Imports externes
from django import forms
from django.forms.widgets import Textarea,\
                                DateInput

#Imports internes
from Intranet.models import Member,\
                            Aeronef,\
                            OuiNon
                            
#Comptes pilotes/Gérer mes vols
class monVolForm(forms.Form):
    aeronef = forms.ModelChoiceField(queryset = Aeronef.objects.all(),
                                                initial = 0,
                                              label = 'Aéronef ')   
    date = forms.CharField(widget = DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                                   label = "Date du vol ")    
    textVVent = forms.CharField(max_length = 1000,
                                  label = "Vent ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textAltitude = forms.CharField(max_length = 1000,
                                  label = "Altitude ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textStress = forms.CharField(max_length = 1000,
                                  label = "Stress ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textDecollage = forms.CharField(max_length = 1000,
                                  label = "Décollage ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textVol = forms.CharField(max_length = 1000,
                                  label = "Vol ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textNav = forms.CharField(max_length = 1000,
                                  label = "Navigation ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textRadio = forms.CharField(max_length = 1000,
                                  label = "Radio ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textAtterrissage = forms.CharField(max_length = 1000,
                                  label = "Atterrissage ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textTdp = forms.CharField(max_length = 1000,
                                  label = "Tour de piste ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textBaseULM = forms.CharField(max_length = 1000,
                                  label = "Aérodromes et bases visités ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textCommentaire = forms.CharField(max_length = 1000,
                                  label = "Commentaires ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    instructeur = forms.ModelChoiceField(queryset = Member.objects.filter(brevetInstructeur = 2),
                                             required = False,
                                             label = 'Instructeur ')    
    indemInstructeur = forms.ModelChoiceField(queryset = OuiNon.objects.all(),
                                                      initial = 1,
                                                      label = "Indemnisation directe instructeur ")
    bapteme = forms.ModelChoiceField(queryset = OuiNon.objects.all(),
                                                      initial = 1,
                                                      label = "Vol découverte ")
    maintenance = forms.ModelChoiceField(queryset = OuiNon.objects.all(),
                                                      initial = 1,
                                                      label = "Maintenance ")
    horoInit = forms.DecimalField(max_digits = 6,
                                          decimal_places= 2,
                                          min_value = 00.00,
                                          label = "Horomètre début vol ")
    horoFin = forms.DecimalField(max_digits = 6,
                                         decimal_places= 2,
                                         min_value = 00.00,
                                         label = "Horomètre fin vol ")
    
class volForm(forms.Form):
    date = forms.CharField(widget = DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                               label = "Date du vol ")
    aeronef = forms.ModelChoiceField(queryset = Aeronef.objects.all(),
                                                initial = 0,
                                                label = 'Aéronef ') 
    pilote = forms.ModelChoiceField(queryset = Member.objects.all(), 
                                    initial = 0,
                                   label = 'Pilote ')
    textVVent = forms.CharField(max_length = 1000,
                                  label = "Vent ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textAltitude = forms.CharField(max_length = 1000,
                                  label = "Altitude ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textStress = forms.CharField(max_length = 1000,
                                  label = "Stress ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textDecollage = forms.CharField(max_length = 1000,
                                  label = "Décollage ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textVol = forms.CharField(max_length = 1000,
                                  label = "Vol ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textNav = forms.CharField(max_length = 1000,
                                  label = "Navigation ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textRadio = forms.CharField(max_length = 1000,
                                  label = "Radio ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textAtterrissage = forms.CharField(max_length = 1000,
                                  label = "Atterrissage ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textTdp = forms.CharField(max_length = 1000,
                                  label = "Tour de piste ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textBaseULM = forms.CharField(max_length = 1000,
                                  label = "Aérodromes et bases visités ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    textCommentaire = forms.CharField(max_length = 1000,
                                  label = "Commentaires ",
                                  initial = 'RAS',
                                  widget = Textarea(attrs={'cols':'35','rows':'2'}))
    instructeur = forms.ModelChoiceField(queryset = Member.objects.filter(brevetInstructeur = 2),
                                             required = False,
                                             label = 'Instructeur ')    
    indemInstructeur = forms.ModelChoiceField(queryset = OuiNon.objects.all(),
                                                  initial = 1,
                                                  label = "Indemnisation directe instructeur ")
    bapteme = forms.ModelChoiceField(queryset = OuiNon.objects.all(),
                                                  initial = 1,
                                                  label = "Vol découverte ")
    maintenance = forms.ModelChoiceField(queryset = OuiNon.objects.all(),
                                                  initial = 1,
                                                  label = "Maintenance ")
    remise = forms.DecimalField(max_digits = 6,
                                      decimal_places= 2,
                                      min_value = 00.00,
                                      initial = 00.00,
                                 label = 'remise (€)')
    horoInit = forms.DecimalField(max_digits = 6,
                                      decimal_places= 2,
                                      min_value = 00.00,
                                      label = "Horomètre début vol ")
    horoFin = forms.DecimalField(max_digits = 6,
                                     decimal_places= 2,
                                     min_value = 00.00,
                                     label = "Horomètre fin vol ")
    
class comptePiloteChoiceForm(forms.Form):
    pilote = forms.ModelChoiceField(queryset = Member.objects.all(),
                        initial = 0,
                        label = '')

class carnetVolChoiceForm(forms.Form):
    pilote = forms.ModelChoiceField(queryset = Member.objects.all(),
                        initial = 0,
                        label = '')