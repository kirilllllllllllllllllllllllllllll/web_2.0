from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired


class AddPublic(FlaskForm):
    name = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Текст', validators=[DataRequired()])
    photo = FileField('Изображение (png, jpg, jpeg)')
    is_private = BooleanField('Только для друзей')
    submit = SubmitField('Готово')
