from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *


def index(request):
    return HttpResponse("Hullo world! At the httprequest")

def record(request):
    if request.method == 'POST':
        form = EncounterForm(request.POST)
        if form.is_valid():
            Encounter.objects.create(
                character_id= request.POST['character'],
                role_id= request.POST['role'],
                location_id= request.POST['location'],
                outcome_id= request.POST['outcome'],
            )
            return HttpResponseRedirect("census:record")
    else:
        context = {
            "form": EncounterForm()
        }
    return render(request, "census/record.html", context)
