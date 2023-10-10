from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    User._meta.get_field('email')._unique = True

    class Meta:
        model = User
        fields = ('username',  'email', 'password1', 'password2', )


class AddressForm(forms.Form):
    country = forms.CharField(max_length=50)
    region = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    street_address = forms.CharField(max_length=100)


class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16)
    owner_name = forms.CharField(max_length=100)
    expiration_month = forms.IntegerField()
    expiration_year = forms.IntegerField()
    cvv = forms.CharField(max_length=4)


class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=254)
    country = CountryField(blank_label='(select country)')
    zip = forms.CharField(max_length=10)
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput())
    payment_option = forms.ChoiceField(widget=forms.RadioSelect())
