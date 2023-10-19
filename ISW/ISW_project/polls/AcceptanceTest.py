from telnetlib import EC

from selenium import webdriver
from selenium.webdriver.common import by
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from .models import Prodotto
import time

from selenium.webdriver.support.wait import WebDriverWait

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
        self.assertEqual(quantita_dopo,quantita_prima+1)
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

        #Aumento la quantita
        self.browser.find_element(By.CSS_SELECTOR, 'a[href*="increase_quantity"]').click()
        quantita_prima= int(self.browser.find_element(By.ID, 'quantita').text)

        #Diminuisco la quantita
        self.browser.find_element(By.CSS_SELECTOR, 'a[href*="decrease_quantity"]').click()
        quantita_dopo = int(self.browser.find_element(By.ID, 'quantita').text)

        self.assertEqual(quantita_dopo, quantita_prima -1)
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
        products[1].find_element(By.CLASS_NAME, 'aggiungiAlCarrello').click()
        self.browser.find_element(By.CSS_SELECTOR, 'li a[href*="carrello"]').click()

        prodotti_carrello_prima = len(self.browser.find_elements(By.CLASS_NAME, 'infoOggetto'))
        self.browser.find_element(By.CSS_SELECTOR, 'a[href*="remove_product"]').click()
        prodotti_carrello_dopo = len(self.browser.find_elements(By.CLASS_NAME, 'infoOggetto'))
        self.assertEqual(prodotti_carrello_prima,prodotti_carrello_dopo+1)
        time.sleep(2)

    def tearDown(self):
        self.browser.quit()