import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# таблица пользователя
class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'


    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    publications = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    friends = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    potential_friends = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    photo = sqlalchemy.Column(sqlalchemy.String)

    messages = sqlalchemy.Column(sqlalchemy.String)

    messages_bad = sqlalchemy.Column(sqlalchemy.String)

    about = sqlalchemy.Column(sqlalchemy.String)

    form = sqlalchemy.Column(sqlalchemy.String)

    informal_name = sqlalchemy.Column(sqlalchemy.Integer)

    role = sqlalchemy.Column(sqlalchemy.Integer)

    chats = sqlalchemy.Column(sqlalchemy.String)


    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
