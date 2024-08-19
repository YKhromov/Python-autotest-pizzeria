import allure
import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def wait_element(selenium):
    @allure.step('Ожидание элемента по {by} со значением {value}')
    def callback(by, value):
        return WebDriverWait(selenium, timeout=30).until(
            lambda d: d.find_element(by, value)
        )
    return callback


@pytest.fixture
def wait_elements(selenium):
    @allure.step('Ожидание элементов по {by} со значением {value}')
    def callback(by, value):
        return WebDriverWait(selenium, timeout=30).until(
            lambda d: d.find_elements(by, value)
        )
    return callback


@pytest.fixture
def wait_and_click(selenium):
    @allure.step('Ожидание и нажатие на элемент по {by} со значением {value}')
    def callback(by, value):
        return WebDriverWait(selenium, timeout=30).until(
            EC.element_to_be_clickable((by, value))
        ).click()
    return callback


@pytest.fixture
def wait_visible_all(selenium):
    @allure.step('Ожидание отображения элементов по {by} со значением {value}')
    def callback(by, value):
        return WebDriverWait(selenium, timeout=30).until(
            EC.visibility_of_all_elements_located((by, value))
        )
    return callback


@pytest.fixture
def wait_visible_one(selenium):
    @allure.step('Ожидание отображения элемента по {by} со значением {value}')
    def callback(by, value):
        return WebDriverWait(selenium, timeout=30).until(
            EC.visibility_of_element_located((by, value))
        )
    return callback
