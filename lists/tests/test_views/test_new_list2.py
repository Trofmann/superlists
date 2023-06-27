from unittest.mock import patch, Mock

from django.http import HttpRequest
from django.test import TestCase  # Надо использовать unittest.TestCase, но с ним не работает, т.к не запущена Django

from lists.views import new_list2


@patch('lists.views.view_new_list.NewListForm')
class NewListUnitTest(TestCase):
    """Модульный тест нового представления списка"""

    def setUp(self) -> None:
        """Установка"""
        self.request = HttpRequest()
        self.request.POST['text'] = 'new list item'
        self.request.user = Mock()

    def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
        """
        Тест: передаются POST-данные в новую форму списка
        """
        mock_form = mockNewListForm.return_value
        list_ = mock_form.save.return_value
        list_.get_absolute_url.return_value = 'fakeurl'

        new_list2(self.request)

        mockNewListForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_valid(self, mockNewListForm):
        """
        Тест: сохраняет форму с владельцем, если форма допустима
        """
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        list_ = mock_form.save.return_value
        list_.get_absolute_url.return_value = 'fakeurl'

        new_list2(self.request)

        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch('lists.views.view_new_list.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(
            self, mock_redirect, mockNewListForm,
    ):
        """
        Тест: переадресует в возвращаемый формой объект,
        если форма допустима
        """
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True

        response = new_list2(self.request)

        self.assertEqual(response, mock_redirect.return_value)

        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @patch('lists.views.view_new_list.render')
    def test_renders_home_template_with_form_if_form_invalid(
            self, mock_render, mockNewListForm
    ):
        """
        Тест: отображает домашний шаблон с формой, если форма недопустима
        """
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        response = new_list2(self.request)

        # self.assertEqual(response, mock_render)

        mock_render.assert_called_once_with(
            self.request, 'lists/home.html', dict(form=mock_form)
        )

    def test_does_not_save_if_form_invalid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        new_list2(self.request)

        self.assertFalse(mock_form.save.called)
