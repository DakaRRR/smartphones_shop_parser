from bs4 import BeautifulSoup
from typing import List, Dict
import json
import requests
import logging


logging.basicConfig(level=logging.INFO, filename='smartphones_parser.log', encoding='utf-8')


def configure_bs_html(url: str) -> BeautifulSoup:
    """Вовзрщает объект BeautifulSoup c заданной ссылкой url через request"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.82 Safari/537.36'}
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup


def extract_smartphone_data(soup: BeautifulSoup) -> List[Dict]:
    """Извлекает соответствующие данные для каждого смартфона из заданного объекта BeautifulSoup soup и возвращает
        данные в виде списка словарей smartphones."""
    smartphones = []
    try:
        elements = soup.select('.bx_catalog_item_container')
        for element in elements:
            data = json.loads(element['data-product'])
            smartphones.append({
                'name': data["item_name"],
                'article': data["item_id"],
                'price': data['price'],
                'memory-size': data["item_name"].split(",")[1].strip()
            })
        logging.info(f'{len(smartphones)} - смартфонов были пропарсены.')
        return smartphones
    except Exception as e:
        logging.error(f'Ошибка при парсинге элементов со смартфонами: {e}')


def get_number_of_pages(url: str) -> int:
    """Возвращает число страниц текущей веб-страницы"""
    try:
        soup = configure_bs_html(url)
        pagination_div = soup.find('div', class_="bx-pagination-container")
        pagination_li = pagination_div.find_all('li')
        last_page_link = pagination_li[-2].find('a')[
            'href']  # -2, т.к. предпоследняя кнопка имеет значение с общим кол-вом страниц
        last_page_number = int(last_page_link.split("PAGEN_1=")[-1])
        logging.info(f'Страниц которых надо пропарсить - {last_page_number}')
        return last_page_number
    except Exception as e:
        logging.error(f'Ошибка при получении количества страниц: {e}')
        return 14  # текущее количество страниц смартфонов на сайте


def save_smartphones_to_json(data: List[Dict], filename: str) -> None:
    """Создает json файл из значений data и с названием filename"""
    try:
        with open(f'{filename}.json', "w", encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)
        logging.info(f'Данные успешно записались в {filename}.json')
    except Exception as e:
        logging.error(f'Ошибка при сохранении json файла: {e}')


def smartphones_parser_start() -> None:
    smartphones_url = "https://shop.kz/smartfony/filter/astana-is-v_nalichii-or-ojidaem-or-dostavim/apply/"
    smartphones = []  # словарь для записи данных
    number_of_pages = get_number_of_pages(smartphones_url)  # получение кол-ва страниц со смартфонами
    for page_number in range(1, number_of_pages + 1):
        try:
            page_url = f'{smartphones_url}?PAGEN_1={page_number}'  # создаем str являвющейся ссылкой на страницу
            logging.info(f'{page_number} страница понеслась....... Ссылка: {page_url}')
            soup = configure_bs_html(page_url)  #создаем объект Beatifulsoup из ссылки которые мы получили
            smartphones.extend(extract_smartphone_data(soup))  # записываем данные в словарь
        except Exception as e:
            logging.error(f'Ошибка при парсинге {page_number} страницы: {e}')

    logging.info(f'Данные о смарфтонах со всех элементов записались их количество - {len(smartphones)}')

    save_smartphones_to_json(smartphones, "smartphones")


def main():
    smartphones_parser_start()


if __name__ == "__main__":
    main()
