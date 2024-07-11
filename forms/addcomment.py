from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class AddComment(FlaskForm):
    content = TextAreaField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Готово')
