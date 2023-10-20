from django.db import models
from django.contrib.auth.models import User
import uuid

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


class Pagamento(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome_carta = models.TextField(null=False)
    numero_carta = models.IntegerField(null=False)
    scadenza = models.DateField(null=False)
    cvv = models.IntegerField(null=False)


class ElementoOrdine(models.Model):
    nome = models.TextField(max_length=250)
    descrizione = models.TextField(max_length=400)
    prezzo = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.TextField(max_length=250)

    def __str__(self):
        return str(self.nome)


class Ordine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.TextField(max_length=150, null=False)
    cognome = models.TextField(max_length=150, null=False)
    email = models.EmailField(max_length=254, null=False)
    indirizzo = models.TextField(max_length=254, null=False)
    stato = models.TextField(max_length=254, null=False)
    citta = models.TextField(max_length=150, null=False)
    regione = models.TextField(max_length=150, null=False)
    provincia = models.TextField(max_length=150, null=False)
    codice_postale = models.TextField(max_length=10, null=False)
    pagamento = models.OneToOneField(Pagamento, on_delete=models.CASCADE, null=False, default=1)
    elemento_ordine = models.OneToOneField(ElementoOrdine, null=False, on_delete=models.CASCADE, default=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elementiOrdine = ElementoOrdine.objects.all()

    def __str__(self):
        return str(self.id)

    @property
    def prezzo_complessivo_ordine(self):
        return sum(oggetto.prezzo for oggetto in self.elementiOrdine)

    @property
    def numero_elementi(self):
        return sum(elemento.quantita for elemento in self.elementiOrdine.count())
