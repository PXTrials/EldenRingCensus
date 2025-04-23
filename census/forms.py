from django import forms
from .models import *

class EncounterForm(forms.Form):
    character = forms.ModelChoiceField(label="Character", queryset=Character.objects.all())
    #role = forms.ModelChoiceField(label="Role", queryset=Role.objects.all())
    role = forms.CharField(widget=forms.HiddenInput())
    location = forms.ModelChoiceField(label="Location", queryset=Location.objects.order_by('sort_order'))
    outcome = forms.ModelChoiceField(label="Outcome", queryset=Outcome.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['outcome'].queryset = Outcome.objects.filter(role_id= args[0]['role']).order_by('sort_order')
