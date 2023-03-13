import json

class DataBase():

    def __init__(self, cur, con) -> None: 
        self.cur = cur
        self.con = con
        cur.execute("""
        CREATE TABLE IF NOT EXISTS requests
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            car_number TEXT,
            request_date TEXT,
            rezult TEXT
        );""")
        con.commit()


    def add_request(self, car_number, request_date, rezult) -> int:
        id = self.cur.execute("INSERT INTO requests (car_number, request_date, rezult) VALUES (?, ?, ?) RETURNING id;", 
                            (car_number, request_date, rezult, )).fetchone()

        self.con.commit()

        return int(id[0])
    

    def search_rezult(self, car_number):
        rezult = self.cur.execute("SELECT * FROM requests WHERE (car_number == ?);", (car_number, )).fetchone()

        if rezult is None:
            return None
        else: 
            return rezult

    def search_rezult_for_id(self, car_id):
        id_rezult = self.cur.execute(f"SELECT rezult FROM requests WHERE (id == ?);", (int(car_id), )).fetchone()
        return id_rezult