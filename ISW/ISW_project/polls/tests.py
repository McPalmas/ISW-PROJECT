from django.test import TestCase
from .models import Prodotto
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


   