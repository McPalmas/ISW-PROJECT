from django.contrib import admin
from .models import *


@admin.register(Prodotto)
class ProdottoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descrizione', 'prezzo')
    list_filter = ["descrizione","prezzo"]
    search_fields = ["nome"]


@admin.register(Ordine)
class OrdineAdmin(admin.ModelAdmin):
    list_display = ['user', 'nome', 'cognome', 'email', 'prezzo_complessivo_ordine']
    list_filter = ['user',]
    search_fields = ['user', 'nome', 'cognome', 'email']
    ordering = ['-id']


@admin.register(ElementoOrdine)
class ElementoOrdineAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descrizione', 'prezzo', 'categoria', 'ordine']
    list_filter = ['nome','prezzo','categoria']
    search_fields = ['nome', 'categoria']