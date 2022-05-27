import sqlite3

class Database:
    def __init__(self):
        self.sqlite = sqlite3.connect('data.db')
        self.db = self.sqlite.cursor()

    def installetion(self):
        self.db.execute("""CREATE TABLE users (
                    userid integer,
                    balls integer,
                    admin boolean
                    )""")

        self.sqlite.commit()

    def createuser(self, vk_id):
        self.db.execute(f"""INSERT INTO users VALUES ({vk_id}, 0, False)""")
        self.sqlite.commit()

    def getinfo(self, vk_id):
        res = self.db.execute(f"""SELECT * FROM users WHERE userid = {vk_id}""")
        return res.fetchall()

    def setbal(self, vk_id, new_value):
        self.db.execute(f"""UPDATE users SET balls = {new_value} WHERE userid = {vk_id}""")
        self.sqlite.commit()

    def switchRights(self, vk_id):
        res = self.db.execute(f"""SELECT admin FROM users WHERE userid = {vk_id}""").fetchall()[0][0]
        if bool(res):
            self.db.execute(f"""UPDATE users SET admin={False} WHERE userid = {vk_id}""")
            self.sqlite.commit()
            return 'пользователь'
        else:
            self.db.execute(f"""UPDATE users SET admin={True} WHERE userid = {vk_id}""")
            self.sqlite.commit()
            return 'админ'

db = Database()