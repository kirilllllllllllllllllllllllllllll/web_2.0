import sqlalchemy
from .db_session import SqlAlchemyBase


# таблица пользователя
class Publication(SqlAlchemyBase):
    __tablename__ = 'publication'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    author = sqlalchemy.Column(sqlalchemy.Integer)

    author_name = sqlalchemy.Column(sqlalchemy.String)

    is_private = sqlalchemy.Column(sqlalchemy.Boolean)

    photos = sqlalchemy.Column(sqlalchemy.String)

    count_photos = sqlalchemy.Column(sqlalchemy.Integer)

    title = sqlalchemy.Column(sqlalchemy.String)

    # photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # comments = sqlalchemy.Column(sqlalchemy.String, nullable=True)

