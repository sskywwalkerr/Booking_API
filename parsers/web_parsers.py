# Функции парсинга конкретных веб-страниц
import requests
import json

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "bx-ajax": "True"
}


def get_page(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    # Проверяем статус ответа
    response.raise_for_status()

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(response.text)


def get_json(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    try:
        response.raise_for_status()
        data = response.json()
    except ValueError as e:
        print("Error loading JSON: " + str(e))
        print("Response content: " + response.text)
    else:
        with open("result.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    #get_page(url="https://www.lamoda.ru/c/15/shoes-women/")
    get_json(url="https://www.lamoda.ru/api/v1/catalog/discovery")


if __name__ == '__main__':
    main()
