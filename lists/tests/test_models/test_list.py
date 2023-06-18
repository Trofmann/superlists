from django.test import TestCase

from ...models import List


class ListModelTest(TestCase):
    """
    Тест модели списка
    """

    def test_get_absolute_url(self):
        """
        Тест: получен абсолютный url
        """
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')
