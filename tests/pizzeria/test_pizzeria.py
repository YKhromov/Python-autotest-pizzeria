import random
import time
import allure

from random import randint
from datetime import timedelta, datetime

from playwright.async_api import Playwright
from playwright.sync_api import Page
import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from src.helpers.Authorization_base import AuthBase
from src.utils.numbers import only_numbers


@allure.feature('Проект по автоматизации тестирования сайта Pizzeria на Python')
class TestPractice(AuthBase):
    @allure.title('Кейс №1. Проверка добавления товара в корзину с помощью кнопки на главной странице')
    def test_case_1(self, selenium, wait_element, go_to_url, hover_element, wait_and_click, wait_elements):
        go_to_url('https://pizzeria.skillbox.cc/')
        pizza_on_screen = wait_elements(
            By.XPATH, './/li[contains(@class, "span3 wow flipInY  slick-slide slick-active")]')
        with allure.step('Выбор случайной пиццы'):
            pizza_num = randint(1, len(pizza_on_screen))
            chosen_pizza = wait_element(
                By.XPATH,
                f'.//li[contains(@class, "span3 wow flipInY  slick-slide slick-active")][{pizza_num}]'
            )
        with allure.step('Добавление выбранной пиццы в корзину'):
            hover_element(chosen_pizza)
            expected_pizza = chosen_pizza.find_element(By.XPATH, './descendant::h3') \
                .get_attribute('textContent')
            expected_sum = chosen_pizza.find_element(By.XPATH, './descendant::span/span') \
                .get_attribute('textContent')
            wait_and_click(
                By.XPATH,
                f'.//li[contains(@class, "span3 wow flipInY  slick-slide slick-active")][{pizza_num}]/*/a[2]')
        with allure.step('Ожидание и проверка изменения суммы в корзине'):
            WebDriverWait(selenium, 10).until(lambda d: only_numbers(d.find_element(
                By.CLASS_NAME, 'cart-contents').get_attribute('textContent')) != 0)
            order_summ = selenium.find_element(By.CLASS_NAME, 'cart-contents').get_attribute('textContent')
            assert only_numbers(expected_sum) == only_numbers(order_summ)
        with allure.step('Переход в Корзину'):
            selenium.find_element(By.LINK_TEXT, 'Корзина').click()
        with allure.step('Проверка соответствия пиццы в корзине выбранной пицце'):
            actual_pizza = wait_element(By.XPATH, './/tbody/descendant::td[@class="product-name"]/a') \
                .get_attribute('textContent')
            order_summ = wait_element(By.XPATH, './/td[@class="product-subtotal"]//bdi') \
                .get_attribute('textContent')
            assert actual_pizza in expected_pizza.translate(str.maketrans('«»', '""'))
            assert expected_sum == order_summ
        pass

    @allure.title('Кейс №2. Проверка переключения слайдера на главной странице вправо')
    def test_case_2(self, selenium, go_to_url, wait_elements, wait_visible_all,
                    hover_element, wait_and_click):
        go_to_url('https://pizzeria.skillbox.cc/')
        wait_visible_all(
            By.XPATH,
            './/li[contains(@class, "span3 wow flipInY  slick-slide slick-active")]/descendant::img')
        with allure.step('Определение количества элементов в слайдере'):
            all_elements = wait_elements(
                By.XPATH, './/li[contains(@class, "span3 wow flipInY  slick-slide")]/descendant::h3')
            clones = selenium.find_elements(By.XPATH, './/li[contains(@class, "slick-cloned")]')
            unique_pizza = len(all_elements) - len(clones)
        with allure.step('Определение количества элементов слайдера на экране'):
            pizza_on_screen = selenium.find_elements(
                By.XPATH, './/li[contains(@class, "span3 wow flipInY  slick-slide slick-active")]/descendant::h3')
            first_pizza = pizza_on_screen[0].get_attribute('textContent')
            last_pizza = pizza_on_screen[len(pizza_on_screen) - 1].get_attribute('textContent')
            expected_pizza = all_elements[len(pizza_on_screen) * 2].get_attribute('textContent')
            k = 0  # коэффициент для нового круга в слайдере

        for i in range(unique_pizza + 1):
            with allure.step('Переключение слайдера вправо'):
                hover_element(selenium.find_element(By.CSS_SELECTOR, 'a.slick-next'))
                wait_and_click(By.CSS_SELECTOR, 'a.slick-next')
                time.sleep(1)
            with allure.step('Проверка корректности переключения'):
                pizza_on_screen = selenium.find_elements(
                    By.XPATH,
                    './/li[contains(@class, "slick-active")]/descendant::h3[contains(text(), "Пицца")]')
                penult_pizza = pizza_on_screen[len(pizza_on_screen) - 2].get_attribute('textContent')
                new_last_pizza = pizza_on_screen[len(pizza_on_screen) - 1].get_attribute('textContent')
                assert penult_pizza == last_pizza
                assert new_last_pizza == expected_pizza
                if i - unique_pizza * (k + 1) == len(pizza_on_screen):
                    assert new_last_pizza == first_pizza
                last_pizza = new_last_pizza
                if i % (unique_pizza) == 0:
                    k += 1
                expected_pizza = all_elements[len(pizza_on_screen) * 2 - unique_pizza * k + 1 + i] \
                    .get_attribute('textContent')
        pass

    @allure.title('Кейс №3. Проверка переключения слайдера на главной странице влево')
    def test_case_3(self, selenium, go_to_url, wait_and_click, wait_elements, wait_visible_all, hover_element):
        go_to_url('https://pizzeria.skillbox.cc/')
        wait_visible_all(
            By.XPATH,
            './/li[contains(@class, "span3 wow flipInY  slick-slide slick-active")]/descendant::img')
        with allure.step('Определение количества элементов в слайдере'):
            all_elements = wait_elements(
                By.XPATH, './/li[contains(@class, "span3 wow flipInY  slick-slide")]/descendant::h3')
            clones = selenium.find_elements(By.XPATH, './/li[contains(@class, "slick-cloned")]')
            unique_pizza = len(all_elements) - len(clones)
        with allure.step('Определение количества элементов слайдера на экране'):
            pizza_on_screen = selenium.find_elements(
                By.XPATH, './/li[contains(@class, "span3 wow flipInY  slick-slide slick-active")]/descendant::h3')
            first_pizza = pizza_on_screen[0].get_attribute('textContent')
            last_pizza = pizza_on_screen[len(pizza_on_screen) - 1].get_attribute('textContent')
            expected_pizza = all_elements[len(pizza_on_screen) - 1].get_attribute('textContent')
            k = 0  # коэффициент для нового круга в слайдере

        for i in range(unique_pizza + 1):
            with allure.step('Переключение слайдера влево'):
                hover_element(selenium.find_element(By.CSS_SELECTOR, 'a.slick-prev'))
                wait_and_click(By.CSS_SELECTOR, 'a.slick-prev')
                time.sleep(1)
            with allure.step('Проверка корректности переключения'):
                pizza_on_screen = selenium.find_elements(
                    By.XPATH,
                    './/li[contains(@class, "slick-active")]/descendant::h3[contains(text(), "Пицца")]')
                second_pizza = pizza_on_screen[1].get_attribute('textContent')
                new_first_pizza = pizza_on_screen[0].get_attribute('textContent')
                assert second_pizza == first_pizza
                assert new_first_pizza == expected_pizza
                if i - unique_pizza * (k + 1) == len(pizza_on_screen):
                    assert new_first_pizza == last_pizza
                first_pizza = new_first_pizza
                if i != 0 and i % unique_pizza == 0:
                    k += 1
                expected_pizza = all_elements[len(pizza_on_screen) * 2 - 1 - i + unique_pizza * k] \
                    .get_attribute('textContent')
        pass

    @allure.title('Кейс №4. Проверка перехода в карточку товара через слайдер на главной странице')
    def test_case_4(self, go_to_url, wait_element, wait_elements, wait_visible_all, hover_element):
        go_to_url('https://pizzeria.skillbox.cc/')
        wait_visible_all(
            By.XPATH,
            './/li[contains(@class, "span3 wow flipInY  slick-slide slick-active")]/descendant::img')
        with allure.step('Определение списка пицц на экране'):
            pizza_on_screen = wait_elements(
                By.XPATH, './/li[contains(@class, "span3 wow flipInY  slick-slide slick-active")]')
        with allure.step('Выбор случайной пиццы'):
            pizza_num = randint(1, len(pizza_on_screen))
            chosen_pizza = wait_element(
                By.XPATH,
                f'.//li[contains(@class, "span3 wow flipInY  slick-slide slick-active")][{pizza_num}]'
            )
            expected_pizza = chosen_pizza.find_element(By.XPATH, './descendant::h3') \
                .get_attribute('textContent')
        with allure.step('Нажатие по изображению выбранной пиццы'):
            chosen_pizza.find_element(By.XPATH, './div/a').click()
        with allure.step('Проверка соответствия открытой карточки'):
            actual_pizza = wait_element(
                By.XPATH, './/h1[contains(@class, "product_title entry-title")]').get_attribute('textContent')
            assert expected_pizza == actual_pizza
        pass

    @allure.title('Кейс №5. Тестирование функции выбора дополнительных опций в карточке товара')
    def test_case_5(self, selenium, go_to_url, wait_element, wait_visible_all, wait_elements):
        go_to_url('https://pizzeria.skillbox.cc/')
        wait_visible_all(
            By.XPATH,
            './/li[contains(@class, "span3 wow flipInY  slick-slide slick-active")]/descendant::img')
        with allure.step('Определение списка пицц на экране'):
            pizza_on_screen = wait_elements(
                By.XPATH, './/li[contains(@class, "span3 wow flipInY  slick-slide slick-active")]')
        with allure.step('Выбор случайной пиццы'):
            pizza_num = randint(1, len(pizza_on_screen))
            chosen_pizza = wait_element(
                By.XPATH,
                f'.//li[contains(@class, "span3 wow flipInY  slick-slide slick-active")][{pizza_num}]'
            )
        with allure.step('Нажатие по изображению выбранной пиццы'):
            chosen_pizza.find_element(By.XPATH, './div/a').click()
        first_price = wait_element(
            By.XPATH, './/div[contains(@class, "summary entry-summary")]/descendant::bdi') \
            .get_attribute('textContent')
        with allure.step('Открытие списка дополнительных опций'):
            selenium.find_element(
                By.XPATH, './/span[contains(@class, "woocommerce-input-wrapper")]').click()
        with allure.step('Выбор случайной опции'):
            available_options = wait_visible_all(By.XPATH, './/option')
            chosen_option = available_options[randint(1, len(available_options) - 1)]
            option_price = chosen_option.get_attribute('value')
            chosen_option.click()
        with allure.step('Проверка изменения стоимости пиццы'):
            new_price = wait_element(
                By.XPATH, './/div[contains(@class, "summary entry-summary")]/descendant::bdi') \
                .get_attribute('textContent')
            assert chosen_option.get_attribute('textContent') in selenium.find_element(
                By.XPATH, './/span[contains(@class, "woocommerce-input-wrapper")]') \
                .get_attribute('textContent')
            assert only_numbers(first_price) + only_numbers(option_price) == only_numbers(new_price)
        pass

    @allure.title('Кейс №6. Проверка добавления товара в корзину из карточки товара')
    def test_case_6(self, selenium, go_to_url, wait_element, wait_visible_all, wait_elements):
        go_to_url('https://pizzeria.skillbox.cc/')
        wait_visible_all(
            By.XPATH,
            './/li[contains(@class, "span3 wow flipInY  slick-slide slick-active")]/descendant::img')
        with allure.step('Определение списка пицц на экране'):
            pizza_on_screen = wait_elements(
                By.XPATH, './/li[contains(@class, "span3 wow flipInY  slick-slide slick-active")]')
        with allure.step('Выбор случайной пиццы'):
            pizza_num = randint(1, len(pizza_on_screen))
            chosen_pizza = wait_element(
                By.XPATH,
                f'.//li[contains(@class, "span3 wow flipInY  slick-slide slick-active")][{pizza_num}]'
            )
            expected_pizza = chosen_pizza.find_element(By.XPATH, './descendant::h3') \
                .get_attribute('textContent')
        with allure.step('Нажатие по изображению выбранной пиццы'):
            chosen_pizza.find_element(By.XPATH, './div/a').click()
        with allure.step('Открытие списка дополнительных опций'):
            selenium.find_element(
                By.XPATH, './/span[contains(@class, "woocommerce-input-wrapper")]').click()
        with allure.step('Выбор случайной опции'):
            available_options = wait_visible_all(By.XPATH, './/option')
            chosen_option = available_options[randint(0, len(available_options) - 1)]
            chosen_option.click()
        new_price = wait_element(
            By.XPATH, './/div[contains(@class, "summary entry-summary")]/descendant::bdi') \
            .get_attribute('textContent')
        with allure.step('Добавление пиццы в корзину'):
            selenium.find_element(
                By.XPATH, './/button[contains(@class, "single_add_to_cart_button button alt")]').click()
        with allure.step('Переход в корзину'):
            selenium.find_element(By.LINK_TEXT, 'Корзина').click()
        with allure.step('Проверка соответствия пиццы в корзине выбранной пицце'):
            actual_pizza = wait_element(By.XPATH, './/tbody/descendant::td[@class="product-name"]/a') \
                .get_attribute('textContent')
            order_summ = wait_element(By.XPATH, './/td[@class="product-subtotal"]//bdi') \
                .get_attribute('textContent')
            assert actual_pizza in expected_pizza.translate(str.maketrans('«»', '""'))
            assert new_price == order_summ
        pass

    @allure.title('Кейс №7. Проверка увеличения количества товара в корзине')
    def test_case_7(self, selenium, go_to_url, wait_element, wait_visible_all, wait_elements):
        go_to_url('https://pizzeria.skillbox.cc/')
        wait_visible_all(
            By.XPATH,
            './/li[contains(@class, "span3 wow flipInY  slick-slide slick-active")]/descendant::img')
        with allure.step('Определение списка пицц на экране'):
            pizza_on_screen = wait_elements(
                By.XPATH, './/li[contains(@class, "span3 wow flipInY  slick-slide slick-active")]')
        with allure.step('Выбор случайной пиццы'):
            pizza_num = randint(1, len(pizza_on_screen))
            chosen_pizza = wait_element(
                By.XPATH,
                f'.//li[contains(@class, "span3 wow flipInY  slick-slide slick-active")][{pizza_num}]'
            )
        with allure.step('Нажатие по изображению выбранной пиццы'):
            chosen_pizza.find_element(By.XPATH, './div/a').click()
        with allure.step('Открытие списка дополнительных опций'):
            selenium.find_element(
                By.XPATH, './/span[contains(@class, "woocommerce-input-wrapper")]').click()
        with allure.step('Выбор случайной опции'):
            available_options = wait_visible_all(By.XPATH, './/option')
            chosen_option = available_options[randint(0, len(available_options) - 1)]
            chosen_option.click()
        with allure.step('Добавление пиццы в корзину'):
            selenium.find_element(
                By.XPATH, './/button[contains(@class, "single_add_to_cart_button button alt")]').click()
        with allure.step('Переход в корзину'):
            selenium.find_element(By.LINK_TEXT, 'Корзина').click()
        pizza_amount = wait_element(By.XPATH, './/input[contains(@class, "input-text qty text")]')
        pizza_price = wait_element(By.XPATH, './/td[@class="product-price"]/span/bdi') \
            .get_attribute('textContent')
        with allure.step('Ввод случайного количества пицц'):
            new_amount = randint(1, 100)
            pizza_amount.clear()
            pizza_amount.send_keys(new_amount)
        with allure.step('Обновление корзины'):
            selenium.find_element(By.XPATH, './/button[@name="update_cart"]').click()
            time.sleep(1)
        with allure.step('Проверка изменения стоимости позиции с учетом нового количества'):
            order_summ = wait_element(By.XPATH, './/td[@class="product-subtotal"]//bdi') \
                .get_attribute('textContent')
            assert only_numbers(pizza_price) * new_amount == only_numbers(order_summ)
        pass

    @allure.title('Кейс №8. Проверка удаления товара из корзины')
    def test_case_8(self, selenium, go_to_url, wait_element, wait_visible_all, wait_elements):
        go_to_url('https://pizzeria.skillbox.cc/')
        wait_visible_all(
            By.XPATH,
            './/li[contains(@class, "span3 wow flipInY  slick-slide slick-active")]/descendant::img')
        with allure.step('Определение списка пицц на экране'):
            pizza_on_screen = wait_elements(
                By.XPATH, './/li[contains(@class, "span3 wow flipInY  slick-slide slick-active")]')
        with allure.step('Выбор случайной пиццы'):
            pizza_num = randint(1, len(pizza_on_screen))
            chosen_pizza = wait_element(
                By.XPATH,
                f'.//li[contains(@class, "span3 wow flipInY  slick-slide slick-active")][{pizza_num}]'
            )
        with allure.step('Нажатие по изображению выбранной пиццы'):
            chosen_pizza.find_element(By.XPATH, './div/a').click()
        with allure.step('Открытие списка дополнительных опций'):
            selenium.find_element(
                By.XPATH, './/span[contains(@class, "woocommerce-input-wrapper")]').click()
        with allure.step('Выбор случайной опции'):
            available_options = wait_visible_all(By.XPATH, './/option')
            chosen_option = available_options[randint(0, len(available_options) - 1)]
            chosen_option.click()
        with allure.step('Добавление пиццы в корзину'):
            selenium.find_element(
                By.XPATH, './/button[contains(@class, "single_add_to_cart_button button alt")]').click()
        with allure.step('Переход в корзину'):
            selenium.find_element(By.LINK_TEXT, 'Корзина').click()
        with allure.step('Удаление пиццы из корзины'):
            wait_element(By.CSS_SELECTOR, 'a.remove').click()
        with allure.step('Проверка отсутствия товаров в корзине'):
            wait_element(By.XPATH, './/p[contains(text(), "Корзина пуста.")]')
            time.sleep(0.5)
            assert only_numbers(wait_element(By.CLASS_NAME, 'cart-contents').get_attribute('textContent')) == 0
        pass

    @allure.title('Кейс №9. Проверка просмотра всех товаров определенной категории через рубрикатор')
    def test_case_9(self, go_to_url, wait_element, wait_visible_one, hover_element):
        go_to_url('https://pizzeria.skillbox.cc/')
        with allure.step('Открытие рубрикатора с категориями'):
            hover_element(wait_element(By.XPATH, './/a[contains(text(), "Меню")]/parent::li'))
        with allure.step('Выбор категории "Десерты"'):
            wait_visible_one(By.XPATH, './/a[contains(text(), "Десерты")]').click()
        with allure.step('Проверка соответствия открывшеся категории выбранной'):
            wait_element(By.XPATH, './/h1[contains(text(), "Десерты")]')
        pass

    @allure.title('Кейс №10. Проверка добавления товара со страницы "меню" (десерт, не дороже 135 рублей)')
    def test_case_10(self, selenium, go_to_url, wait_element, wait_visible_one, wait_elements, hover_element):
        budget = 13500
        go_to_url('https://pizzeria.skillbox.cc/')
        with allure.step('Открытие рубрикатора с категориями'):
            hover_element(wait_element(By.XPATH, './/a[contains(text(), "Меню")]/parent::li'))
        with allure.step('Выбор категории "Десерты"'):
            wait_visible_one(By.XPATH, './/a[contains(text(), "Десерты")]').click()
        with allure.step('Определение десертов, подходящих под заданный бюджет'):
            dessert_on_screen = wait_elements(
                By.XPATH, './/li[contains(@class, "type-product")]')
            available_to_order = []
            for i in dessert_on_screen:
                price = i.find_element(By.XPATH, './/bdi').get_attribute('textContent')
                if only_numbers(price) <= budget:
                    available_to_order.append(i)
        with allure.step('Выбор случайного десерта из доступных'):
            dessert_num = randint(1, len(available_to_order))
            chosen_dessert = available_to_order[dessert_num - 1].find_element(By.XPATH, './/h3') \
                .get_attribute('textContent')
            price = available_to_order[dessert_num - 1].find_element(By.XPATH, './/bdi') \
                .get_attribute('textContent')
        with allure.step('Добавление выбранного десерта в корзину'):
            available_to_order[dessert_num - 1].find_element(By.XPATH, './/a[contains(text(), "В корзину")]').click()
            time.sleep(1)
        with allure.step('Проверка корректности изменения суммы в корзине'):
            order_summ = selenium.find_element(By.CLASS_NAME, 'cart-contents').get_attribute('textContent')
            assert only_numbers(price) == only_numbers(order_summ)
        with allure.step('Переход в корзину'):
            selenium.find_element(By.LINK_TEXT, 'Корзина').click()
        with allure.step('Проверка соответствия десерта в корзине выбранному десерту'):
            actual_dessert = wait_element(By.XPATH, './/tbody/descendant::td[@class="product-name"]/a') \
                .get_attribute('textContent')
            order_summ = wait_element(By.XPATH, './/td[@class="product-subtotal"]//bdi') \
                .get_attribute('textContent')
            assert actual_dessert in chosen_dessert.translate(str.maketrans('«»', '""'))
            assert only_numbers(price) == only_numbers(order_summ)
        pass

    @allure.title('Кейс №11. Проверка оформления заказа без авторизации')
    def test_case_11(self, selenium, go_to_url, wait_element, wait_and_click, wait_visible_all, hover_element):
        go_to_url('https://pizzeria.skillbox.cc/')
        with allure.step('Переход к десертам и ожидание анимации появления'):
            action = webdriver.ActionChains(selenium)
            action.scroll_to_element(selenium.find_element(By.XPATH, './/h2[contains(text(), "Напитки")]')).perform()
            time.sleep(0.5)
        with allure.step('Определение списка десертов на экране'):
            dessert_on_screen = wait_visible_all(
                By.XPATH,
                './/a/h3[contains(text(), "Десерт")]/ancestor::li')
        with allure.step('Выбор случайного десерта'):
            dessert_num = randint(1, len(dessert_on_screen))
            chosen_dessert = dessert_on_screen[dessert_num - 1]
        with allure.step('Добавление выбранного десерта в корзину'):
            hover_element(chosen_dessert)
            wait_and_click(By.XPATH, f'(.//a/h3[contains(text(), "Десерт")])[{dessert_num}]'
                                     f'/ancestor::li//a[contains(text(), "В корзину")]')
            time.sleep(1)
        with allure.step('Переход в корзину'):
            selenium.find_element(By.LINK_TEXT, 'Корзина').click()
        with allure.step('Переход к оформлению заказа'):
            wait_element(By.XPATH, './/a[contains(text(), "ПЕРЕЙТИ К ОПЛАТЕ")]').click()
        with allure.step('Проверка необходимости авторизации'):
            wait_element(By.LINK_TEXT, 'Авторизуйтесь')
            wait_element(By.XPATH, './/div[text()="Для оформления заказа необходимо авторизоваться."]')
        pass

    @allure.title('Кейс №12. Тестирование функции регистрации на сайте')
    def test_case_12(self, selenium, go_to_url, wait_element, hover_element):
        go_to_url('https://pizzeria.skillbox.cc/')
        reg_base = 'RT' + (datetime.now()).strftime('%d%m%H%M%S')
        with allure.step('Переход в раздел "Мой аккаунт"'):
            selenium.find_element(By.LINK_TEXT, 'Мой аккаунт').click()
        with allure.step('Переход в форму регистрации'):
            wait_element(By.CLASS_NAME, 'custom-register-button').click()
        with allure.step('Заполнение формы регистрации'):
            wait_element(By.CSS_SELECTOR, 'input#reg_username').send_keys(reg_base)
            wait_element(By.CSS_SELECTOR, 'input#reg_email').send_keys(reg_base + '@mail.ru')
            wait_element(By.CSS_SELECTOR, 'input#reg_password').send_keys(reg_base)
        with allure.step('Отправка заполненной формы'):
            wait_element(By.CSS_SELECTOR, 'button[value="Зарегистрироваться"]').click()
            time.sleep(0.5)
        with allure.step('Переход в раздел "Мой аккаунт"'):
            selenium.find_element(By.XPATH, './/a[contains(text(), "Мой аккаунт")]').click()
        with allure.step('Проверка соответствия имени в приветствии указанному при регистрации'):
            wait_element(By.XPATH, f'.//strong[contains(text(), "{reg_base}")]')
        pass

    @allure.title('Кейс №13. Проверка оформления заказа авторизованным пользователем')
    def test_case_13(self, selenium, open_and_log_in, go_to_url, wait_element, wait_and_click,
                     wait_elements, wait_visible_all, hover_element):
        expected_address = 'Вязова 13'
        expected_city = 'Сайлент Хил'
        expected_state = 'Тьмы'
        expected_postcode = '131313'
        expected_phone = '+79876543210'
        expected_mail = 'RandTester0@mail.ru'
        expected_first_name = 'Тестер'
        expected_last_name = 'Рандомный'

        go_to_url('https://pizzeria.skillbox.cc/')
        with allure.step('Переход к десертам и ожидание анимации появления'):
            action = webdriver.ActionChains(selenium)
            action.scroll_to_element(selenium.find_element(By.XPATH, './/h2[contains(text(), "Напитки")]')).perform()
            time.sleep(0.5)
        with allure.step('Определение списка десертов на экране'):
            dessert_on_screen = wait_visible_all(
                By.XPATH,
                './/a/h3[contains(text(), "Десерт")]/ancestor::li')
        with allure.step('Выбор случайного десерта'):
            dessert_num = randint(1, len(dessert_on_screen))
            chosen_dessert = dessert_on_screen[dessert_num - 1]
        with allure.step('Добавление выбранного десерта в корзину'):
            hover_element(chosen_dessert)
            wait_and_click(By.XPATH, f'(.//a/h3[contains(text(), "Десерт")])[{dessert_num}]'
                                     f'/ancestor::li//a[contains(text(), "В корзину")]')
            time.sleep(1)
        with allure.step('Переход в корзину'):
            selenium.find_element(By.LINK_TEXT, 'Корзина').click()
        with allure.step('Переход к оформлению заказа'):
            wait_element(By.XPATH, './/a[contains(text(), "ПЕРЕЙТИ К ОПЛАТЕ")]').click()
        with allure.step('Заполнение формы'):
            with allure.step('Ввод имени'):
                first_name = wait_element(By.CSS_SELECTOR, 'input#billing_first_name')
                first_name.clear()
                first_name.send_keys(expected_first_name)
            with allure.step('Ввод фамилии'):
                surname = wait_element(By.CSS_SELECTOR, 'input#billing_last_name')
                surname.clear()
                surname.send_keys(expected_last_name)
            with allure.step('Выбор страны из списка'):
                wait_and_click(By.CSS_SELECTOR, 'span.selection')
                countries = wait_elements(By.XPATH, './/li[contains(@class, "select2-results__option")]')
                countries.pop(0)
                # chosen_country = countries[21]
                chosen_country = random.choice(countries)
                expected_country = chosen_country.get_attribute('textContent')
                chosen_country.click()
            with allure.step('Ввод адреса'):
                billing_address = wait_element(By.CSS_SELECTOR, 'input#billing_address_1')
                billing_address.clear()
                billing_address.send_keys(expected_address)
            with allure.step('Проверка наличия поля ввода названия города'):
                if selenium.find_element(By.CSS_SELECTOR, 'p#billing_city_field').get_attribute(
                        'style') != 'display: none;':
                    with allure.step('Ввод названия города'):
                        billing_city = wait_element(By.CSS_SELECTOR, 'input#billing_city')
                        billing_city.clear()
                        billing_city.send_keys(expected_city)
                        city_option = 1
                else:
                    city_option = 0
            with allure.step('Проверка наличия и вида поля ввода области'):
                if selenium.find_element(By.CSS_SELECTOR, 'p#billing_state_field label *') \
                        .get_attribute('class') == 'required':
                    state_option = 1
                try:
                    billing_state = selenium.find_element(By.CSS_SELECTOR, 'input#billing_state')
                    if billing_state.get_attribute('class') != 'hidden':
                        with allure.step('Ввод названия области'):
                            billing_state.clear()
                            billing_state.send_keys(expected_state)
                    else:
                        state_option = 0
                except NoSuchElementException:
                    with allure.step('Выбор случайной области из списка'):
                        wait_and_click(By.CSS_SELECTOR, 'span#select2-billing_state-container')
                        states = wait_elements(By.XPATH, './/li[contains(@class, "select2-results__option")]')
                        states.pop(0)
                        chosen_state = random.choice(states)
                        expected_state = chosen_state.get_attribute('textContent')
                        chosen_state.click()

            with allure.step('Проверка наличия поля ввода почтового индекса'):
                billing_postcode = wait_element(By.CSS_SELECTOR, 'input#billing_postcode')
                if selenium.find_element(By.CSS_SELECTOR, 'p#billing_postcode_field') \
                        .get_attribute('style') != 'display: none;':
                    with allure.step('Ввод почтового индекса'):
                        billing_postcode.clear()
                        billing_postcode.send_keys(expected_postcode)
                        if selenium.find_element(By.CSS_SELECTOR, 'p#billing_postcode_field label *') \
                                .get_attribute('class') == 'required':
                            postcode_option = 1
                        else:
                            postcode_option = 0
                else:
                    postcode_option = 0
            with allure.step('Ввод номера телефона'):
                billing_phone = wait_element(By.CSS_SELECTOR, 'input#billing_phone')
                billing_phone.clear()
                billing_phone.send_keys(expected_phone)
            with allure.step('Ввод завтрашнего дня в поле с датой доставки'):
                tomorrow = (datetime.now() + timedelta(days=1)).strftime('%d.%m.%Y')
                wait_element(By.CSS_SELECTOR, 'input#order_date').send_keys(tomorrow)
            with allure.step('Случайный выбор метода оплаты'):
                payment_methods = ['payment_method_bacs', 'payment_method_cod']
                chosen_payment_method = f'input#{random.choice(payment_methods)}'
                time.sleep(1)
                wait_and_click(By.CSS_SELECTOR, chosen_payment_method)
            with allure.step('Согласие с условиями и положениями'):
                wait_element(By.CSS_SELECTOR, 'input#terms').click()
            expected_price = selenium.find_element(By.CSS_SELECTOR, 'strong bdi').get_attribute('textContent')

        while True:
            with allure.step('Нажатие на кнопку "Оформить заказ"'):
                wait_and_click(By.CSS_SELECTOR, 'button#place_order')
                time.sleep(2)
                if selenium.current_url == 'https://pizzeria.skillbox.cc/checkout/' and expected_postcode != '':
                    with allure.step('Подбор специфичного почтового индекса для выбранной страны'):
                        billing_postcode.send_keys(Keys.BACK_SPACE)
                        expected_postcode = expected_postcode[:-1]
                elif expected_postcode == '':
                    pytest.skip('Для выбранной страны требуется особый индекс либо ввод валидного индекса невозможен.'
                                ' Завершение теста')
                else:
                    break

        wait_element(By.XPATH, './/h2[contains(text(), "Заказ получен")]')
        with allure.step('Проверка корректности данных в заказе'):
            actual_price = wait_element(By.CSS_SELECTOR, 'strong bdi').get_attribute('textContent')
            actual_info = wait_element(By.CSS_SELECTOR, 'section address').get_attribute('textContent')
            assert actual_price == expected_price
            assert expected_first_name in actual_info
            assert expected_last_name in actual_info
            assert expected_country in actual_info
            assert expected_address in actual_info
            if city_option:
                assert expected_city in actual_info
            if state_option:
                assert expected_state in actual_info
            if postcode_option:
                assert expected_postcode in actual_info
            assert expected_phone in actual_info
            assert expected_mail in actual_info
        pass

    @allure.title('Кейс №14. Проверка применения промокода GIVEMEHALYAVA')
    def test_case_14(self, selenium, go_to_url, wait_element, wait_and_click, wait_visible_all, hover_element):
        coupon = 'GIVEMEHALYAVA'
        go_to_url('https://pizzeria.skillbox.cc/')
        action = webdriver.ActionChains(selenium)
        with allure.step('Переход к напиткам и ожидание анимации появления'):
            action.scroll_to_element(selenium.find_element(By.XPATH, './/h2[contains(text(), "Напитки")]')).perform()
            action.scroll_to_element(selenium.find_element(
                By.XPATH, './/h1[contains(text(), "Контактная информация")]')).perform()
            time.sleep(0.5)
        with allure.step('Определение списка товаров на экране'):
            products_on_screen = wait_visible_all(
                By.XPATH,
                './/li[contains(@class, "slick-active")]')
            if len(products_on_screen) > 5:
                max_products = 5
            else:
                max_products = len(products_on_screen)
            products_to_be_added = list(range(1, len(products_on_screen) + 1))
        for products in range(randint(1, max_products)):
            with allure.step('Добавление случайного товара в корзину, удаление его из списка доступных для добавления'):
                product_num = random.choice(products_to_be_added)
                products_to_be_added.remove(product_num)
                chosen_product = products_on_screen[product_num - 1]
                hover_element(chosen_product)
                wait_and_click(By.XPATH, f'(.//li[contains(@class, "slick-active")])[{product_num}]'
                                         f'//a[contains(text(), "В корзину")]')
        time.sleep(1)
        with allure.step('Переход в корзину'):
            selenium.find_element(By.LINK_TEXT, 'Корзина').click()
        expected_summ = wait_element(By.CSS_SELECTOR, 'strong bdi').get_attribute('textContent')
        with allure.step('Ввод купона'):
            coupon_code = wait_element(By.CSS_SELECTOR, 'input#coupon_code')
            coupon_code.send_keys(coupon)
        with allure.step('Применение купона'):
            wait_and_click(By.XPATH, './/button[@name="apply_coupon"]')
            time.sleep(1)
        new_summ = wait_element(By.CSS_SELECTOR, 'strong bdi').get_attribute('textContent')
        with allure.step('Проверка корректности изменения суммы'):
            assert only_numbers(new_summ) == only_numbers(expected_summ) * 0.9
        pass

    @allure.title('Кейс №15. Проверка применения промокода DC120')
    def test_case_15(self, selenium, go_to_url, wait_element, wait_and_click, wait_visible_all, hover_element):
        coupon = 'DC120'
        go_to_url('https://pizzeria.skillbox.cc/')
        with allure.step('Переход к напиткам и ожидание анимации появления'):
            action = webdriver.ActionChains(selenium)
            action.scroll_to_element(selenium.find_element(By.XPATH, './/h2[contains(text(), "Напитки")]')).perform()
            action.scroll_to_element(selenium.find_element(
                By.XPATH, './/h1[contains(text(), "Контактная информация")]')).perform()
            time.sleep(0.5)
        with allure.step('Определение списка товаров на экране'):
            products_on_screen = wait_visible_all(
                By.XPATH,
                './/li[contains(@class, "slick-active")]')
            if len(products_on_screen) > 5:
                max_products = 5
            else:
                max_products = len(products_on_screen)
            products_to_be_added = list(range(1, len(products_on_screen) + 1))

        for products in range(randint(1, max_products)):
            with allure.step('Добавление случайного товара в корзину, удаление его из списка доступных для добавления'):
                product_num = random.choice(products_to_be_added)
                products_to_be_added.remove(product_num)
                chosen_product = products_on_screen[product_num - 1]
                hover_element(chosen_product)
                wait_and_click(By.XPATH, f'(.//li[contains(@class, "slick-active")])[{product_num}]'
                                         f'//a[contains(text(), "В корзину")]')
        time.sleep(1)
        with allure.step('Переход в корзину'):
            selenium.find_element(By.LINK_TEXT, 'Корзина').click()
        expected_summ = wait_element(By.CSS_SELECTOR, 'strong bdi').get_attribute('textContent')
        with allure.step('Ввод купона купона'):
            coupon_code = wait_element(By.CSS_SELECTOR, 'input#coupon_code')
            coupon_code.send_keys(coupon)
        with allure.step('Применение купона'):
            wait_and_click(By.XPATH, './/button[@name="apply_coupon"]')
            time.sleep(0.5)
        new_summ = wait_element(By.CSS_SELECTOR, 'strong bdi').get_attribute('textContent')
        with allure.step('Проверка уведомления о неверном купоне'):
            selenium.find_element(By.XPATH, './/li[contains(text(), "Неверный купон.")]')
        with allure.step('Проверка суммы'):
            assert only_numbers(new_summ) == only_numbers(expected_summ)
        pass

    @allure.title('Кейс №16. Перехват запроса')
    def test_case_16(self, playwright: Playwright, page: Page):
        with allure.step('Запуск браузера'):
            webkit = playwright.webkit
            browser_playwright = webkit.launch()
        with allure.step('Блокировка ссылки на активацию промокода'):
            page.route("**/?wc-ajax=apply_coupon", lambda route: route.abort())
        coupon = 'GIVEMEHALYAVA'
        with allure.step('Переход на сайт "https://pizzeria.skillbox.cc/"'):
            page.goto('https://pizzeria.skillbox.cc/', wait_until='commit')
            time.sleep(3)
        with allure.step('Добавление товара в корзину'):
            page.locator('xpath=(//*[@class="button product_type_simple add_to_cart_button ajax_add_to_cart"])[6]').click()
            time.sleep(2)
        with allure.step('Переход в корзину'):
            page.locator('xpath=//*[@class="fa fa-shopping-cart"]').click()
            time.sleep(2)
            order_text = page.locator('xpath=//*[@data-title="Сумма"]').inner_text()
            order_text_int = int(order_text.replace(',00₽', ''))
        with allure.step('Ввод купона "GIVEMEHALYAVA"'):
            page.locator('xpath=(//*[@name="coupon_code"])').fill(coupon)
            time.sleep(5)
        with allure.step('Применение купона'):
            page.locator('xpath=(//*[@name="apply_coupon"])').click()
            time.sleep(4)
        with allure.step('Проверка неизменности суммы'):
            order_text = page.locator('xpath=//*[@data-title="Сумма"]').inner_text()
            new_order_text_int = int(order_text.replace(',00₽', ''))
            assert new_order_text_int == order_text_int
        with allure.step('Закрытие браузера'):
            browser_playwright.close()

    @allure.title('Кейс №17. Проверка повторного применения промокода GIVEMEHALYAVA')
    def test_case_17(self, selenium, go_to_url, wait_element, wait_and_click, wait_visible_all, hover_element):
        go_to_url('https://pizzeria.skillbox.cc/')
        reg_base = 'RT' + (datetime.now()).strftime('%d%m%H%M%S')
        with allure.step('Переход на вкладку "Мой аккаунт"'):
            selenium.find_element(By.LINK_TEXT, 'Мой аккаунт').click()
        with allure.step('Ввод регистрационных данных'):
            wait_element(By.CLASS_NAME, 'custom-register-button').click()
            wait_element(By.CSS_SELECTOR, 'input#reg_username').send_keys(reg_base)
            wait_element(By.CSS_SELECTOR, 'input#reg_email').send_keys(reg_base + '@mail.ru')
            wait_element(By.CSS_SELECTOR, 'input#reg_password').send_keys(reg_base)
        with allure.step('Отправка регистрационных данных'):
            wait_element(By.CSS_SELECTOR, 'button[value="Зарегистрироваться"]').click()
            time.sleep(0.5)
        expected_address = 'Вязова 13'
        expected_city = 'Сайлент Хил'
        expected_state = 'Тьмы'
        expected_postcode = '131313'
        expected_phone = '+79876543210'
        expected_first_name = 'Тестер'
        expected_last_name = 'Рандомный'
        for i in range(2):
            coupon = 'GIVEMEHALYAVA'
            with allure.step('Переход на Главную'):
                go_to_url('https://pizzeria.skillbox.cc/')
            with allure.step('Переход к напиткам и ожидание анимации появления'):
                action = webdriver.ActionChains(selenium)
                action.scroll_to_element(selenium.find_element(
                    By.XPATH, './/h2[contains(text(), "Напитки")]')).perform()
                action.scroll_to_element(selenium.find_element(
                    By.XPATH, './/h1[contains(text(), "Контактная информация")]')).perform()
                time.sleep(0.5)
            with allure.step('Определение товаров на экране'):
                products_on_screen = wait_visible_all(
                    By.XPATH,
                    './/li[contains(@class, "slick-active")]')
                if len(products_on_screen) > 5:
                    max_products = 5
                else:
                    max_products = len(products_on_screen)
                products_to_be_added = list(range(1, len(products_on_screen) + 1))

            for products in range(randint(1, max_products)):
                with allure.step(
                        'Добавление случайного товара в корзину, удаление его из списка доступных для добавления'):
                    product_num = random.choice(products_to_be_added)
                    products_to_be_added.remove(product_num)
                    chosen_product = products_on_screen[product_num - 1]
                    hover_element(chosen_product)
                    wait_and_click(By.XPATH, f'(.//li[contains(@class, "slick-active")])[{product_num}]'
                                             f'//a[contains(text(), "В корзину")]')
            time.sleep(1)
            with allure.step('Переход в корзину'):
                selenium.find_element(By.LINK_TEXT, 'Корзина').click()
            expected_summ = wait_element(By.CSS_SELECTOR, 'strong bdi').get_attribute('textContent')
            with allure.step('Ввод купона'):
                coupon_code = wait_element(By.CSS_SELECTOR, 'input#coupon_code')
                coupon_code.send_keys(coupon)
            with allure.step('Применение купона'):
                wait_and_click(By.XPATH, './/button[@name="apply_coupon"]')
            time.sleep(2)
            if i == 0:
                with allure.step('Переход к оформлению заказа'):
                    wait_and_click(By.XPATH, './/a[contains(text(), "ПЕРЕЙТИ К ОПЛАТЕ")]')
                with allure.step('Заполнение формы'):
                    with allure.step('Ввод имени'):
                        first_name = wait_element(By.CSS_SELECTOR, 'input#billing_first_name')
                        first_name.clear()
                        first_name.send_keys(expected_first_name)
                    with allure.step('Ввод фамилии'):
                        surname = wait_element(By.CSS_SELECTOR, 'input#billing_last_name')
                        surname.clear()
                        surname.send_keys(expected_last_name)
                    with allure.step('Ввод адреса'):
                        billing_address = wait_element(By.CSS_SELECTOR, 'input#billing_address_1')
                        billing_address.clear()
                        billing_address.send_keys(expected_address)
                    with allure.step('Ввод названия города'):
                        billing_city = wait_element(By.CSS_SELECTOR, 'input#billing_city')
                        billing_city.clear()
                        billing_city.send_keys(expected_city)
                    with allure.step('Ввод названия области'):
                        billing_state = selenium.find_element(By.CSS_SELECTOR, 'input#billing_state')
                        billing_state.clear()
                        billing_state.send_keys(expected_state)
                    with allure.step('Ввод почтового индекса'):
                        billing_postcode = wait_element(By.CSS_SELECTOR, 'input#billing_postcode')
                        billing_postcode.clear()
                        billing_postcode.send_keys(expected_postcode)
                    with allure.step('Ввод номера телефона'):
                        billing_phone = wait_element(By.CSS_SELECTOR, 'input#billing_phone')
                        billing_phone.clear()
                        billing_phone.send_keys(expected_phone)
                    with allure.step('Ввод завтрашнего дня в поле с датой доставки'):
                        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%d.%m.%Y')
                        wait_element(By.CSS_SELECTOR, 'input#order_date').send_keys(tomorrow)
                    with allure.step('Случайный выбор метода оплаты'):
                        payment_methods = ['payment_method_bacs', 'payment_method_cod']
                        chosen_payment_method = f'input#{random.choice(payment_methods)}'
                        time.sleep(1)
                        wait_and_click(By.CSS_SELECTOR, chosen_payment_method)
                    with allure.step('Согласие с условиями и положениями'):
                        wait_element(By.CSS_SELECTOR, 'input#terms').click()

                with allure.step('Нажатие на кнопку "Оформить заказ"'):
                    wait_and_click(By.CSS_SELECTOR, 'button#place_order')
                    time.sleep(2)

        new_summ = wait_element(By.CSS_SELECTOR, 'strong bdi').get_attribute('textContent')
        with allure.step('Проверка суммы'):
            assert only_numbers(new_summ) == only_numbers(expected_summ)
        pass

    @allure.title('Кейс №18. Проверка формы бонусной программы')
    def test_case_18(self, selenium, go_to_url, wait_element, wait_and_click, hover_element):
        go_to_url('https://pizzeria.skillbox.cc/')
        with allure.step('Переход в раздел "Бонусная программа"'):
            wait_and_click(By.LINK_TEXT, 'Бонусная программа')
        with allure.step('Заполнение формы'):
            expected_name = 'RandTester0'
            expected_phone = '+79876543210'
            bonus_username = selenium.find_element(By.CSS_SELECTOR, 'input#bonus_username')
            bonus_username.send_keys(expected_name)
            bonus_phone = selenium.find_element(By.CSS_SELECTOR, 'input#bonus_phone')
            bonus_phone.send_keys(expected_phone)
        with allure.step('Проверка корректности ввода данных'):
            assert bonus_username.get_attribute('value') == expected_name
            assert bonus_phone.get_attribute('value') == expected_phone
        with allure.step('Отправка данных'):
            wait_and_click(By.XPATH, './/button[text()="Оформить карту"]')
        with allure.step('Ожидание появления уведодмления'):
            WebDriverWait(selenium, 10).until(EC.alert_is_present())
        with allure.step('Закрытие уведомления'):
            selenium.switch_to.alert.accept()
        with allure.step('Ожидание завершения оформления карты'):
            wait_element(By.XPATH, './/h3[text()="Ваша карта оформлена!"]')
        pass
