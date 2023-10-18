from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from django.test import LiveServerTestCase
from .models import *
from django.contrib.auth.models import User
import time

"Test di accettazione per il login"
class LoginTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(2)
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_login(self):
        self.browser.get(self.live_server_url + '/login/')
        username = self.browser.find_element_by_name('username')
        password = self.browser.find_element_by_name('password')
        username.send_keys('testuser')
        password.send_keys('12345')
        time.sleep(2)
        self.browser.find_element_by_name('submit').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/home/')
        time.sleep(2)