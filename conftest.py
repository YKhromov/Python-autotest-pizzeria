import logging.config
from os import path


log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.ini')
logging.config.fileConfig(log_file_path)

pytest_plugins = [
    'src.fixtures',
    'src.actions',
    'src.actions.go_to_url',
    'src.actions.hover'
]


def pytest_addoption(parser):
    parser.addini("page_load_strategy", "page load strategy")
