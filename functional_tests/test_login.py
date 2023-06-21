import re

from django.core import mail
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

TEST_EMAIL = 'edith@example.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
    """Тест регистрации в системе"""

    def test_can_get_email_link_to_log_in(self):
        """
        Тест: можно получить ссылку по почте для регистрации
        """
        # Эдит заходит на сайт суперсписков и впервые
        # замечает раздел 'войти' в навигационной панели
        # Он говорит ей ввести свой адрес электронной почты, что она и делает
        self.browser.get(self.live_server_url)
        self.browser.find_element(by=By.NAME, value='email').send_keys(TEST_EMAIL)
        self.browser.find_element(by=By.NAME, value='email').send_keys(Keys.ENTER)

        # Появляется сообщение, которое говорит, что ей на почту
        # было выслано электронное письмо
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element(by=By.TAG_NAME, value='body').text
        ))

        # Эдит проверяет почту и находит сообщение
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # Оно содержит ссылку на url-адрес
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Эдит нажимает на ссылку
        self.browser.get(url)

        # Она зарегистрирована в системе!
        self.wait_for(
            lambda: self.browser.find_element(by=By.LINK_TEXT, value='Log out')
        )
        navbar = self.browser.find_element(by=By.CSS_SELECTOR, value='.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)
