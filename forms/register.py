from wsgiref.validate import validator

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, FileField, SelectField
from wtforms.validators import DataRequired


class Register(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    form = SelectField('Класс',
                       choices=[(0, '7А'), (1, '7Б'), (2, '7В'), (3, '7Г'), (4, '8А'), (5, '8Б'), (6, '8В'), (7, '8Г'),
                                (8, '9А'), (9, '9Б'), (10, '9В'), (11, '9Г'), (12, '10А'), (13, '10Б'), (14, '10В'),
                                (15, '10Г'), (16, '11А'), (17, '11Б'), (18, '11В'), (19, '11Г')], validators=[DataRequired()])
    img = FileField('Фото пользователя (png, jpg, jpeg)')
    role = SelectField('Роль',
                       choices=[(0, 'ученик'), (1, 'учитель'), (2, 'модератор')], validators=[DataRequired()])
    code = StringField('Код подтверждения (для учителей и модераторов)')
    submit = SubmitField('Войти')
