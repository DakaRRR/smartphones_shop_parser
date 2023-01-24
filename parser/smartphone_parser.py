from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from typing import List, Dict
import json
import logging
import time


logging.basicConfig(level=logging.INFO, filename='smartphones_parser.log', encoding='utf-8')


def configure_chrome_webdriver() -> webdriver:
    """Вовращает Хромовский webdriver"""
    options = Options()
    options.add_argument("--disable-infobars")
    return webdriver.Chrome(options=options)


def extract_smartphone_elements(browser: webdriver, smartphones_url: str):
    """
       Извлекает все элементы со смартфонами из заданного url с помощью selenium webdriver
       и css selector'а класса - .bx_catalog_item_container"
       """
    try:
        browser.get(url=smartphones_url)
        elements = browser.find_elements(By.CSS_SELECTOR, ".bx_catalog_item_container")
        logging.info(f'Элементы со всеми смартфонами на этой странице были извлечены. Их количество - {len(elements)}')
        return elements
    except Exception as e:
        logging.error(f'Ошибка при загрузке элементов: {e}')


def create_smartphone_list(elements: List[webdriver.remote.webelement.WebElement], smartphones: List[Dict]) -> List[Dict]:
    """
        Создает список смартфонов из заданных элементов. Находит все через data-product
        из которого вытаскивает все необходимые данные и записывает в smartphones

        Параметры:
        elements (list) : список элементов webdriver, представляющих смартфоны
        smartphones(list(dict)): список куда записываются данные

        Возвращает:
        smartphones : обновленный список с новыми данными
        """
    for element in elements:
        try:
            data_product = element.get_attribute("data-product")
            data_product_dict = json.loads(data_product)
            name = data_product_dict["item_name"].encode('utf-8', 'unicode-escape').decode() #декодим т.к. текст на русском
            smartphones.append({
                "name": name,
                "articul": data_product_dict["item_id"],
                "price": data_product_dict["price"],
                "memory-size": name.split(",")[1].strip()
            })
        except Exception as e:
            logging.error(f'Ошибка при создании словаря смартфонов: {e}')

    logging.info(f'Данные о смарфтонах со всех элементов записались их количество - {len(smartphones)}')
    return smartphones


def save_smartphones_to_json(data: List[Dict], filename: str) -> None:
    """Создает json файл из значений data и с названием filename"""
    try:
        with open(f'{filename}.json', "w", encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)
        logging.info(f'Данные успешно записались в {filename}.json')
    except Exception as e:
        logging.error(f'Ошибка при сохранении json файла: {e}')


def get_number_of_pages(browser: webdriver) -> int:
    """Возвращает число страниц текущей веб-страницы"""
    try:
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        pagination_div = soup.find('div', class_="bx-pagination-container")
        pagination_li = pagination_div.find_all('li')
        last_page_link = pagination_li[-2].find('a')['href'] # -2, т.к. предпоследняя кнопка имеет значение с общим кол-вом страниц
        last_page_number = int(last_page_link.split("PAGEN_1=")[-1])
        logging.info(f'Страниц которых надо пропарсить - {last_page_number}')
        return last_page_number
    except Exception as e:
        logging.error(f'Ошибка при получении количества страниц: {e}')
        return 14  # текущее количество страниц смартфонов на сайте


def get_next_page_url(browser: webdriver) -> str:
    """Возвращает URL следующей страницы"""
    try:
        next_page_button = browser.find_element(By.CSS_SELECTOR, '.bx-pag-next')
        next_page_button.click()
        smartphones_url = browser.current_url
        return smartphones_url
    except Exception as e:
        logging.error(f'Ошибка при переходе на следующую страницу: {e}')


def smartphones_parser_start() -> None:
    browser = configure_chrome_webdriver()
    smartphones_url = "https://shop.kz/smartfony/filter/astana-is-v_nalichii-or-ojidaem-or-dostavim/apply/"
    browser.get(url=smartphones_url)
    last_page_number = get_number_of_pages(browser)
    smartphones_json = []
    # проходимся по всем страницам и по очередности запускаем функции
    for page_number in range(1, last_page_number + 1):
        try:
            logging.info(f'{page_number} страница понеслась.......')
            time.sleep(15)
            elements = extract_smartphone_elements(browser, smartphones_url)
            smartphones_json = create_smartphone_list(elements, smartphones_json)
            smartphones_url = get_next_page_url(browser)
        except Exception as e:
            logging.error(f'Ошибка при парсинге {page_number} страницы: {e}')

    save_smartphones_to_json(smartphones_json, "smartphones")


def main():
    smartphones_parser_start()


if __name__ == "__main__":
    main()
