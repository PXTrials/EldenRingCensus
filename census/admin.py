from django.contrib import admin

# Register your models here.
from .models import *

class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort_order')
admin.site.register(Area, AreaAdmin)

class CoopTypeAdmin(admin.ModelAdmin):
    list_display = ('description', 'sort_order')
admin.site.register(CoopType, CoopTypeAdmin)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'sort_order')
admin.site.register(Location, LocationAdmin)

class OutcomeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'role')
admin.site.register(Outcome, OutcomeAdmin)

admin.site.register(Character)
admin.site.register(Encounter)
