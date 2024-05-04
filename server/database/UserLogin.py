from server.database.db import Users
from flask_login import UserMixin


class UserLogin(UserMixin):
    def from_db(self, user_id, db: Users):
        _, self.__user = db.get_user_id(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user[0])

    def get_username(self):
        return str(self.__user[1])
