from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField
from wtforms.validators import DataRequired


class AddFriend(FlaskForm):
    email = EmailField('Почта друга', validators=[DataRequired()])
    submit = SubmitField('Готово')
