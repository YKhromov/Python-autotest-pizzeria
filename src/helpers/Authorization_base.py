import random

import allure
import pytest
from selenium.webdriver.common.by import By


def pytest_addoption(parser):
    parser.addini('authorization_name', 'Username for authorization')
    parser.addini('authorization_mail', 'E-mail for authorization')


class AuthBase:
    @pytest.fixture()
    def open_and_log_in(self, selenium, pytestconfig):
        with allure.step('Открытие страницы https://pizzeria.skillbox.cc/my-account/'):
            selenium.get("https://pizzeria.skillbox.cc/my-account/")
        auth_method = ['RandTester0', 'RandTester0@mail.ru']
        with allure.step('Ввод данных для авторизации'):
            selenium.find_element(By.CSS_SELECTOR, 'input#username').send_keys(random.choice(auth_method))
            selenium.find_element(By.CSS_SELECTOR, 'input#password').send_keys('RandTester011')
            selenium.find_element(By.CSS_SELECTOR, 'button[value="Войти"]').click()
