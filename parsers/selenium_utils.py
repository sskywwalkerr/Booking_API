from selenium import webdriver
from selenium.webdriver.chrome.options import Options


#  Вспомогательные  функции  для  Selenium


def create_headless_driver():
    options = Options()
    options.add_argument('--headless=new')  #  Headless  браузер
    options.add_argument('--no-sandbox')  #  Для  Docker
    driver = webdriver.Chrome(options=options)
    return driver