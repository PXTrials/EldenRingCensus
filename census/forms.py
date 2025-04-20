from django import forms
from .models import *

class EncounterForm(forms.Form):
    character = forms.ModelChoiceField(label="Character", queryset=Character.objects.all())
    role = forms.ModelChoiceField(label="Role", queryset=Role.objects.all())
    location = forms.ModelChoiceField(label="Location", queryset=Location.objects.all())
    outcome = forms.ModelChoiceField(label="Outcome", queryset=Outcome.objects.all())
