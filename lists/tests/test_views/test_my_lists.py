from django.test import TestCase


class MyListsTest(TestCase):
    """Тест 'Мои списки'"""

    def test_my_lists_url_renders_my_lists_template(self):
        response = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'lists/my_lists.html')
