from os import path

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
import pytest
import logging


def pytest_addoption(parser):
    parser.addini("page_load_strategy", "page load strategy")


@pytest.fixture()
def selenium(pytestconfig):
    logging.info('Prepare browser')
    service = Service(executable_path=path.join(path.dirname(path.abspath(__file__)), 'chromedriver.exe'))
    options = ChromeOptions()
    options.page_load_strategy = pytestconfig.getini('page_load_strategy')
    driver = Chrome(service=service, options=options)
    logging.info('Browser has been started')
    yield driver
    driver.quit()
    logging.info('Browser has been closed')
