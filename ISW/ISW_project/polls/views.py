from django.contrib.auth import login
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from .models import *
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import RegisterForm, CheckoutForm, OrdineForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='login/')
def lista_prodotti(request):
    # recupero le categorie definite
    categorie = Prodotto.objects.values_list('categoria', flat=True).distinct()

    prodotti = Prodotto.objects.all()

    # recupero filtro e query di ordinamento
    order_by = request.GET.get('order_by')
    filtro_categoria = request.GET.get('filtro_categoria')

    if order_by in ['prezzo', '-prezzo', 'nome', '-nome']:
        prodotti = prodotti.order_by(order_by)

    if filtro_categoria and filtro_categoria != 'Tutte le categorie':
        prodotti = prodotti.filter(categoria=filtro_categoria)

    # recupero valore del form per la ricerca
    search_term = request.GET.get('search')
    if search_term:
        prodotti = prodotti.filter(nome__icontains=search_term)

    return render(request, 'polls/Prodotti.html', {'prodotti': prodotti, 'categorie': categorie})


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


class CheckoutView(View):
    context = {}

    def get(self, request):
        form = OrdineForm()
        carr = Carrello.objects.get(user=request.user, completato=False)

        self.context['prezzo_totale'] = carr.prezzo_complessivo_carrello
        self.context['numero_elementi'] = carr.numero_elementi
        self.context['form'] = form
        return render(self.request, 'polls/Checkout.html', self.context)

    def post(self, request):
        form = OrdineForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

        self.context['form'] = form
        self.context['detail'] = Ordine.objects.all()
        return render(self.request, 'polls/Checkout.html', self.context)


def carrello(request):
    carrello = None
    elementiCarrello = []

    if request.user.is_authenticated:
        carrello, creato = Carrello.objects.get_or_create(user=request.user, completato=False)
        elementiCarrello = carrello.elementiCarrello.all()

    if carrello.numero_elementi == 0:
        context = {"carrello": carrello, "elementiCarrello": elementiCarrello}
        return render(request, "polls/Carrello.html", context)
    context = {"carrello": carrello, "elementiCarrello": elementiCarrello}
    return render(request, "polls/Carrello.html", context)


def aggiungi_al_carrello(request, id):
    product = Prodotto.objects.get(id=id)
    carrello = []

    if request.user.is_authenticated:
        carrello, creato = Carrello.objects.get_or_create(user=request.user, completato=False)
        elemento, creato = ElementoCarrello.objects.get_or_create(carrello=carrello, prodotto=product)
        elemento.quantita += 1
        elemento.save()

    num_elementi_carrello = carrello.numero_elementi

    return redirect('home')

def remove_product(request, id):
    product = Prodotto.objects.get(id=id)
    carrello = []

    if request.user.is_authenticated:
        carrello, creato = Carrello.objects.get_or_create(user=request.user, completato=False)
        elemento, creato = ElementoCarrello.objects.get_or_create(carrello=carrello, prodotto=product)
        elemento.delete()

    num_elementi_carrello = carrello.numero_elementi

    return redirect('carrello')

def decrease_quantity(request, id):
    product = Prodotto.objects.get(id=id)
    carrello = []

    if request.user.is_authenticated:
        carrello, creato = Carrello.objects.get_or_create(user=request.user, completato=False)
        elemento, creato = ElementoCarrello.objects.get_or_create(carrello=carrello, prodotto=product)
        if elemento.quantita > 0:
            elemento.quantita -= 1
            elemento.save()
        else:
            elemento.delete()

    return redirect('carrello')


def increase_quantity(request, id):
    product = Prodotto.objects.get(id=id)
    carrello = []

    if request.user.is_authenticated:
        carrello, creato = Carrello.objects.get_or_create(user=request.user, completato=False)
        elemento, creato = ElementoCarrello.objects.get_or_create(carrello=carrello, prodotto=product)
        elemento.quantita += 1
        elemento.save()

    return redirect('carrello')

