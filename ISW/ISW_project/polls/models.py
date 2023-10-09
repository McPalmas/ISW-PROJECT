from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import uuid


class Prodotto(models.Model):
    nome = models.TextField(default='Nome di default')
    descrizione = models.TextField(default='Descrizione di default')
    prezzo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.nome)


# definizione del carrello
class Carrello(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
