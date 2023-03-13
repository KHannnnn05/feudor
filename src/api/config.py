from fastapi import FastAPI
from parser.bot import ParseBot
import sqlite3

app = FastAPI()

with sqlite3.connect('db.sqlite3') as con:
    cur = con.cursor()

bot = ParseBot()