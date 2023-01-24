**Тестовое задание №1**

**Первая часть**

Необходимо написать парсер для сайта *https:/[/shop.kz* в ](https://shop.kz)*разделе **«***с[мартфоны***»** ](https://shop.kz/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply)*для извлечения данных обо всех смартфонах с их характеристиками. Данные должны быть в формате json и соответствовать примеру:

{![](Aspose.Words.0ff407c6-1b99-472e-8df4-d68085e19268.001.png)

"name": "Apple iPhone 11 (2020), 64Gb, Green (MHDG3)", "articul": "151840",

"price": "329900",

"memory-size": "64 Гб"

}

**Описание ключей**



|**Ключ**|**Описание**|
| - | - |
|name|Название смартфона|
|articul|Артикул в магазине|
|price|Цена смартфона на данный момент|
|memory-size|Объем встроенной памяти|
Все данные следует сохранить в файл smartphones.json. **Вторая часть**

Необходимо написать API используя один из трех фреймворков (*Bottle, Flask, FastAPI*), и реализовать эндпоинт ***«**/smartphones**»*** с параметром **«***price**»*** который выведет все смартфоны с указанной ценой (данные необходимо взять из файла smartphones.json).

Также необходимо обернуть сервис в докер контейнер (Dockerfile, docker-compose).

Пример![](Aspose.Words.0ff407c6-1b99-472e-8df4-d68085e19268.002.png)

Запрос: http://localhost:8000/smartphones?price=329900 Ответ:

[

{

"name": "Apple iPhone 11 (2020), 64Gb, Green (MHDG3)", "articul": "151840",

"price": "329900",

"memory-size": "64 Гб"

}, {

"name": "Apple iPhone 11 (2020), 64Gb, Red (MHDD3)", "articul": "152229",

"price": "329900",

"memory-size": "64 Гб"

}

]

В качестве решения можно отправить ссылку на репозиторий или zip архив проекта.

