import sqlalchemy
from .db_session import SqlAlchemyBase


# таблица
class PrivateChat(SqlAlchemyBase):
    __tablename__ = 'privatechat'


    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name1 = sqlalchemy.Column(sqlalchemy.String)

    name2 = sqlalchemy.Column(sqlalchemy.String)

    user1 = sqlalchemy.Column(sqlalchemy.Integer)

    user2 = sqlalchemy.Column(sqlalchemy.Integer)

    photo1 = sqlalchemy.Column(sqlalchemy.String)

    photo2 = sqlalchemy.Column(sqlalchemy.String)
