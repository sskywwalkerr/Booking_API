from selenium import webdriver
from bs4 import BeautifulSoup

#  Функции  парсинга  конкретных  веб-страниц


def parse_product_page(url: str):
    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Извлечение  данных  с  веб-страницы
    title = soup.find('h1', class_='product-title').text.strip()
    price = soup.find('span', class_='product-price').text.strip()

    driver.quit()
    return {"title": title, "price": price}