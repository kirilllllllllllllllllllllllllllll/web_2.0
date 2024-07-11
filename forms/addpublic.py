from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class AddPublic(FlaskForm):
    name = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('...', validators=[DataRequired()])
    # img = FileField('Фото пользователя (png, jpg, jpeg)')
    is_private = BooleanField('Только для друзей')
    submit = SubmitField('Готово')
