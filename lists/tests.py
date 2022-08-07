from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from .views import home_page


class HomePageTest(TestCase):
    """
    Тест домашней страницы
    """

    def test_root_url_resolvers_to_home_page_view(self):
        """
        Тест: корневой урл преобразуется в представление домашней страницы
        """
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """
        Тест: домашняя страница возвращает правильный html
        """
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf-8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do</title>', html)
        self.assertTrue(html.endswith('</html>'))