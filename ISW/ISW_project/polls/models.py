from django.db import models

class Prodotto(models.Model):
    nome = models.TextField(default='Nome di default')
    descrizione = models.TextField(default='Descrizione di default')
    prezzo = models.DecimalField(max_digits=10, decimal_places=2)


