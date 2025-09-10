from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db import connection
from collections import namedtuple
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
    if 'character' in request.GET:
        character_obj = Character.objects.filter(id=request.GET['character']).first()
        if character_obj.user_id != request.user.id:
            return HttpResponseRedirect("census/characters")

    if request.method == 'POST':
        form = EncounterForm(request.POST, request=request)
        if form.is_valid():
            encounter = Encounter(
                character_id= request.POST['character'],
                role_id= request.POST['role'],
                location_id= request.POST['location'],
                outcome_id= request.POST['outcome'],
            )
            if 'host_runes' in request.POST and request.POST['host_runes']:
                encounter.host_runes = int(request.POST['host_runes'])
            if 'coop_type' in request.POST and request.POST['coop_type']:
                encounter.coop_type_id = int(request.POST['coop_type'])

            encounter.save()
            messages.success(request, "Encounter successfully recorded")

            #return HttpResponseRedirect(reverse("census:record"))
            return HttpResponseRedirect(f"/census/record?role={request.POST['role']}&character={request.POST['character']}")

    else:
        context = {
            'form': None,
            'roles': Role.objects.order_by('id'),
            'role_styles': role_styles,
            'selected_role': request.GET.get('role'),
        }
        if 'character' in request.GET:
            context['character_obj'] = character_obj
        if 'role' in request.GET:
            context['form'] = EncounterForm(request.GET, request=request)

    return render(request, "census/record.html", context)

def character_stats(request):
    context = {}
    if 'character' in request.GET:
        character_obj = Character.objects.filter(id=request.GET['character']).first()
        if character_obj.user_id != request.user.id:
            return HttpResponseRedirect("characters")

        if 'character' in request.GET:
            context['character_obj'] = character_obj
            context['locations'] = Location.objects.annotate(num_encounters=models.Count("encounter", filter=models.Q(encounter__character=character_obj))).order_by("-num_encounters")[:10]
            context['coop_types'] = CoopType.objects.annotate(num_encounters=models.Count("encounter", filter=models.Q(encounter__character=character_obj))).order_by("sort_order")[:10]
            context['num_encounters_with_type'] = sum(e.num_encounters for e in context['coop_types'])
    return render(request, "census/character_stats.html", context)


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
        messages.success(request, "New Character Saved")
        return HttpResponseRedirect("/census/characters")

def character_create(request):
    context = {
        'form': CharacterForm()
    }
    return render(request, "census/character_create.html", context)

def stats(request):
    platforms = Platform.objects.annotate(num_encounters=models.Count("character__encounter")).order_by("-num_encounters")
    roles = Role.objects.annotate(num_encounters=models.Count("encounter")).order_by("id")
    locations = Location.objects.annotate(num_encounters=models.Count("encounter")).order_by("-num_encounters")[:10]
    query = '''select rune_level, weapon_level, count(census_encounter.id) as num_encounters
        from census_character
        inner join census_encounter on census_encounter.character_id = census_character.id
        group by rune_level, weapon_level
        order by count(census_encounter.id) desc
        limit 10'''
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        levels = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, "census/stats.html", {"platforms":platforms, "roles":roles, "levels": levels, "locations": locations})

class CharacterListView(ListView):
    model = Character

    def get_queryset(self):
        return Character.objects.filter(user_id=self.request.user.id)

class HistoryListView(ListView):
    model = Encounter

    def get_queryset(self):
        return Encounter.objects.filter(character__user_id=self.request.user.id).order_by("-created_at")[:100]

def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "New Account Created")
            return HttpResponseRedirect("/census/characters")
    else:
        form = UserCreationForm()
    return render(request, "census/sign_up.html", {"form": form})
