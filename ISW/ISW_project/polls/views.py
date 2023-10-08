from django.contrib.auth import login
from django.shortcuts import render
from django.views.generic import FormView
from .models import Prodotto
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import RegisterForm
from django.template import loader
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required

@login_required(login_url='login/')
def lista_prodotti(request):
    #recupero filtro e query di ordinamento
    #print("La vista lista_prodotti è stata chiamata")
    order_by = request.GET.get('order_by')
    if order_by in ['prezzo','-prezzo','nome','-nome']:
        prodotti = Prodotto.objects.order_by(order_by)
    else:
        prodotti = Prodotto.objects.all()

    #recupero valore del form per la ricerca
    search_term = request.GET.get('search')
    if search_term:
        prodotti = prodotti.filter(nome__icontains=search_term)

    return render(request, 'polls/Prodotti.html', {'prodotti': prodotti})

class UserLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('home')


class RegisterView(FormView):
    template_name = 'polls/register.html'
    form_class = RegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)

        messages.success(self.request, 'Account created successfully!')
        return super(RegisterView, self).form_valid(form)

