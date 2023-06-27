from selenium.webdriver.common.by import By

from .base import FunctionalTest


class MyListsPage(object):
    def __init__(self, test: FunctionalTest):
        self.test = test
