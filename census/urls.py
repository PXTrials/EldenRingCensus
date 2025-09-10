from django.urls import include, path
from census.views import *
from . import views

app_name = "census"
urlpatterns = [
    path("", views.index, name="index"),
    path('record', views.record, name="record"),
    path('character_stats', views.character_stats, name="character_stats"),
    path('stats', views.stats, name="stats"),
    path('characters/', CharacterListView.as_view()),
    path('history/', HistoryListView.as_view()),
    path('character_create', views.character_create, name="character_create"),
    path('character_save', views.character_save, name="character_save"),
    path('sign_up', views.sign_up, name="sign_up"),
    path('accounts/', include('django.contrib.auth.urls')),
]
