from config import app, bot, con, cur
from fastapi.responses import JSONResponse
from .db import DataBase
import json

db = DataBase(cur, con)

@app.get('/id')
async def get_id_rezult(request_id: int):
    id_dbr = db.search_rezult_for_id(request_id)
    if id_dbr is None:
        return {'ERROR': 'По вашему id не найдено записей'}
    return JSONResponse({
        'request_id': request_id,
        'rezult': json.loads(id_dbr[0])
        })