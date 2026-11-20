import sqlite3


class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

        sql = """CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    phone TEXT,
                    diagnosis TEXT,
                    cost REAL
                )"""
        self.cur.execute(sql)
        self.con.commit()

    def insert(self, name, age, phone, diagnosis, cost):
        self.cur.execute(
            "INSERT INTO patients (name, age, phone, diagnosis, cost) VALUES (?,?,?,?,?)",
            (name, age, phone, diagnosis, cost)
        )
        self.con.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM patients")
        rows = self.cur.fetchall()
        return rows

    def remove(self, id):
        self.cur.execute("DELETE FROM patients WHERE id=?", (id,))
        self.con.commit()

    def update(self, id, name, age, phone, diagnosis, cost):
        self.cur.execute(
            "UPDATE patients SET name=?, age=?, phone=?, diagnosis=?, cost=? WHERE id=?",
            (name, age, phone, diagnosis, cost, id)
        )
        self.con.commit()