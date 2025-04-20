from django.urls import path

from . import views

app_name = "census"
urlpatterns = [
    path("", views.index, name="index"),
    path('record', views.record, name="record")
]
