from django import forms
from .models import ConstructItem, ApplicationItem

class ConstructItemForm(forms.ModelForm):
    class Meta:
        model = ConstructItem
        fields = ['construct_number','receptor', 'DNA_sequence', 'description', 'comment','user']

class ApplicationItemForm(forms.ModelForm):
    class Meta:
        model = ApplicationItem
        fields = ['construct_number', 'P', 'biomass', 'expression_system',  'application_user', 'comment']