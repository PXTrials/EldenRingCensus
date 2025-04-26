from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from .models import *
from .forms import *


def index(request):
    return HttpResponse("Hullo world! At the httprequest")

def record(request):
    role_styles = {
        'gold':'warning',
        'red':'danger',
        'blue':'primary'
    }
    if request.method == 'POST':
        form = EncounterForm(request.POST)
        if form.is_valid():
            Encounter.objects.create(
                character_id= request.POST['character'],
                role_id= request.POST['role'],
                location_id= request.POST['location'],
                outcome_id= request.POST['outcome'],
            )
            #return HttpResponseRedirect(reverse("census:record"))
            return HttpResponseRedirect(f"/census/record?role={request.POST['role']}&character={request.POST['character']}")
    else:
        context = {
            'form': None,
            'roles': Role.objects.order_by('id'),
            'role_styles': role_styles,
            'selected_role': request.GET.get('role')
        }
        if 'role' in request.GET:
            context['form'] = EncounterForm(request.GET)

    return render(request, "census/record.html", context)

def character_save(request):
    form = CharacterForm(request.POST)
    if form.is_valid():
        Character.objects.create(
            player_id=1,
            platform_id = request.POST['platform'],
            name = request.POST['name'],
            rune_level = request.POST['rune_level'],
            weapon_level = request.POST['weapon_level'],
        )
        return HttpResponseRedirect("/census/characters")

def character_create(request):
    context = {
        'form': CharacterForm()
    }
    return render(request, "census/character_create.html", context)

class CharacterListView(ListView):
    model = Character

