import sqlalchemy
from .db_session import SqlAlchemyBase


# таблица пользователя
class Publication(SqlAlchemyBase):
    __tablename__ = 'publication'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    author = sqlalchemy.Column(sqlalchemy.Integer)

    # photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    comments = sqlalchemy.Column(sqlalchemy.String, nullable=True)

