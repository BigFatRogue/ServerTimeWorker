import sqlite3
import os, shutil, sys, zipfile
from werkzeug.security import generate_password_hash
from server.my_sitting import DATABASE, PROJECT_ROOT


class DataBase:
    def __init__(self):
        self.conn = None
        self.cur = None

    def connection_db(self):
        self.conn = sqlite3.connect(DATABASE)
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()
        self.conn = None


class Users(DataBase):
    def create_db(self: str) -> None:
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

        if not os.path.exists(os.path.join(PROJECT_ROOT, 'database', 'users')):
            os.mkdir(os.path.join(PROJECT_ROOT, 'database', 'users'))

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
            self.close()
            return False, None
        else:
            # Создание пользователя и личного календаря
            self.cur.execute(f"""INSERT INTO user (username, password, filepath) VALUES(?, ?, ?)""",
                             (username, password, 'tmp'))

            user_id = self.cur.execute(f"SELECT id FROM user WHERE username = '{username}'").fetchone()[0]

            filepath = os.path.join(PROJECT_ROOT, 'database', 'users', f'user_{user_id}.json')
            self.cur.execute(f"UPDATE user SET filepath = '{filepath}' WHERE username = '{username}'")

            if not os.path.exists(filepath):
                shutil.copy(os.path.join(PROJECT_ROOT, 'resources', 'standart_calendar_json_2024.json'), filepath)

            self.close()
            return True, user_id

    def get_user_username(self, username: str, close = True) -> tuple:
        """
        :param username:
        :param password:
        :return: status response: bool, message or filepath: str
        """
        self.create_db()

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

        user_db = self.cur.execute(f"SELECT * FROM user WHERE id = '{user_id}'").fetchone()

        if user_db:
            return True, user_db
        return False, None

    def get_all_users(self) -> dict:
        column = ('id', 'username')
        self.create_db()

        res = self.cur.execute(f"SELECT {', '.join(column)} FROM user").fetchall()
        self.close()

        return {'users': res, 'column': column}

    def del_user(self, user_id: str) -> None:
        self.connection_db()
        self.cur.execute(f"DELETE FROM user WHERE id = '{user_id}'")
        self.close()

        os.remove(os.path.join(PROJECT_ROOT, 'database', 'users', f'user_{user_id}.json'))

    def update_password(self, user_id: str, new_password: str) -> None:
        self.connection_db()
        self.cur.execute(f"UPDATE user SET password = '{generate_password_hash(new_password) }' WHERE id = '{user_id}'")
        self.close()

    def update_username(self, user_id: str, username: str) -> None:
        self.connection_db()
        self.cur.execute(f"UPDATE user SET username = '{username}' WHERE id = '{user_id}'")
        self.close()

    def del_db(self) -> None:
        if self.conn:
            self.close()
        if os.path.exists(DATABASE):
            os.remove(DATABASE)
        if os.path.exists(os.path.join(f'{PROJECT_ROOT}', 'database', 'users')):
            shutil.rmtree(os.path.join(f'{PROJECT_ROOT}', 'database', 'users'))


class Admin(DataBase):
    def create_db(self: str) -> None:
        if self.conn is None:
            self.connection_db()

        self.cur.execute(f'''
        CREATE TABLE IF NOT EXISTS admin (
        id INTEGER,
        username TEXT NOT NULL,
        password TEXT NOT NULL
        )
        ''')

    def get_set_admin(self, username: str, password: str) -> tuple:
        """
        Регистрация нового пользователя
        :param username:
        :param password:
        :return:
        """
        self.create_db()

        res = self.cur.execute(f"SELECT * FROM admin").fetchone()
        if not res:
            self.cur.execute(f"INSERT INTO admin (id, username, password) VALUES(?, ?, ?)", (1000, username, password))
            self.close()
            return False, None
        else:
            self.close()
            return True, res

    def get_user_id(self, user_id: str) -> tuple:
        """
        :param username:
        :param password:
        :return: status response: bool, message or filepath: str
        """
        self.create_db()

        user_db = self.cur.execute(f"SELECT * FROM admin WHERE id = '{user_id}'").fetchone()

        if user_db:
            return True, user_db
        return False, None

    def del_admin(self):
        self.create_db()
        self.cur.execute("DELETE FROM admin")
        self.close()


def load_zipdb() -> str:
    zipname = 'database_unload.zip'
    fullpath = os.path.join(PROJECT_ROOT, zipname)

    if os.path.exists(fullpath):
        os.remove(fullpath)

    with zipfile.ZipFile(fullpath, 'w') as file:
        file.write(os.path.join(PROJECT_ROOT, 'database', 'db.db'))
        for user_js in os.listdir(os.path.join(PROJECT_ROOT, 'database', 'users')):
            file.write(os.path.join(PROJECT_ROOT, 'database', 'users', user_js))

    return zipname


def upload_zipdb():
    with zipfile.ZipFile(os.path.join(PROJECT_ROOT, 'database_upload.zip'), 'r') as file:
        file.extractall(os.path.join(PROJECT_ROOT, 'extract_upload'))

    for roots, folders, files in os.walk(os.path.join(PROJECT_ROOT, 'extract_upload')):
        for file in files:
            if file == 'db.db':
                path_db = os.path.join(PROJECT_ROOT, 'database', 'db.db')
                os.remove(path_db)
                shutil.copy(os.path.join(roots, file), path_db)

        for folder in folders:
            if folder == 'users':
                path_users = os.path.join(PROJECT_ROOT, 'database', 'users')
                shutil.rmtree(path_users)
                shutil.copytree(os.path.join(roots, folder), path_users)


if __name__ == '__main__':
    db = Users()
    # db.del_db()
    print(db.get_user_username("pavel"))
    # db.update_password_user('2', '444')
    # print(db.get_all_users())
    # res = db.get_user_username('user2')
    # print(res)
    # db_a = Admin()
    # db_a.del_table()
    # print(db_a.get_admin())
    #

