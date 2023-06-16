import time
from typing import Callable, Any

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By


class FunctionalTest(StaticLiveServerTestCase):
    """
    Функциональный тест
    """

    MAX_WAIT = 10
    USING_BROWSER = webdriver.Firefox

    def setUp(self) -> None:
        """Установка"""
        self.browser = self.USING_BROWSER()

    def tearDown(self) -> None:
        """Завершение"""
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text: str) -> None:
        """
        Ожидание строки в таблице списка
        """
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(by=By.ID, value='id_list_table')
                rows = table.find_elements(by=By.TAG_NAME, value='tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for(self, fn: Callable) -> Any:
        """Ожидать"""
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def get_item_input_box(self):
        """Получить поле ввода для элемента"""
        return self.browser.find_element(by=By.ID, value='id_text')
