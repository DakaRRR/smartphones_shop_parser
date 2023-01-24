from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from typing import List, Dict
import json
import logging


def setup_logger():
    logging.basicConfig(level=logging.INFO, filename='smartphones_parser.log')


def configure_webdriver() -> webdriver:
    options = Options()
    options.add_argument("--disable-infobars")
    return webdriver.Chrome(options=options)


def extract_smartphone_elements(browser: webdriver, smartphones_url: str) -> List[
    webdriver.remote.webelement.WebElement]:
    try:
        browser.get(url=smartphones_url)
        elements = browser.find_elements(By.CSS_SELECTOR, ".bx_catalog_item_container")
        return elements
    except Exception as e:
        logging.error(f'Ошибка при загрузке элементов: {e}')


def create_smartphone_list(elements: List[webdriver.remote.webelement.WebElement]) -> List[Dict]:
    smartphones = []
    for element in elements:
        try:
            data_product = element.get_attribute("data-product")
            data_product_dict = json.loads(data_product)
            name = data_product_dict["item_name"].encode('utf-8', 'unicode-escape').decode()
            smartphones.append({
                "name": name,
                "articul": data_product_dict["item_id"],
                "price": data_product_dict["price"],
                "memory-size": name.split(",")[1].strip()
            })
        except Exception as e:
            logging.error(f'Ошибка при создании словаря смартфонов: {e}')
    return smartphones


def save_smartphones_to_json(smartphones: List[Dict], filename: str) -> None:
    try:
        with open(f'{filename}.json', "w", encoding='utf-8') as file:
            json.dump(smartphones, file, ensure_ascii=False)
    except Exception as e:
        logging.error(f'Ошибка при сохрании json файла: {e}')


def get_number_of_pages(browser: webdriver) -> int:
    try:
        pages = browser.find_elements(By.CSS_SELECTOR, "ul li")
        last_page_link = pages[-2].find_element(By.TAG_NAME, ('a')).get_attribute('href')
        last_page_number = int(last_page_link.split("PAGEN_1=")[-1])
        return last_page_number
    except Exception as e:
        logging.error(f'Ошибка при получении количества страниц: {e}')
        return 0  # текущее количество страниц смартфонов на сайте


def get_next_page_url(browser: webdriver) -> str:
    try:
        next_page_button = browser.find_element(By.CSS_SELECTOR, '.bx-pag-next')
        next_page_button.click()
        smartphones_url = browser.current_url
        return smartphones_url
    except Exception as e:
        logging.error(f'Ошибка при перехода на следующуюю страницу: {e}')


def start_smartphones_shop_parser(smartphones_url: str):
    setup_logger()
    browser = configure_webdriver()
    browser.get(url=smartphones_url)
    number_of_pages = get_number_of_pages(browser)
    print(number_of_pages)
    smartphones_json = []
    for i in range(1, 2):
        try:
            elements = extract_smartphone_elements(browser, smartphones_url)
            smartphones_json.append(create_smartphone_list(elements))
            smartphones_url = get_next_page_url(browser)
            print(i)
        except Exception as e:
            logging.error(f'Ошибка при парсинге {i} страницы: {e}')

    save_smartphones_to_json(smartphones_json, "smartphones")
