from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Area)
admin.site.register(Location)
admin.site.register(Outcome)
admin.site.register(Character)
admin.site.register(Encounter)
