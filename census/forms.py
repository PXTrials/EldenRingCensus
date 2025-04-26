from django import forms
from .models import *

class EncounterForm(forms.Form):
    character = forms.ModelChoiceField(
        label="Character",
        queryset=Character.objects.all(),
        widget=forms.Select(attrs={'class':'selectpicker'})
    )
    #role = forms.ModelChoiceField(label="Role", queryset=Role.objects.all())
    role = forms.CharField(widget=forms.HiddenInput())
    location = forms.ModelChoiceField(
        label="Location",
        queryset=Location.objects.order_by('sort_order'),
        widget=forms.Select(attrs={'class':'selectpicker','data-live-search':'true'})
    )
    outcome = forms.ModelChoiceField(
        label="Outcome",
        queryset=Outcome.objects.all(),
        widget=forms.Select(attrs={'class':'selectpicker'})
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['outcome'].queryset = Outcome.objects.filter(role_id= args[0]['role']).order_by('sort_order')

class CharacterForm(forms.Form):
    platform = forms.ModelChoiceField(
        label = "Platform",
        queryset=Platform.objects.order_by('id')
    )
    name = forms.CharField()
    rune_level = forms.CharField()
    weapon_level = forms.CharField()
