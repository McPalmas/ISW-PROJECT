from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import FormView
from .models import *
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import RegisterForm
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


def carrello(request):
    carrello = None
    elementiCarrello = []

    if request.user.is_authenticated:
        carrello, creato = Carrello.objects.get_or_create(user=request.user, completato=False)
        elementiCarrello = carrello.elementiCarrello.all()
    else:
        return redirect('login')

    if carrello.numero_elementi == 0:
        context = {"carrello": carrello, "elementiCarrello": elementiCarrello}
        return render(request, "polls/Carrello.html", context)
    context = {"carrello": carrello, "elementiCarrello": elementiCarrello}
    return render(request, "polls/Carrello.html", context)


def add_to_cart(request, id):
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


def ordine(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        cognome = request.POST["cognome"]
        email = request.POST["email"]
        indirizzo = request.POST["indirizzo"]
        citta = request.POST["citta"]
        regione = request.POST["regione"]
        provincia = request.POST["provincia"]
        stato = request.POST["stato"]
        codice_postale = request.POST["codice_postale"]
        nome_carta = request.POST["nome_carta"]
        numero_carta = request.POST["numero_carta"]
        scadenza = request.POST["scadenza"]
        cvv = request.POST["cvv"]
        pagamento = Pagamento(user=request.user, nome_carta=nome_carta, numero_carta=numero_carta, scadenza=scadenza, cvv=cvv)
        pagamento.save()
        carrello = Carrello.objects.get(user=request.user, completato=False)
        for elemento_carrello in carrello.elementiCarrello.all():
            elemento_ordine = ElementoOrdine(nome=elemento_carrello.prodotto.nome,
                                               descrizione=elemento_carrello.prodotto.descrizione,
                                               prezzo=elemento_carrello.prodotto.prezzo, categoria=elemento_carrello.prodotto.categoria)
            elemento_ordine.save()

        ordine = Ordine(user=request.user, nome=nome, cognome=cognome, email=email, indirizzo=indirizzo, stato=stato,
                        citta=citta, regione=regione, provincia=provincia, codice_postale=codice_postale,
                        pagamento=pagamento, elemento_ordine=elemento_ordine)
        ordine.save()
        Carrello.objects.all().delete()
        return render(request, "polls/Carrello.html")
    else:
        carrello, creato = Carrello.objects.get_or_create(user=request.user, completato=False)
        numero_elementi = carrello.elementiCarrello.all().count() * carrello.numero_elementi
        prezzo_totale = carrello.prezzo_complessivo_carrello
        return render(request, "polls/Checkout.html", {'numero_elementi': numero_elementi, 'prezzo_totale': prezzo_totale})



