

from selenium import webdriver

from selenium.webdriver.common.by import By

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from .models import Prodotto, Ordine
import time
driver = webdriver.Chrome()

class AcceptanceTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(2)
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.prodotto1 = Prodotto.objects.create(nome='Prodotto 1', descrizione='Descrizione prodotto 1', prezzo=10.0)
        self.prodotto2 = Prodotto.objects.create(nome='Prodotto 2', descrizione='Descrizione prodotto 2', prezzo=20.0)

    def test_login(self):
        self.browser.get(self.live_server_url + '/login/')
        username = self.browser.find_element(By.NAME, 'username')
        password = self.browser.find_element(By.NAME, 'password')
        username.send_keys('testuser')
        password.send_keys('12345')
        time.sleep(2)
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/home/')
        time.sleep(2)

    def test_logout(self):
        self.browser.get(self.live_server_url + '/login/')
        username = self.browser.find_element(By.NAME, 'username')
        password = self.browser.find_element(By.NAME, 'password')
        username.send_keys('testuser')
        password.send_keys('12345')
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/home/')
        time.sleep(2)
        self.browser.find_element(By.CSS_SELECTOR, 'li a[href*="logout"]').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/accounts/login/')
        time.sleep(2)

    def test_visualizza_prodotti(self):
        self.browser.get(self.live_server_url + '/login/')
        username = self.browser.find_element(By.NAME, 'username')
        password = self.browser.find_element(By.NAME, 'password')
        username.send_keys('testuser')
        password.send_keys('12345')
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        product_section = self.browser.find_element(By.CLASS_NAME, 'listaProdotti')
        products = product_section.find_elements(By.CLASS_NAME, 'schedaProdotto')
        self.assertTrue(len(products) > 0)
        time.sleep(2)

    def test_aggiungi_carrello(self):
        self.browser.get(self.live_server_url + '/login/')
        username = self.browser.find_element(By.NAME, 'username')
        password = self.browser.find_element(By.NAME, 'password')
        username.send_keys('testuser')
        password.send_keys('12345')
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        products = self.browser.find_elements(By.CLASS_NAME, 'schedaProdotto')

        products[0].find_element(By.CLASS_NAME, 'aggiungiAlCarrello').click()
        self.browser.find_element(By.CSS_SELECTOR, 'li a[href*="carrello"]').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/carrello/')

        prodotti_carrello = self.browser.find_elements(By.CLASS_NAME, 'infoOggetto')
        self.assertTrue(len(prodotti_carrello) > 0)
        time.sleep(2)

    def test_aumenta_quantita(self):
        self.browser.get(self.live_server_url + '/login/')
        username = self.browser.find_element(By.NAME, 'username')
        password = self.browser.find_element(By.NAME, 'password')
        username.send_keys('testuser')
        password.send_keys('12345')
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        products = self.browser.find_elements(By.CLASS_NAME, 'schedaProdotto')

        products[0].find_element(By.CLASS_NAME, 'aggiungiAlCarrello').click()
        self.browser.find_element(By.CSS_SELECTOR, 'li a[href*="carrello"]').click()
        quantita_prima = int(self.browser.find_element(By.ID, 'quantita').text)
        self.browser.find_element(By.CSS_SELECTOR, 'a[href*="increase_quantity"]').click()
        quantita_dopo = int(self.browser.find_element(By.ID, 'quantita').text)
        self.assertEqual(quantita_dopo, quantita_prima + 1)
        time.sleep(2)

    def test_diminuisci_quantita(self):
        self.browser.get(self.live_server_url + '/login/')
        username = self.browser.find_element(By.NAME, 'username')
        password = self.browser.find_element(By.NAME, 'password')
        username.send_keys('testuser')
        password.send_keys('12345')
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        products = self.browser.find_elements(By.CLASS_NAME, 'schedaProdotto')

        products[0].find_element(By.CLASS_NAME, 'aggiungiAlCarrello').click()
        self.browser.find_element(By.CSS_SELECTOR, 'li a[href*="carrello"]').click()

        # Aumento la quantita
        self.browser.find_element(By.CSS_SELECTOR, 'a[href*="increase_quantity"]').click()
        quantita_prima = int(self.browser.find_element(By.ID, 'quantita').text)

        # Diminuisco la quantita
        self.browser.find_element(By.CSS_SELECTOR, 'a[href*="decrease_quantity"]').click()
        quantita_dopo = int(self.browser.find_element(By.ID, 'quantita').text)

        self.assertEqual(quantita_dopo, quantita_prima - 1)
        time.sleep(2)

    def test_rimuovi_dal_carrello(self):
        self.browser.get(self.live_server_url + '/login/')
        username = self.browser.find_element(By.NAME, 'username')
        password = self.browser.find_element(By.NAME, 'password')
        username.send_keys('testuser')
        password.send_keys('12345')
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        products = self.browser.find_elements(By.CLASS_NAME, 'schedaProdotto')

        products[0].find_element(By.CLASS_NAME, 'aggiungiAlCarrello').click()
        self.browser.find_element(By.CSS_SELECTOR, 'li a[href*="carrello"]').click()
        prodotti_carrello = self.browser.find_elements(By.CLASS_NAME, 'infoOggetto')
        self.assertTrue(len(prodotti_carrello) > 0)
        self.browser.find_element(By.CSS_SELECTOR, 'a[href*="remove_product"]').click()
        prodotti_carrello = self.browser.find_elements(By.CLASS_NAME, 'infoOggetto')
        self.assertTrue(len(prodotti_carrello) == 0)
        time.sleep(2)
    
    def test_ordine(self):
        self.browser.get(self.live_server_url + '/login/')
        username = self.browser.find_element(By.NAME, 'username')
        password = self.browser.find_element(By.NAME, 'password')
        username.send_keys('testuser')
        password.send_keys('12345')
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        products = self.browser.find_elements(By.CLASS_NAME, 'schedaProdotto')

        products[0].find_element(By.CLASS_NAME, 'aggiungiAlCarrello').click()
        self.browser.find_element(By.CSS_SELECTOR, 'li a[href*="carrello"]').click()

        prodotti_carrello = self.browser.find_elements(By.CLASS_NAME, 'infoOggetto')
        self.assertTrue(len(prodotti_carrello) == 1 )

        link_element = self.browser.find_element(By.LINK_TEXT, 'Pagamento')
        link_href = link_element.get_attribute("href")
        self.browser.get(link_href)

        #compila tutti i dati del checkout
        self.browser.find_element(By.NAME, 'nome').send_keys('NomeTest')
        self.browser.find_element(By.NAME, 'cognome').send_keys('CognomeTest')
        self.browser.find_element(By.NAME, 'email').send_keys('test@example.com')
        self.browser.find_element(By.NAME, 'indirizzo').send_keys('IndirizzoTest')
        self.browser.find_element(By.NAME, 'citta').send_keys('CittaTest')
        self.browser.find_element(By.NAME, 'regione').send_keys('RegioneTest')
        self.browser.find_element(By.NAME, 'provincia').send_keys('ProvinciaTest')
        self.browser.find_element(By.NAME, 'stato').send_keys('StatoTest')
        self.browser.find_element(By.NAME, 'codice_postale').send_keys('12345')
        self.browser.find_element(By.NAME, 'nome_carta').send_keys('NomeCartaTest')
        self.browser.find_element(By.NAME, 'numero_carta').send_keys('1234567890123456')
        self.browser.find_element(By.NAME, 'scadenza').send_keys('12/24')
        self.browser.find_element(By.NAME, 'cvv').send_keys('123')

        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        ordine_creato = Ordine.objects.filter(
            nome='NomeTest',
            cognome='CognomeTest',
            email='test@example.com',
            indirizzo='IndirizzoTest',
            stato='StatoTest',
            citta='CittaTest',
            regione='RegioneTest',
            provincia='ProvinciaTest',
            codice_postale='12345',
            # Assicurati che gli ID seguenti siano validi o sostituiscili con quelli appropriati
            pagamento__id=1,
            elemento_ordine__id=1
        ).first()

        self.assertIsNotNone(ordine_creato)
        time.sleep(5)


    def tearDown(self):
        self.browser.quit()