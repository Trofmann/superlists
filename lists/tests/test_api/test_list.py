import json
from django.test import TestCase

from lists.models import List, Item


class ListAPITest(TestCase):
    """Тест API списков"""
    base_url = '/api/lists/{}/'

    def get_list_url(self, list_):
        return self.base_url.format(list_.id)

    def test_get_returns_json_200(self):
        """
        Тест: возвращает json и код состояния 200
        """
        list_ = List.objects.create()
        response = self.client.get(self.get_list_url(list_))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_get_returns_items_correct_list(self):
        """
        Тест: получает отклик с элементами правильного списка
        """
        other_list = List.objects.create()
        Item.objects.create(list=other_list, text='item 1')
        correct_list = List.objects.create()
        item1 = Item.objects.create(list=correct_list, text='item 1')
        item2 = Item.objects.create(list=correct_list, text='item 2')
        response = self.client.get(self.get_list_url(correct_list))
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [
                {'id': item1.id, 'text': item1.text},
                {'id': item2.id, 'text': item2.text}
            ]
        )

    def test_POSTing_a_new_item(self):
        """
        Тест: отправляя POST-запрос, можно создать элемент списка
        """
        list_ = List.objects.create()
        response = self.client.post(
            self.get_list_url(list_),
            {'text': 'new item'},
        )
        self.assertEqual(response.status_code, 201)
        new_item = list_.item_set.get()
        self.assertEqual(new_item.text, 'new item')
