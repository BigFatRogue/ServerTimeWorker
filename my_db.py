from my_sitting import DATABASE
import sqlite3
import os
import shutil


class UsersDB:
    def __init__(self):
        self.table = 'user'
        self.conn = None

    def create_db(self) -> None:
        if self.conn is None:
            self.connection_db()

        self.cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.table} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        filepath TEXT NOT NULL
        )
        ''')
        self.close()

        if not os.path.exists('users'):
            os.mkdir('users')

    def connection_db(self):
        self.conn = sqlite3.connect(DATABASE)
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()
        self.conn = None

    def del_db(self) -> None:
        if self.conn:
            self.close()
        if os.path.exists(DATABASE):
            os.remove(DATABASE)
        if os.path.exists('users'):
            shutil.rmtree('users')

    def set_users(self, username: str, password: str) -> tuple:
        """
        Регистрация нового пользователя
        :param username:
        :param password:
        :return:
        """
        self.create_db()
        if self.conn is None:
            self.connection_db()

        check = self.cur.execute(f"SELECT username FROM {self.table} WHERE username = '{username}'").fetchall()
        print(check)
        if check:
            return False, 'Такой пользователь уже зарегистрирован'
        else:
            user_id = len(self.cur.execute(f"SELECT username FROM {self.table}").fetchall()) + 1
            filepath = f'users/user_{user_id}.json'

            if not os.path.exists(filepath):
                shutil.copy('standart_calendar_json.json', filepath)

                self.cur.execute(f"""INSERT INTO {self.table} (username, password, filepath) VALUES(?, ?, ?)""",
                                 (username, password, filepath))
            self.close()
            return True, f'Новый пользователь {username} зарегистрирован'

    def get_user(self, username: str, password: str) -> tuple:
        """
        :param username:
        :param password:
        :return: status response: bool, message or filepath: str
        """
        self.create_db()
        if self.conn is None:
            self.connection_db()

        res = self.cur.execute(f"SELECT * FROM {self.table} WHERE username = '{username}'").fetchall()
        if res:
            user_id, user_db, password_db, filepath = res[0]
            if password != password_db:
                return False, None, 'Неверный пароль'
            return True, user_id, filepath
        else:
            return False, None, 'Такого пользователя нет'

    @property
    def get_all_users(self):
        if self.conn is None:
            self.connection_db()
        return self.cur.execute(f"SELECT * FROM {self.table}").fetchall()

    def update_users(self, username: str, password=None, filepath=None) -> None:
        pass


if __name__ == '__main__':
    db = UsersDB()
    # db.create_db()
    # res = db.get_all_users
    # print(res)
    db.del_db()
    # print(db.get_users('pavel', '13'))
