from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddComment(FlaskForm):
    content = StringField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Готово')
