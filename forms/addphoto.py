from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired


class AddPhoto(FlaskForm):
    photo = FileField('Изображение (png, jpg, jpeg)', validators=[DataRequired()])
    submit = SubmitField('Готово')
