from config import app, bot, con, cur
from fastapi.responses import JSONResponse
from .db import DataBase
import datetime
import json

db = DataBase(cur, con)

@app.post('/search')
async def post_index(gosnumber: str):
    '''Валидация полученного номера'''
    if len(gosnumber) != 9:
        return JSONResponse({'ERROR': 'Отправьте корректный номер!'})
    now = datetime.datetime.now()
    '''Ищем номер в бд, если находим, то отрпавляем его с id'''
    if db.search_rezult(gosnumber) is not None:
        dbr = db.search_rezult(gosnumber)
        return JSONResponse({
                        'request_id': dbr[0], 
                        'rezult': json.loads((dbr[-1]))
                        })
    rezult = bot.parse(car_number=gosnumber)
    rez_id = db.add_request(car_number=str(gosnumber), 
                            request_date=str(now),
                            rezult=json.dumps(rezult, ensure_ascii=False))
    return JSONResponse({
                        'request_id': rez_id, 
                        'rezult': rezult
                        })