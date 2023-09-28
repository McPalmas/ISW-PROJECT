from django.shortcuts import render
from .models import Prodotto
from django.http import HttpResponse

def lista_prodotti(request):
    prodotti = Prodotto.objects.all()
    return render(request, 'polls/Prodotti.html', {'prodotti': prodotti})