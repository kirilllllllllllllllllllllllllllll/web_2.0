import sqlalchemy
from .db_session import SqlAlchemyBase


# таблица пользователя
class Comment(SqlAlchemyBase):
    __tablename__ = 'comment'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    author = sqlalchemy.Column(sqlalchemy.Integer)

    author_name = sqlalchemy.Column(sqlalchemy.String)

    publication = sqlalchemy.Column(sqlalchemy.Integer)

    photo = sqlalchemy.Column(sqlalchemy.String)
