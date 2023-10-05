from django.contrib.auth import login
from django.shortcuts import render
from django.views.generic import FormView
from .models import Prodotto
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.template import loader
from django.views.generic.list import ListView


class UserLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('home')


class HomeView(ListView):
     model = Prodotto
     template_name = 'polls/Prodotti.html'
     context_object_name = 'prodotti'