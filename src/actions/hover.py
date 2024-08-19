import allure
import pytest
from selenium import webdriver


@pytest.fixture()
def hover_element(selenium):
    @allure.step('Наведение курсора на {element}')
    def callback(element):
        action_chains = webdriver.ActionChains(selenium)
        action_chains.move_to_element(element).perform()
    return callback
