import sqlalchemy
from .db_session import SqlAlchemyBase


# таблица
class Timetable(SqlAlchemyBase):
    __tablename__ = 'timetable'


    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    lessons = sqlalchemy.Column(sqlalchemy.String)

    day = sqlalchemy.Column(sqlalchemy.Integer)

    form = sqlalchemy.Column(sqlalchemy.String)
