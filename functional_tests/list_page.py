from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from .base import wait, FunctionalTest


class ListPage(object):
    """Страница списка"""

    def __init__(self, test: FunctionalTest):
        self.test = test

    def get_table_rows(self) -> List[WebElement]:
        """Получить строки таблицы"""
        return self.test.browser.find_elements(by=By.CSS_SELECTOR, value='#id_list_table tr')

    @wait
    def wait_for_row_in_list_table(self, item_number: int, item_text: str) -> None:
        row_text = f'{item_number}: {item_text}'
        rows = self.get_table_rows()
        self.test.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self) -> WebElement:
        """Получить поле ввода для элемента"""
        return self.test.browser.find_element(by=By.ID, value='id_text')

    def add_list_item(self, item_text: str):
        """Добавить элемент списка"""
        new_item_no = len(self.get_table_rows()) + 1
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(new_item_no, item_text)
        return self

    def get_share_box(self) -> WebElement:
        """Получить поле для обмена списками"""
        return self.test.browser.find_element(
            by=By.CSS_SELECTOR,
            value='input[name="sharee"]'
        )

    def get_shared_with_list(self) -> List[WebElement]:
        """Получить список от того, кто им делится"""
        return self.test.browser.find_elements(
            by=By.CSS_SELECTOR,
            value='.list-sharee',
        )

    def share_list_with(self, email: str) -> None:
        """Поделиться списокм с"""
        self.get_share_box().send_keys(email)
        self.get_share_box().send_keys(Keys.ENTER)
        self.test.wait_for(
            lambda: self.test.assertIn(
                email,
                [item.text for item in self.get_shared_with_list()]
            )
        )

    def get_header(self) -> WebElement:
        return self.test.browser.find_element(by=By.TAG_NAME, value='h1')

    def get_title(self) -> str:
        return self.test.browser.title

    def get_body(self) -> WebElement:
        return self.test.browser.find_element(by=By.TAG_NAME, value='body')
