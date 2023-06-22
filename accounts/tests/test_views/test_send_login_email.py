from unittest.mock import patch

from django.test import TestCase

from accounts.models import Token
from accounts.tests.const import EDITH_EMAIL
from accounts.views import CHECK_EMAIL_TEXT


class SendLoginEmailViewTest(TestCase):
    """Тест представления, которое отправляет сообщение для входа в систему"""

    def test_redirects_to_home_page(self):
        """Тест: переадресуется на домашнюю страницу"""
        response = self.client.post('/accounts/send_login_email', data={
            'email': EDITH_EMAIL,
        })
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_email.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        """
        Тест: отправляется сообщение на адрес из метода post
        """

        self.client.post('/accounts/send_login_email', data={
            'email': EDITH_EMAIL,
        })

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args

        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['edith@example.com'])

    def test_adds_success_message(self):
        """
        Тест: добавляется сообщение об успехе
        """
        response = self.client.post('/accounts/send_login_email', data={
            'email': EDITH_EMAIL,
        }, follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(message.message, CHECK_EMAIL_TEXT)
        self.assertEqual(message.tags, 'success')

    def test_creates_token_associated_with_email(self):
        """
        Тест: создаётся маркер, связанный с электронной почтой
        """
        self.client.post('/accounts/send_login_email', data={
            'email': EDITH_EMAIL,
        })
        token = Token.objects.first()
        self.assertEqual(token.email, EDITH_EMAIL)

    @patch('accounts.views.send_email.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        """
        Тест: отсылается ссылка на вход в систему, используя uid маркера
        """
        self.client.post('/accounts/send_login_email', data={
            'email': EDITH_EMAIL,
        })

        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)
