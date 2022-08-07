from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from .views import home_page
from django.template.loader import render_to_string


class HomePageTest(TestCase):
    """
    Тест домашней страницы
    """

    def test_uses_home_template(self):
        """
        Тест: используется шаблон домашней страницы
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')
