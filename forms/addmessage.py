from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class AddMessage(FlaskForm):
    content = StringField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить')
