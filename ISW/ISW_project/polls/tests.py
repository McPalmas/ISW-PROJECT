from django.test import TestCase
from .models import *
from django.contrib.auth.models import User


#Unit test for Prodotto model

class ProdottoModelTest(TestCase):
    def setUp(self):
        Prodotto.objects.create(id=100,nome='Prodotto di test', descrizione='Descrizione di test', prezzo=10.00)

    def test_prodotto_creation(self):
        prodotto = Prodotto.objects.get(id=100)
        self.assertEqual(prodotto.nome, 'Prodotto di test')
        self.assertEqual(prodotto.descrizione, 'Descrizione di test')
        self.assertEqual(prodotto.prezzo, 10.00)

class CarrelloTests(TestCase):

    def test_creazione_carrello(self):
        """
        Verifica che sia possibile creare un nuovo carrello.
        """
        user = User.objects.create(username="test_user")
        carrello = Carrello.objects.create(user=user)
        self.assertNotEqual(carrello.id, None)
        self.assertEqual(carrello.user, user)
        self.assertEqual(carrello.completato, False)

    def test_prezzo_complessivo_carrello(self):
        """
        Verifica che il prezzo complessivo del carrello sia corretto.
        """
        user = User.objects.create(username="test_user")
        carrello = Carrello.objects.create(user=user)
        elemento_carrello_1 = ElementoCarrello.objects.create(
            carrello=carrello, prodotto=Prodotto.objects.create(nome="Prodotto 1", prezzo=10.00), quantita=1
        )
        elemento_carrello_2 = ElementoCarrello.objects.create(
            carrello=carrello, prodotto=Prodotto.objects.create(nome="Prodotto 2", prezzo=20.00), quantita=2
        )
        self.assertEqual(carrello.prezzo_complessivo_carrello, 50.00)

    def test_numero_elementi(self):
        """
        Verifica che il numero di elementi nel carrello sia corretto.
        """
        user = User.objects.create(username="test_user")
        carrello = Carrello.objects.create(user=user)
        elemento_carrello_1 = ElementoCarrello.objects.create(
            carrello=carrello, prodotto=Prodotto.objects.create(nome="Prodotto 1", prezzo=10.00), quantita=1
        )
        elemento_carrello_2 = ElementoCarrello.objects.create(
            carrello=carrello, prodotto=Prodotto.objects.create(nome="Prodotto 2", prezzo=20.00), quantita=2
        )
        self.assertEqual(carrello.numero_elementi, 3)


class ElementoCarrelloTests(TestCase):

    def test_creazione_elemento_carrello(self):
        """
        Verifica che sia possibile creare un nuovo elemento del carrello.
        """
        user = User.objects.create(username="test_user")
        carrello = Carrello.objects.create(user=user)
        prodotto = Prodotto.objects.create(nome="Prodotto 1", prezzo=10.00)
        elemento_carrello = ElementoCarrello.objects.create(
            prodotto=prodotto, carrello=carrello, quantita=1
        )
        self.assertEqual(elemento_carrello.prodotto, prodotto)
        self.assertEqual(elemento_carrello.carrello, carrello)
        self.assertEqual(elemento_carrello.quantita, 1)

    def test_prezzo_elemento_carrello(self):
        """
        Verifica che il prezzo dell'elemento del carrello sia corretto.
        """
        user = User.objects.create(username="test_user")
        carrello = Carrello.objects.create(user=user)
        prodotto = Prodotto.objects.create(nome="Prodotto 1", prezzo=10.00)
        elemento_carrello = ElementoCarrello.objects.create(
            prodotto=prodotto, carrello=carrello, quantita=1
        )
        self.assertEqual(elemento_carrello.prezzo, 10.00)

    def test_quantita_elemento_carrello(self):
        """
        Verifica che la quantità dell'elemento del carrello sia corretta.
        """
        user = User.objects.create(username="test_user")
        carrello = Carrello.objects.create(user=user)
        prodotto = Prodotto.objects.create(nome="Prodotto 1", prezzo=10.00)
        elemento_carrello = ElementoCarrello.objects.create(
            prodotto=prodotto, carrello=carrello, quantita=1
        )
        self.assertEqual(elemento_carrello.quantita, 1)


