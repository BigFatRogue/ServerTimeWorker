import sqlite3
import os, shutil, sys
from server.my_sitting import DATABASE, PROJECT_ROOT


class UsersDB:
    def __init__(self):
        self.conn = None

    def create_db(self) -> None:
        if self.conn is None:
            self.connection_db()

        self.cur.execute(f'''
        CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        filepath TEXT NOT NULL
        )
        ''')
        self.close()

        if not os.path.exists(os.path.join(PROJECT_ROOT, 'users')):
            os.mkdir(os.path.join(PROJECT_ROOT, 'users'))

    def connection_db(self):
        self.conn = sqlite3.connect(DATABASE)
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()
        self.conn = None

    def set_users(self, username: str, password: str) -> tuple:
        """
        Регистрация нового пользователя
        :param username:
        :param password:
        :return:
        """
        self.create_db()

        flag, user_db = self.get_user_username(username, close=False)
        if flag:
            # Пользователь существует
            return False, None
        else:
            # Создание пользователя и личного календаря
            new_user_id = self.cur.execute(f"SELECT COUNT(username) FROM user").fetchone()[0] + 1
            filepath = fr'{PROJECT_ROOT}/users/user_{new_user_id}.json'

            if not os.path.exists(filepath):
                shutil.copy(rf'{PROJECT_ROOT}/resources/standart_calendar_json_2024.json', filepath)

                self.cur.execute(f"""INSERT INTO user (username, password, filepath) VALUES(?, ?, ?)""",
                                     (username, password, filepath))
            self.close()
            return True, new_user_id

    def get_user_username(self, username: str, close=True) -> tuple:
        """
        :param username:
        :param password:
        :return: status response: bool, message or filepath: str
        """
        self.create_db()
        if self.conn is None:
            self.connection_db()

        user_db = self.cur.execute(f"SELECT * FROM user WHERE username = '{username}'").fetchone()
        if close:
            self.close()
        if user_db:
            return True, user_db
        return False, None

    def get_user_id(self, user_id: str) -> tuple:
        """
        :param username:
        :param password:
        :return: status response: bool, message or filepath: str
        """
        self.create_db()
        if self.conn is None:
            self.connection_db()

        user_db = self.cur.execute(f"SELECT * FROM user WHERE id = '{user_id}'").fetchone()

        if user_db:
            return True, user_db
        return False, None

    def del_db(self) -> None:
        if self.conn:
            self.close()
        if os.path.exists('db.db'):
            os.remove('db.db')
        if os.path.exists('users'):
            shutil.rmtree('users')


if __name__ == '__main__':
    db = UsersDB()
    # res = db.set_users('user2', '123')
    res = db.get_user_username('user2')
    print(res)
