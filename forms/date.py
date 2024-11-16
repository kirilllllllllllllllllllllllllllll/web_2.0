from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired


class AddDate(FlaskForm):
    name = StringField('Заголовок', validators=[DataRequired()])
    date = DateField('дата', validators=[DataRequired()])
    submit = SubmitField('Готово')
