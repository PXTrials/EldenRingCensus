from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import *
from .forms import *


def index(request):
    return render(request, "census/index.html", {})

def record(request):
    role_styles = {
        'gold':'warning',
        'red':'danger',
        'blue':'primary'
    }
    if request.method == 'POST':
        form = EncounterForm(request.POST, request=request)
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
            context['form'] = EncounterForm(request.GET, request=request)

    return render(request, "census/record.html", context)

def character_save(request):
    form = CharacterForm(request.POST)
    if form.is_valid():
        Character.objects.create(
            user_id = request.user.id,
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

    def get_queryset(self):
        return Character.objects.filter(user_id=self.request.user.id)

def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("/census/record")
    else:
        form = UserCreationForm()
    return render(request, "census/sign_up.html", {"form": form})
