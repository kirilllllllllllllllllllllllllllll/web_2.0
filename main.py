from datetime import datetime, timedelta

from sqlalchemy import and_

from flask import Flask, render_template, redirect, url_for
from data import db_session

from forms.register import Register
from forms.login import Login
from forms.addfriend import AddFriend
from forms.addpublic import AddPublic
from forms.addcomment import AddComment
from forms.date import AddDate

from data.user import User
from data.publication import Publication
from data.comment import Comment
from data.date import Date

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
        num1 = int(form.form.data)
        st = str(num1 // 4 + 7)
        num2 = num1 % 4
        if num2 == 0:
            st += 'A'
        elif num2 == 1:
            st += 'Б'
        elif num2 == 2:
            st += 'В'
        else:
            st += 'Г'
        if f.filename == '':
            user = User(
                name=form.name.data,
                email=form.email.data,
                form=st,
                informal_name=form.informal_name.data,
                about=form.about.data,
                publications='0',
                friends='0',
                photo='watch_cat_2.png',
                potential_friends='0',
                messages='0',
                messages_bad='0'
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
                    form=st,
                    informal_name=form.informal_name.data,
                    about=form.about.data,
                    publications='0',
                    friends='0',
                    photo='0',
                    potential_friends='0',
                    messages='0',
                    messages_bad='0'
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


@app.route('/add_publication', methods=['GET', 'POST'])
def add_publication():
    form = AddPublic()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        public = Publication(
            name=form.name.data,
            content=form.content.data,
            author=current_user.id,
            author_name=current_user.name,
            is_private=form.is_private.data,
        )

        db_sess.add(public)
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if current_user.publications == '0':
            user.publications = str(public.id)
        else:
            user.publications = user.publications + ',' + str(public.id)
        db_sess.commit()
        return redirect('/posts')

    return render_template('add_publication.html', title='Добавление публикации', form=form)


@app.route('/add_friend')
def add_friend():
    if current_user.friends != '0':
        data = db_sess.query(User).filter(
            and_(User.id.notin_(list(map(int, current_user.friends.split(',')))), User.id != current_user.id),
            User.potential_friends.notlike(f'%{current_user.id}%'), User.id.notin_(list(map(int, current_user.potential_friends.split(','))))).all()
    else:
        data = db_sess.query(User).filter(
            and_(User.id != current_user.id),
            User.potential_friends.notlike(f'%{current_user.id}%'), User.id.notin_(list(map(int, current_user.potential_friends.split(','))))).all()
    return render_template('add_friend.html', title='Добавление друга', data=data)


@app.route('/add_friend2', methods=['GET', 'POST'])
def add_friend2():
    form = AddFriend()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.email != current_user.email:
            if str(user.id) not in current_user.friends and str(user.id) not in current_user.potential_friends and str(current_user.id) not in user.potential_friends:
                if user.potential_friends == '0':
                    user.potential_friends = str(current_user.id)
                else:
                    user.potential_friends = user.potential_friends + ',' + str(current_user.id)
                db_sess.commit()
                return redirect('/main')
            else:
                return render_template('add_friend2.html',
                                       message="Этот пользователь уже ваш друг",
                                       form=form)
        return render_template('add_friend2.html',
                               message="Такого пользователя нет (либо вы пытаетесь добавить самого себя в друзья)",
                               form=form)
    # data = db_sess.query(User).filter(User.id.notin_(current_user.friends))
    return render_template('add_friend2.html', title='Добавление друга', form=form)


@app.route('/read_publication/posts')
def mirror():
    return redirect('/posts')


@app.route('/reflection/<int:id>')
def reflection(id):
    user = db_sess.query(User).filter(User.id == id).first()
    if user.potential_friends == '0':
        user.potential_friends = str(current_user.id)
    else:
        user.potential_friends = user.potential_friends + ',' + str(current_user.id)
    db_sess.commit()
    return redirect('/add_friend')


@app.route('/shadow1/<int:id>')
def shadow1(id):
    user1 = db_sess.query(User).filter(User.id == current_user.id).first()
    user2 = db_sess.query(User).filter(User.id == id).first()
    if user1.friends == '0':
        user1.friends = str(id)
    else:
        user1.friends = user1.friends + ',' + str(id)
    if user2.friends == '0':
        user2.friends = str(user1.id)
    else:
        user2.friends = user2.friends + ',' + str(user1.id)
    data = user1.potential_friends.split(',')
    data.remove(str(id))
    user1.potential_friends = ','.join(data)
    if user1.potential_friends == '':
        user1.potential_friends = '0'
    if user2.messages == '0':
        user2.messages = str(current_user.id)
    else:
        user2.messages = user2.messages + ',' + str(current_user.id)
    db_sess.commit()
    return redirect('/main')


@app.route('/shadow2/<int:id>')
def shadow2(id):
    user1 = db_sess.query(User).filter(User.id == current_user.id).first()
    user2 = db_sess.query(User).filter(User.id == id).first()

    data = user1.potential_friends.split(',')
    data.remove(str(id))
    user1.potential_friends = ','.join(data)
    if user1.potential_friends == '':
        user1.potential_friends = '0'
    if user2.messages_bad == '0':
        user2.messages_bad = str(current_user.id)
    else:
        user2.messages_bad = user2.messages_bad + ',' + str(current_user.id)
    db_sess.commit()
    return redirect('/main')


@app.route('/read_publication/<int:id>', methods=['GET', 'POST'])
def read_publication(id):
    form = AddComment()
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            author=current_user.id,
            author_name=current_user.name,
            photo=current_user.photo,
            publication=id
        )
        db_sess.add(comment)
        db_sess.commit()
        return redirect(f'/read_publication/{id}')

    public = db_sess.query(Publication).filter(Publication.id == id).first()
    text = public.content  # текст публикации
    data = db_sess.query(Comment).filter(
        Comment.publication == id).all()  # список объектов класса Comment, затем в html отображаем комментарии
    return render_template('read_publication.html', title='Публикация', form=form, text=text, data=data,
                           name=public.author_name)


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    data = db_sess.query(Publication).filter(Publication.is_private == 0).all()
    print(data)
    data2 = db_sess.query(Publication).filter(Publication.is_private == 1).all()
    data2 = list(filter(lambda a: str(current_user.id) in db_sess.query(User).filter(
        User.id == a.author).first().friends or current_user.id == db_sess.query(User).filter(
        User.id == a.author).first().id, data2))
    print(data2)
    data += data2
    return render_template('posts.html', title='Публикации', data=data)


@app.route('/date', methods=['GET', 'POST'])
def date():
    form = AddDate()
    if form.validate_on_submit():
        date = Date(
            name=form.name.data,
            date=str(form.date.data),
            user=current_user.id
        )
        db_sess.add(date)
        db_sess.commit()
        return redirect('/date')

    dates = db_sess.query(Date).filter(Date.user == current_user.id).all()
    outdated = list(
        filter(lambda a: datetime.now().date() - datetime.fromisoformat(a.date).date() >= timedelta(days=1), dates))
    outdated = list(map(lambda a: a.id, outdated))
    db_sess.query(Date).filter(Date.id.in_(outdated)).delete()
    db_sess.commit()

    dates = db_sess.query(Date).filter(Date.user == current_user.id).all()

    dates1 = list(
        filter(lambda a: datetime.fromisoformat(a.date).date() - datetime.now().date() < timedelta(days=2), dates))
    dates2 = list(
        filter(lambda a: datetime.fromisoformat(a.date).date() - datetime.now().date() >= timedelta(days=2), dates))
    print(dates1, dates2)

    return render_template('date.html', title='Добавление даты', form=form, dates1=dates1, dates2=dates2)


@app.route('/delete_friend/<int:id>')
def delete_frined(id):
    print(current_user.friends)
    user1 = db_sess.query(User).filter(User.id == current_user.id).first()
    data = user1.friends.split(',')
    data.remove(str(id))
    st = ','.join(data)
    if not st:
        st = 0
        user1.friends = st
    db_sess.commit()
    print(user1.friends)
    return redirect('/profile')


@app.route('/profile')
def profile():
    friends = db_sess.query(User).filter(User.id.in_(list(map(int, current_user.friends.split(',')))))
    return render_template('profile.html', title='Профиль', friends=friends)


@app.route('/main')
def main():
    data = db_sess.query(Publication).filter(Publication.is_private == 0).all()
    print(data)
    data2 = db_sess.query(Publication).filter(Publication.is_private == 1).all()
    data2 = list(filter(lambda a: str(current_user.id) in db_sess.query(User).filter(
        User.id == a.author).first().friends or current_user.id == db_sess.query(User).filter(
        User.id == a.author).first().id, data2))
    print(data2)
    data += data2
    if current_user.potential_friends != '0':
        friends = list(map(lambda a: db_sess.query(User).filter(User.id == int(a)).first(),
                           current_user.potential_friends.split(',')))
    else:
        friends = []
    if current_user.messages != '0':
        messages = list(
            map(lambda a: db_sess.query(User).filter(User.id == int(a)).first(), current_user.messages.split(',')))
    else:
        messages = []
    if current_user.messages_bad != '0':
        messages_bad = list(
            map(lambda a: db_sess.query(User).filter(User.id == int(a)).first(), current_user.messages_bad.split(',')))
    else:
        messages_bad = []
    return render_template('main.html', title='Главная страница', data=data, friends=friends, messages_bad=messages_bad,
                           messages=messages)


if __name__ == '__main__':
    db_session.global_init("db/watch_cats.db")
    db_sess = db_session.create_session()
    print(os.getcwd() + '\statiс\profile_photos')
    app.run(port=8080, host='127.0.0.1')
