from django.urls import path

from . import  views

urlpatterns = [
    path("", views.lista_prodotti, name="lista_prodotti"),
]