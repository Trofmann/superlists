from selenium import webdriver
from selenium.webdriver.common.by import By

from .base import FunctionalTest
from .list_page import ListPage


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):
    """
    Тест обмена данными
    """

    def test_can_share_a_list_with_another_user(self):
        """
        Тест: можно обмениваться списком с ещё одним пользователем
        """
        # Эдит является зарегистрированным пользователем
        self.create_pre_authenticated_session('edith@example.com')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # Её друг Анцифер тоже зависает на сайте списков
        oni_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authenticated_session('oniciferous@example.com')

        # Эдит открывает домашнюю страницу и начинает новый список
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Get help')

        # Она замечает опцию 'Поделиться этим списком'
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )

        # Она делится своим списком.
        # Страница обновляется и сообщает,
        # что теперь страница используется совместно с Анцифером
        list_page.share_list_with('oniciferous@example.com')
