from django.db import models
from django.contrib.auth.models import User
import uuid

from django_countries.fields import CountryField


class Prodotto(models.Model):
    nome = models.TextField(max_length=250)
    descrizione = models.TextField(max_length=400)
    prezzo = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.TextField(max_length=250)

    def __str__(self):
        return str(self.nome)


# definizione del carrello
class Carrello(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    completato = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def prezzo_complessivo_carrello(self):
        elementi_carrello = self.elementiCarrello.all()
        return sum(elemento.prezzo for elemento in elementi_carrello)

    @property
    def numero_elementi(self):
        elementi_carrello = self.elementiCarrello.all()
        return sum(elemento.quantita for elemento in elementi_carrello)


# definizione di un generico elemento del carrello
class ElementoCarrello(models.Model):
    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE, related_name="elementi")
    carrello = models.ForeignKey(Carrello, on_delete=models.CASCADE, related_name="elementiCarrello")
    quantita = models.IntegerField(default=0)

    def __str__(self):
        return str(self.prodotto.nome)

    @property
    def prezzo(self):
        return self.prodotto.prezzo * self.quantita


class Ordine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.TextField(max_length=150, null=False)
    cognome = models.TextField(max_length=150, null=False)
    email = models.EmailField(max_length=254, null=False)
    indirizzo = models.TextField(max_length=254, null=False)
    stato = CountryField(blank=True, blank_label='(Seleziona il paese)', null=False)
    citta = models.TextField(max_length=150, null=False)
    regione = models.TextField(max_length=150, null=False)
    provincia = models.TextField(max_length=150, null=False)
    codice_postale = models.TextField(max_length=10, null=False)
    modalita_pagamento = models.TextField(max_length=150, null=False)
    prodotti = models.ManyToManyField(Prodotto)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elementiOrdine = None

    def __str__(self):
        return str(self.id)

    @property
    def prezzo_complessivo_ordine(self):
        elementi_ordine = self.elementiOrdine.all()
        return sum(elemento.prezzo for elemento in elementi_ordine)

    @property
    def numero_elementi(self):
        elementi_ordine = self.elementiOrdine.all()
        return sum(elemento.quantita for elemento in elementi_ordine)
