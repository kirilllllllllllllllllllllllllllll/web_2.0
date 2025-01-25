from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField
from wtforms.validators import DataRequired


class AddPeoples(FlaskForm):
    email = EmailField('Почта пользователя', validators=[DataRequired()])
    submit = SubmitField('Готово')
