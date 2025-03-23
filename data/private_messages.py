import sqlalchemy
from .db_session import SqlAlchemyBase


# таблица
class PrivateMessages(SqlAlchemyBase):
    __tablename__ = 'private_messages'


    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    chat = sqlalchemy.Column(sqlalchemy.Integer)

    sender = sqlalchemy.Column(sqlalchemy.Integer)

    name = sqlalchemy.Column(sqlalchemy.String)

    text = sqlalchemy.Column(sqlalchemy.String)

    photo = sqlalchemy.Column(sqlalchemy.String)

    time = sqlalchemy.Column(sqlalchemy.String)

    sticker = sqlalchemy.Column(sqlalchemy.String)

    file = sqlalchemy.Column(sqlalchemy.String)
