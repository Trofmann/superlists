import time
from typing import Callable, Any

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    """
    Функциональный тест
    """
    USING_BROWSER = webdriver.Firefox

    def setUp(self) -> None:
        """Установка"""
        self.browser = self.USING_BROWSER()

    def tearDown(self) -> None:
        """Завершение"""
        self.browser.quit()

    @wait
    def wait_for_row_in_list_table(self, row_text: str) -> None:
        """
        Ожидание строки в таблице списка
        """
        table = self.browser.find_element(by=By.ID, value='id_list_table')
        rows = table.find_elements(by=By.TAG_NAME, value='tr')
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_for(self, fn: Callable) -> Any:
        """Ожидать"""
        return fn()

    def get_item_input_box(self):
        """Получить поле ввода для элемента"""
        return self.browser.find_element(by=By.ID, value='id_text')

    def get_navbar(self):
        """Получить навигационную панель"""
        return self.browser.find_element(by=By.CSS_SELECTOR, value='.navbar')

    @wait
    def wait_to_be_logged_in(self, email):
        """Ожидать входа в систему"""
        self.browser.find_element(by=By.LINK_TEXT, value='Log out')
        navbar = self.get_navbar()
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        """Ожидать выхода из системы"""
        self.browser.find_element(by=By.NAME, value='email')
        navbar = self.get_navbar()
        self.assertNotIn(email, navbar.text)

    def add_list_item(self, item_text):
        """Добавить элемент списка"""
        num_rows = len(self.browser.find_elements(by=By.CSS_SELECTOR, value='#id_list_table tr'))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f'{item_number}: {item_text}')
