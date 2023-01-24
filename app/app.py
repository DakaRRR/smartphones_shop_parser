from fastapi import FastAPI, Query
import json

fastapi_app = FastAPI()


def get_smartphones_json(filepath:str):
    """Читаем данные с файла smartphones json"""
    with open(filepath, "r", encoding='utf-8') as file:
        smartphones = json.load(file)
    return smartphones


@fastapi_app.get("/smartphones")
def get_smartphones_by_price(price: int = Query(..., gt=0)):
    """Эндпоинт по поиску смартфона по цене"""
    smartphones = get_smartphones_json("parser/smartphones.json")
    smartphones_filter_by_price = [s for s in smartphones if s["price"] == price]
    return smartphones_filter_by_price
