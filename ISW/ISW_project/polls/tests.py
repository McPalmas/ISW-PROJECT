from django.test import TestCase
from .models import Prodotto


#Unit test for Prodotto model

class ProdottoModelTest(TestCase):
    def setUp(self):
        Prodotto.objects.create(id=100,nome='Prodotto di test', descrizione='Descrizione di test', prezzo=10.00)

    def test_prodotto_creation(self):
        prodotto = Prodotto.objects.get(id=100)
        self.assertEqual(prodotto.nome, 'Prodotto di test')
        self.assertEqual(prodotto.descrizione, 'Descrizione di test')
        self.assertEqual(prodotto.prezzo, 10.00)
    

