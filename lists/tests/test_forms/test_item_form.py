from django.test import TestCase

from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import List, Item


class ItemFormTest(TestCase):
    """Тест формы для элемента списка"""

    def test_form_item_input_has_placeholder_and_css_classes(self):
        """
        Тест: форма отображает текстовое поле ввода
        """
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        """
        Тест: валидация формы для пустых элементов
        """
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR],
        )

