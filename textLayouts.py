from django.test import TestCase
from django.http import HttpRequest
from django.urls import resolve

from apps.login.views import index

\
#Aqui se pueba el login 
class TestIndexPage(TestCase):
	def test_have_index(self):
		response = self.client.get('/')

		self.assertTemplateUsed(response, '')
		self.assertTemplateUsed(response, '')