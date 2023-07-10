# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import selenium.common.exceptions as exceptions


URL = 'https://www.saucedemo.com/'
LOGIN = 'standard_user'
PASSWORD = 'secret_sauce'


def get_driver():
    """
    Функция, создающая и настраивающая экземпляр вебдрайвера.

    :return: Экземпляр вебдрайвера
    """
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,800")
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                              options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(8)
    return driver


def open_page(driver, url: str):
    """
    Функция, открывающая страницу по указанному URL.

    :param driver: Экземпляр вебдрайвера
    :param url: URL-ссылка на целевую страницу
    """
    driver.get(url)


def auth(driver, login: str, password: str):
    """
    Функция, проводящая аутентификацию с использованием переданных логина и пароля.
    Заполняет input-элементы и нажимает кнопку отправки.

    :param driver: Экземпляр вебдрайвера
    :param login: Значение логина для проведения аутентификации
    :param password: Значение пароля для проведения аутентификации
    """
    element_send_keys(driver, selector="username", content=login)
    element_send_keys(driver, selector="password", content=password)
    element_click(driver, selector="login-button")


def element_send_keys(driver, selector: str, content: str):
    """
    Функция, заполняющая указанные input-элементы. Получает элементы с текущей страницы,
    очищает их и заполняет указанным текстом.

    :param driver: Экземпляр вебдрайвера
    :param selector: Идентификатор элемента (значение атрибута "data-test")
    :param content: Значение, которое должно появиться в элементе
    """
    element = get_element_by_selector(driver, selector)
    element.clear()
    element.send_keys(content)


def element_click(driver, selector: str):
    """
    Функция, имитирующая клик на элемент.

    :param driver: Экземпляр вебдрайвера
    :param selector: Идентификатор элемента (значение атрибута "data-test")
    """
    element = get_element_by_selector(driver, selector)
    element.click()


def get_element_by_selector(driver, selector: str):
    """
    Функция, выбирающая элемент по его идентификатору. На текущей странице в соответствии
    с указанным значением атрибута "data-test" выбирает и возвращает элемент страницы.

    :param driver: Экземпляр вебдрайвера
    :param selector: Идентификатор элемента (значение атрибута "data-test")
    :return: Экземпляр элемента страницы
    """
    return driver.find_element(By.CSS_SELECTOR, f"[data-test='{selector}']")


def auth_is_successful(driver):
    """
    Функция, определяющая успешность прохождения аутентификации. В случае успешного прохождения
    выводит сообщение "Success". В случае непрохождения аутентификации вызывает исключение,
    за счёт которого прохождение теста заканчивается с кодом отличным от "0" (Failed).

    :param driver: Экземпляр вебдрайвера
    """
    # уменьшаем время ожидания для оптимизации
    driver.implicitly_wait(0)
    # пробуем получить кнопку "Login" с текущей страницы
    try:
        get_element_by_selector(driver, "login-button")
    # если получить элемент не получается, значит аутентификация пройдена и мы уже на другой странице
    except exceptions.NoSuchElementException:
        print("Success")
    # если элемент был получен, значит мы всё ещё на странице аутентификации
    else:
        raise Exception("Unsuccessful authentication!")


# инициализация драйвера
driver = get_driver()
# открытие страницы авторизации
open_page(driver, url=URL)
# проведение авторизации
auth(driver, login=LOGIN, password=PASSWORD)
# проверка успешности авторизации
auth_is_successful(driver)
# закрытие драйвера
driver.quit()
