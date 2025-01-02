import sqlalchemy
from .db_session import SqlAlchemyBase


# таблица
class Chat(SqlAlchemyBase):
    __tablename__ = 'chat'


    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    admin = sqlalchemy.Column(sqlalchemy.Integer)

    photo = sqlalchemy.Column(sqlalchemy.String)

    peoples = sqlalchemy.Column(sqlalchemy.String)

    count_peoples = sqlalchemy.Column(sqlalchemy.Integer)
