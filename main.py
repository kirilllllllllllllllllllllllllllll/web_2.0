from flask import Flask, render_template, redirect, url_for
from data import db_session
from forms.register import Register
from forms.login import Login
from data.user import User
from data.publication import Publication

from flask_login import login_user
from flask_login import login_required
from flask_login import LoginManager
from flask_login import logout_user
from flask_login import current_user
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'kirik1234pro_and_thisismyshadow_secret_key'
app.config['UPLOAD_FOLDER'] = os.getcwd() + "\static\profile_photos"


login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('index.html', title='Вход')

# выход из аккаунта
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_teacher(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# регистрация
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = Register()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        f = form.img.data
        if f.filename == '':

            user = User(
                name=form.name.data,
                email=form.email.data,
                publications='0',
                friends='0',
                photo='0'
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        else:
            type = f.filename.split('.')[-1]
            if type in ['png', 'jpg', 'jpeg', 'bmp']:
                user = User(
                    name=form.name.data,
                    email=form.email.data,
                    publications='0',
                    friends='0',
                    photo='0'
                )
                user.set_password(form.password.data)
                db_sess.add(user)
                db_sess.commit()
                st = str(user.id) + '.' + type
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], st))
                user.photo = st
                db_sess.commit()
                return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


# вход в аккаунт
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/main")

        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/main')
def main():
    return render_template('main.html', title='Главныя страница')


if __name__ == '__main__':
    db_session.global_init("db/vklasse.db")
    db_sess = db_session.create_session()
    print(os.getcwd() + '\statiс\img')
    app.run(port=8080, host='127.0.0.1')
