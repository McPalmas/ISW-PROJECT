from django.contrib import admin
from .models import *

admin.site.register([Carrello, ElementoCarrello, Prodotto, Ordine])


class ProdottoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descrizione', 'prezzo')
    list_filter = ["descrizione"]
    search_fields = ["nome"]


class OrdineAdmin(admin.ModelAdmin):
    list_display = ['user', 'nome', 'cognome', 'email', 'prezzo_complessivo_ordine']
    list_filter = ['user']
    search_fields = ['user', 'nome', 'cognome', 'email']
    ordering = ['-id']
