from django import forms
from .models import *

class EncounterForm(forms.Form):

    character = forms.ModelChoiceField(
        label="Character",
        queryset=Character.objects.all(),
        widget=forms.HiddenInput()
    )
    #role = forms.ModelChoiceField(label="Role", queryset=Role.objects.all())
    role = forms.CharField(widget=forms.HiddenInput())
    location = forms.ModelChoiceField(
        label="Location",
        queryset=Location.objects.order_by('sort_order'),
        widget=forms.Select(attrs={'class':'selectpicker form-control','data-live-search':'true'})
    )
    coop_type = forms.ModelChoiceField(
        label="CoopType",
        queryset=CoopType.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class':'selectpicker form-control'})
        )
    outcome = forms.ModelChoiceField(
        label="Outcome",
        queryset=Outcome.objects.all(),
        widget=forms.Select(attrs={'class':'selectpicker form-control'})
        )
    host_runes = forms.IntegerField(required=False, min_value=1, max_value=355173)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['character'].queryset = Character.objects.filter(user_id=self.request.user.id)
        self.fields['outcome'].queryset = Outcome.objects.filter(role_id= args[0]['role']).order_by('sort_order')

class CharacterForm(forms.Form):
    platform = forms.ModelChoiceField(
        label = "Platform",
        queryset=Platform.objects.order_by('id')
    )
    name = forms.CharField()
    rune_level = forms.IntegerField(min_value=1, max_value=713)
    weapon_level = forms.IntegerField(min_value=0, max_value=25)
