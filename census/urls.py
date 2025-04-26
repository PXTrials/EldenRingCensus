from django.urls import path
from census.views import CharacterListView
from . import views

app_name = "census"
urlpatterns = [
    path("", views.index, name="index"),
    path('record', views.record, name="record"),
    path('characters/', CharacterListView.as_view()),
    path('character_create', views.character_create, name="character_create"),
    path('character_save', views.character_save, name="character_save"),
]
