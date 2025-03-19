from flask_wtf import FlaskForm
<<<<<<< HEAD
from wtforms import TextAreaField, SubmitField, StringField
=======
from wtforms import SubmitField, StringField
>>>>>>> 304bd0b271344315fddd8a1e08198432ab75bd08
from wtforms.validators import DataRequired


class AddMessage(FlaskForm):
    content = StringField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить')
