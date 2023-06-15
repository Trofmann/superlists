from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    """
    Тест макета и стилевого оформления
    """

    def test_layout_and_styling(self):
        """
        Тест: макет и стилевое оформление
        """
        # Эдит открывает домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Она замечает, что поле ввода аккуратно центрировано
        input_box = self.browser.find_element(by=By.ID, value='id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )

        # Она начинает новый список и видит,
        # что поле ввода там тоже аккуратно центрировано
        input_box.send_keys('testing')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        input_box = self.browser.find_element(by=By.ID, value='id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )
