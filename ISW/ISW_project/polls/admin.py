from django.contrib import admin
from .models import Prodotto

@admin.register(Prodotto)
class ProdottoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descrizione', 'prezzo')
    list_filter = ["descrizione"]
    search_fields = ["nome"]