class OrdineTests(TestCase):
    def setUp(self) :
        self.user = User.objects.create(username="test_user")
        self.carrello = Carrello.objects.create(user=self.user)
        self.prodotto = Prodotto.objects.create(nome="Prodotto 1", prezzo=10.00)
        self.elemento_carrello = ElementoCarrello.objects.create(
            prodotto=self.prodotto, carrello=self.carrello, quantita=1
        )
        self.ordine = Ordine.objects.create(
            user=self.user,
            nome="Nome",
            cognome="Cognome",
            email="Email@mail.it",
            indirizzo="Indirizzo",
            stato="IT",
            citta="Citta",
            regione="Regione",
            provincia="Provincia",
            codice_postale="12345",
            modalita_pagamento="Carta di credito")
        self.ordine.prodotti.add(self.prodotto)

    def test_creazione_ordine(self):
        """
        Verifica che sia possibile creare un nuovo ordine.
        """
        self.assertNotEqual(self.ordine.id, None)
        self.assertEqual(self.ordine.user, self.user)
        self.assertEqual(self.ordine.nome, "Nome")
        self.assertEqual(self.ordine.cognome, "Cognome")
        self.assertEqual(self.ordine.email, "Email@mail.it")
        self.assertEqual(self.ordine.indirizzo, "Indirizzo")
        self.assertEqual(self.ordine.stato, "IT")
        self.assertEqual(self.ordine.citta, "Citta")
        self.assertEqual(self.ordine.regione, "Regione")
        self.assertEqual(self.ordine.provincia, "Provincia")
        self.assertEqual(self.ordine.codice_postale, "12345")
        self.assertEqual(self.ordine.modalita_pagamento, "Carta di credito")

    def test_prezzo_complessivo_ordine(self):
        """
        Verifica che il prezzo complessivo dell'ordine sia corretto.
        """
        self.assertEqual(self.ordine.prezzo_complessivo_ordine, 10.00)


    def test_numero_elementi(self):
        """
        Verifica che il numero di elementi nell'ordine sia corretto.
        """
        self.assertEqual(self.ordine.numero_elementi, 1)

        


    

