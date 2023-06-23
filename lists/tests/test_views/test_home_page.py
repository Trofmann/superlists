from django.test import TestCase

from lists.forms import ItemForm


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

    def test_home_page_uses_item_form(self):
        """
        Тест: домашняя форма использует форму для элемента
        """
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)
