from fastapi import FastAPI, Query
import json
import os


fastapi_app = FastAPI()


def get_smartphones_json(filepath: str):
    """Читаем данные с файла smartphones json"""
    base_path = os.path.dirname(os.path.abspath(__file__))
    parser_path = os.path.join(base_path, '..', 'parser')
    full_path = os.path.join(parser_path, filepath)
    with open(full_path, "r", encoding='utf-8') as file:
        smartphones = json.load(file)
    return smartphones


@fastapi_app.get("/smartphones")
def get_smartphones_by_price(price: int = Query(..., gt=0)):
    """Эндпоинт по поиску смартфона по цене"""
    smartphones = get_smartphones_json("smartphones.json")
    smartphones_filter_by_price = [s for s in smartphones if s["price"] == price]
    return smartphones_filter_by_price