#Unit test for Register page view
class RegisterViewTest(TestCase):
    def setUp(self):
        Prodotto.objects.create(id=100,nome='Prodotto di test', descrizione='Descrizione di test', prezzo=10.00)

    def test_template_used(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/register.html')

    def test_form_creation(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertContains(response, 'type="text"', 1)
        self.assertContains(response, 'type="password"', 2)
        self.assertContains(response, 'type="email"', 1)
        self.assertContains(response, 'type="submit"')

    def test_form_submit(self):
        response = self.client.post('/register/', {'username': 'testuser', 'password1': 'testpassword', 'password2': 'testpassword'})
        self.assertEqual(response.status_code, 200)

    def test_form_submit_wrong(self):
        response = self.client.post('/register/', {'username': 'testuser', 'password1': 'testpassword', 'password2': 'testpassword2'}) 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'password2')
        self.assertContains(response, 'class="error"')

    def test_form_submit_empty(self):
        response = self.client.post('/register/', {'username': '', 'password1': '', 'password2': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'username')
        self.assertContains(response, 'password1')
        self.assertContains(response, 'password2')
        self.assertContains(response, 'class="error"')

#Unit test for Login page view

class LoginViewTest(TestCase):
    def setUp(self):
        Prodotto.objects.create(id=100,nome='Prodotto di test', descrizione='Descrizione di test', prezzo=10.00)

    def test_page_exist(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_form_creation(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertContains(response, 'type="text"', 1)
        self.assertContains(response, 'type="password"', 1)
        self.assertContains(response, 'type="submit"')
    
    def test_form_submit(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)

    def test_form_submit_wrong(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'testpassword2'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'password')
        self.assertContains(response, 'class="alert alert-danger m-3"')

    def test_form_submit_empty(self):
        response = self.client.post('/login/', {'username': '', 'password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'username')
        self.assertContains(response, 'password')
        self.assertContains(response, '<small')

#Unit test for Logout page view
class LogoutViewTest(TestCase):
    def setUp(self):
        Prodotto.objects.create(id=100,nome='Prodotto di test', descrizione='Descrizione di test', prezzo=10.00)
        User.objects.create_user(username='testuser', password='testpassword')
    
    def test_user_not_logged(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

    def test_user_logged(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

#Unit test for Client Homepage view
class ClientHomepageViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='testuser', password='testpassword')
        Prodotto.objects.create(id=100,nome='Prodotto di test', descrizione='Descrizione di test', prezzo=10.00)
        Prodotto.objects.create(id=101,nome='Prodotto di test2', descrizione='Descrizione di test2', prezzo=20.00)

    def test_user_not_logged(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 302)

    def test_page_exist(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_page_not_exist(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 302)

    def test_template_used(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/Prodotti.html')

    def test_prodotto_list(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Prodotto di test')
        self.assertContains(response, 'Prodotto di test2')


#unit test for Chart list view
class CarrelloViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.prodotto1 = Prodotto.objects.create(id=100,nome='Prodotto di test', descrizione='Descrizione di test', prezzo=10.00)
        self.prodotto2 = Prodotto.objects.create(id=101,nome='Prodotto di test2', descrizione='Descrizione di test2', prezzo=20.00)

    def test_user_not_logged(self):
        response = self.client.get('/carrello/')
        self.assertEqual(response.status_code, 302)

    def test_page_exist(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/carrello/')
        self.assertEqual(response.status_code, 200)
    
    def test_carrello_caricato_correttamente(self):
        self.client.login(username='testuser', password='testpassword')
        carrello = Carrello.objects.create(user=self.user)
        elemento_carrello_1 = ElementoCarrello.objects.create(
            carrello=carrello, prodotto=self.prodotto1, quantita=1
        )
        elemento_carrello_2 = ElementoCarrello.objects.create(
            carrello=carrello, prodotto=self.prodotto2, quantita=2
        )
        response = self.client.get('/carrello/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Prodotto di test')
        self.assertContains(response, 'Prodotto di test2')

    def test_carrello_vuoto(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/carrello/')
        self.assertEqual(response.status_code, 200)

    def test_modifica_quantià_prodotto(self):
        self.client.login(username='testuser', password='testpassword')
        carrello = Carrello.objects.create(user=self.user)
        elemento_carrello_1 = ElementoCarrello.objects.create(
            carrello=carrello, prodotto=self.prodotto1, quantita=1
        )
        response = self.client.get('/increase_quantity/100/')
        self.assertEqual(response.status_code, 302)

        element = ElementoCarrello.objects.get(carrello = carrello, prodotto = self.prodotto1)
        self.assertEqual(element.quantita, 2)

        response = self.client.get('/decrease_quantity/100/')
        self.assertEqual(response.status_code, 302)
        element = ElementoCarrello.objects.get(carrello = carrello, prodotto = self.prodotto1)
        self.assertEqual(element.quantita, 1)

    def test_rimozione_elemento_carrello(self):
        self.client.login(username='testuser', password='testpassword')
        carrello = Carrello.objects.create(user=self.user)
        elemento_carrello_1 = ElementoCarrello.objects.create(
            carrello=carrello, prodotto=self.prodotto1, quantita=1
        )
        response = self.client.get('/remove_product/100/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(carrello.numero_elementi, 0)

    