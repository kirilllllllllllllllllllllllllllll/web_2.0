from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class AddChat(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    img = FileField('Ава группы (png, jpg, jpeg)')
    submit = SubmitField('Готово')
