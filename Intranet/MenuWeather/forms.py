from django.forms import ModelForm, TextInput
from Intranet.models import City

class cityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name',
                  'lat',
                  'long']
        widgets = {
            'name': TextInput(attrs={'class' : 'input', 'placeholder': 'Nom de la ville'}),
            'lat': TextInput(attrs={'class' : 'input', 'placeholder': 'Latitude (décimal)'}),
            'long': TextInput(attrs={'class' : 'input', 'placeholder': 'Longitude (décimal)'}),
        }
        labels = {'name' : 'Nom ',
                  'lat' : 'Latitude ',
                  'long' : 'Longitude'}