from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Ordine


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    User._meta.get_field('email')._unique = True

    class Meta:
        model = User
        fields = ('username',  'email', 'password1', 'password2', )


class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16)
    owner_name = forms.CharField(max_length=100)
    expiration_month = forms.IntegerField()
    expiration_year = forms.IntegerField()
    cvv = forms.CharField(max_length=3)


class CheckoutForm(forms.Form):
    nome = forms.CharField(widget=forms.TextInput())
    cognome = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.TextInput())
    indirizzo = forms.CharField(widget=forms.TextInput())
    stato = CountryField(blank_label='(Seleziona il paese)').formfield(widget=CountrySelectWidget())
    regione = forms.CharField(widget=forms.TextInput())
    provincia = forms.CharField(widget=forms.TextInput())
    citta = forms.CharField(widget=forms.TextInput())
    codice_postale = forms.CharField(widget=forms.TextInput(), max_length=5)
    carta_di_credito = PaymentForm()


class OrdineForm(forms.ModelForm):
    class Meta:
        model = Ordine
        fields = ['nome', 'cognome', 'email', 'indirizzo', 'stato', 'citta', 'regione', 'provincia', 'codice_postale', 'modalita_pagamento']
        exclude = ['prezzo_totale', 'utente']
        widgets = {
            'nome': forms.TextInput(attrs={'id': 'nome'}),
            'cognome': forms.TextInput(attrs={'id': 'cognome'}),
            'email': forms.TextInput(attrs={'id': 'email'}),
            'indirizzo': forms.TextInput(attrs={'id': 'indirizzo'}),
            'stato': CountrySelectWidget(attrs={'id': 'stato'}),
            'citta': forms.TextInput(attrs={'id': 'citta'}),
            'regione': forms.TextInput(attrs={'id': 'regione'}),
            'provincia': forms.TextInput(attrs={'id': 'provincia'}),
            'codice_postale' : forms.TextInput(attrs={'id': 'codice_postale'}),
            'modalita_pagamento': forms.TextInput(attrs={'id': 'modalita_pagamento'}),
        }
        labels = {
            'stato': 'Selezione il paese'
        }
