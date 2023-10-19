from django.contrib import admin
from .models import *

admin.site.register([Carrello, ElementoCarrello ])

@admin.register(Prodotto)
class ProdottoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descrizione', 'prezzo')
    list_filter = ["descrizione","prezzo"]
    search_fields = ["nome"]

@admin.register(Ordine)
class OrdineAdmin(admin.ModelAdmin):
    list_display = ['user', 'nome', 'cognome', 'email', 'prezzo_complessivo_ordine']
    list_filter = ['user']
    search_fields = ['user', 'nome', 'cognome', 'email']
    ordering = ['-id']
