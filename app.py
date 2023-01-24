from fastapi import FastAPI, Query
from typing import List, Dict
import json

app = FastAPI()


@app.get("/smartphones")
def get_smartphones(price: int = Query(..., gt=0)):
    with open("smartphones.json", "r", encoding='utf-8') as file:
        smartphones = json.load(file)
        print(smartphones)
    result = [s for s in smartphones[[]] if s["price"] == price]
    return result