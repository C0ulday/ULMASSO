#Imports externes
from django import forms
from django.forms.widgets import PasswordInput

#Logged member
    #Login
class loginForm(forms.Form):
    identifiant = forms.EmailField(max_length = 50,
                                  label = 'Courriel ')
    password = forms.CharField(max_length=20,
                               widget = PasswordInput,
                               label = 'Mot de passe ')