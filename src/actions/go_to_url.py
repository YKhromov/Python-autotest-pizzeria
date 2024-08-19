import allure
import pytest


@pytest.fixture()
def go_to_url(selenium):
    @allure.step('Ожидание загрузки страницы {value}')
    def callback(value):
        selenium.get(value)
    return callback
