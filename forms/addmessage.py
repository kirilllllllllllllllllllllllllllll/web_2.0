from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FileField


class AddMessage(FlaskForm):
    content = StringField('Сообщение')
    file = FileField('Файл')
    submit = SubmitField('Отправить')
