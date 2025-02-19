from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, FileField, SelectField
from wtforms.validators import DataRequired


class ChooseForm(FlaskForm):
    form = SelectField('Класс',
                       choices=[(0, '7A'), (1, '7Б'), (2, '7В'), (3, '7Г'), (4, '8A'), (5, '8Б'), (6, '8В'), (7, '8Г'),
                                (8, '9A'), (9, '9Б'), (10, '9В'), (11, '9Г'), (12, '10A'), (13, '10Б'), (14, '10В'),
                                (15, '10Г'), (16, '11A'), (17, '11Б'), (18, '11В'), (19, '11Г')], validators=[DataRequired()])

    submit = SubmitField('Вывести расписание')
