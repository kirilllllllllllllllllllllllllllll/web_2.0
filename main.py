from datetime import datetime, timedelta

from sqlalchemy import and_, or_

from flask import Flask, render_template, redirect, url_for
from data import db_session
from data.private_chat import PrivateChat

from forms.register import Register
from forms.login import Login
from forms.addfriend import AddFriend
from forms.addpublic import AddPublic
from forms.addcomment import AddComment
from forms.date import AddDate
from forms.addchat import AddChat
from forms.addmessage import AddMessage
from forms.refactortimetable import RefactorTimetable
from forms.addphoto import AddPhoto
from forms.addpeoples import AddPeoples
from forms.chooseform import ChooseForm

from data.user import User
from data.publication import Publication
from data.comment import Comment
from data.date import Date
from data.chat import Chat
from data.messages import Messages
from data.timetable import Timetable
from data.private_messages import PrivateMessages

from flask_login import login_user
from flask_login import login_required
from flask_login import LoginManager
from flask_login import logout_user
from flask_login import current_user

import os

from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kirik1234pro_and_thisismyshadow_secret_key'
app.config['UPLOAD_FOLDER'] = os.getcwd() + "\static\profile_photos"
app.config['UPLOAD_FOLDER2'] = os.getcwd() + "\static\chat_imgs "
app.config['UPLOAD_FOLDER3'] = os.getcwd() + "\static\posts"
SECRET_CODE1 = '124_9713'
SECRET_CODE2 = '124_nexus'
CONST = ['7А', '7Б', '7В', '7Г', '8А', '8Б', '8В', '8Г', '9А', '9Б', '9В', '9Г', '10А', '10Б', '10В', '10Г', '11А',
         '11Б', '11В', '11Г']
TIME1 = ['8:00 - 8:35', '8:40 - 9:20', '9:25 - 10:05', '10:25 - 12:05', '12:25 - 13:05', '13:10 - 13:50',
         '13:55 - 14:35', '14:50 - 15:20', '14:50 - 15:20']
TIME2 = ['---', '8:00 - 8:40', '8:45 - 9:25', '9:30 - 10:10', '10:30 - 11:10', '11:30 - 12:10', '12:30 - 13:10',
         '13:15 - 13:55', '14:15 - 14:45']
COLORS = ['#E8EAF6', '#C5CAE9']
STICKERS = ['shark_1', 'shark_2', 'shark_3', 'shark_4', 'shark_5', 'shark_6', 'shark_7', 'shark_8', 'shark_9',
            'shark_10', 'shark_11', 'shark_12', 'shark_13', 'shark_14', 'shark_15', 'shark_16', 'shark_17', 'shark_18',
            'shark_19', 'shark_20', 'shark_21', 'shark_22', 'shark_23', 'shark_24', 'shark_25', 'shark_26', 'shark_27',
            'shark_28', 'shark_29', 'shark_30', 'shark_31', 'shark_32', 'shark_33', 'shark_34', 'shark_35', 'shark_36',
            'shark_37', 'shark_38', 'shark_39', 'shark_40', 'shark_41', 'shark_42', 'shark_43', 'shark_44', 'shark_45',
            'shark_46',
            'shark_47', 'shark_48']
SIZE_PHOTO = 500

login_manager = LoginManager()
login_manager.init_app(app)


def create_chat(id, form):
    data = ','.join(list(map(lambda a: str(a.id), db_sess.query(User).filter(User.form == form).all())))
    print(data)
    chat = Chat(
        name=form,
        admin=id,
        photo='chat.png',
        peoples=data,
        count_peoples=data.count(',') + 1

    )
    db_sess.add(chat)
    db_sess.commit()


def add_student(id, form):
    chat = db_sess.query(Chat).filter(Chat.name == form).first()
    if chat:
        chat.peoples = chat.peoples + ',' + str(id)
        chat.count_peoples += 1
        db_sess.commit()


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
        role = int(form.role.data)
        if role == 1 and form.code.data != SECRET_CODE1:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Неверный код подтверждения учителя")
        elif role == 2 and form.code.data != SECRET_CODE2:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Неверный код подтверждения модератора")
        else:
            f = form.img.data
            num1 = int(form.form.data)
            st = str(num1 // 4 + 7)
            num2 = num1 % 4
            if num2 == 0:
                st += 'А'
            elif num2 == 1:
                st += 'Б'
            elif num2 == 2:
                st += 'В'
            else:
                st += 'Г'

            if role == 1 and db_sess.query(User).filter(and_(User.role == 1, User.form == st)).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message=f"В {st} классе уже зарегистрирован классный руководитель")
            else:

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
                        messages_bad='0',
                        role=role,
                        chats='0',
                        current_form=st
                    )
                    user.set_password(form.password.data)
                    db_sess.add(user)

                    db_sess.commit()
                    user.idstr = str(user.id)
                    db_sess.commit()

                    if role == 1:
                        create_chat(user.id, st)
                    elif role == 0:
                        add_student(user.id, st)

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
                            messages_bad='0',
                            role=role,
                            chats='0',
                            current_form=st
                        )
                        user.set_password(form.password.data)
                        db_sess.add(user)
                        db_sess.commit()
                        user.idstr = str(user.id)

                        st2 = str(user.id) + '.' + type
                        f.save(os.path.join(app.config['UPLOAD_FOLDER'], st2))
                        user.photo = st2

                        db_sess.commit()
                        if role == 1:
                            create_chat(user.id, st)
                        elif role == 0:
                            add_student(user.id, st)
                        print(user.id)
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
            return redirect("/posts")

        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/add_publication', methods=['GET', 'POST'])
def add_publication():
    form = AddPublic()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        f = form.photo.data
        if not f.filename:

            public = Publication(
                name=form.name.data,
                content=form.content.data,
                author=current_user.id,
                author_name=current_user.name,
                photos='0',
                count_photos=0,
                title='0',
                is_private=form.is_private.data,
                likes=0,
                flags='0'
            )

            db_sess.add(public)
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            if current_user.publications == '0':
                user.publications = str(public.id)
            else:
                user.publications = user.publications + ',' + str(public.id)
            db_sess.commit()
            return redirect('/posts')
        else:
            f = form.photo.data
            type = f.filename.split('.')[-1]
            if type in ['png', 'jpg', 'jpeg', 'bmp']:
                public = Publication(
                    name=form.name.data,
                    content=form.content.data,
                    author=current_user.id,
                    author_name=current_user.name,
                    photos='0',
                    title='0',
                    count_photos=1,
                    is_private=form.is_private.data,
                    likes=0,
                    flags='0'
                )

                db_sess.add(public)
                db_sess.commit()
                st2 = str(public.id) + '-0' + '.' + type
                path = os.path.join(app.config['UPLOAD_FOLDER3'], st2)
                f.save(path)
                im = Image.open(path)
                size = im.size
                num1 = SIZE_PHOTO
                num2 = int(num1 / size[1] * size[0])
                st3 = st2.split('.')[0] + '-' + str(num1) + '_' + str(num2) + '.' + st2.split('.')[-1]
                im.close()
                os.rename(path, os.path.join(app.config['UPLOAD_FOLDER3'], st3))

                public.photos = st3
                public.title = st3

                db_sess.commit()
                user = db_sess.query(User).filter(User.id == current_user.id).first()
                if current_user.publications == '0':
                    user.publications = str(public.id)
                else:
                    user.publications = user.publications + ',' + str(public.id)
                db_sess.commit()
                return redirect('/posts')
            else:
                return render_template('add_publication.html', title='Добавление публикации', form=form,
                                       message='Неподходящий тип файла')

    return render_template('add_publication.html', title='Добавление публикации', form=form)


@app.route("/add_photo/<int:id>", methods=['GET', 'POST'])
def add_photo(id):
    form = AddPhoto()
    if form.validate_on_submit():
        f = form.photo.data
        type = f.filename.split('.')[-1]
        if type in ['png', 'jpg', 'jpeg', 'bmp']:
            public = db_sess.query(Publication).filter(Publication.id == id).first()
            if public.title == '0':
                st2 = str(public.id) + '-0' + '.' + type
                path = os.path.join(app.config['UPLOAD_FOLDER3'], st2)
                f.save(path)
                im = Image.open(path)
                size = im.size
                num1 = SIZE_PHOTO
                num2 = int(num1 / size[1] * size[0])
                st3 = st2.split('.')[0] + '-' + str(num1) + '_' + str(num2) + '.' + st2.split('.')[-1]
                im.close()
                os.rename(path, os.path.join(app.config['UPLOAD_FOLDER3'], st3))

                public.photos = st3
                public.title = st3
                public.count_photos += 1
                db_sess.commit()
            else:
                st2 = str(public.id) + '-' + str(public.count_photos) + '.' + type
                path = os.path.join(app.config['UPLOAD_FOLDER3'], st2)
                f.save(path)
                im = Image.open(path)
                size = im.size
                num1 = SIZE_PHOTO
                num2 = int(num1 / size[1] * size[0])
                st3 = st2.split('.')[0] + '-' + str(num1) + '_' + str(num2) + '.' + st2.split('.')[-1]
                im.close()
                os.rename(path, os.path.join(app.config['UPLOAD_FOLDER3'], st3))

                public.photos = public.photos + ',' + st3
                # public.title = st2
                public.count_photos += 1
                db_sess.commit()
            # print(1, f)
            return redirect('/posts')
        return render_template('add_photo.html', title='Добавление фото', message='Неподходящий тип', form=form)
    return render_template('add_photo.html', title='Добавление фото', form=form)


@app.route('/add_friend')
def add_friend():
    if current_user.friends != '0':
        data = db_sess.query(User).filter(
            and_(User.id.notin_(list(map(int, current_user.friends.split(',')))), User.id != current_user.id),
            User.potential_friends.notlike(f'%{current_user.id}%'),
            User.id.notin_(list(map(int, current_user.potential_friends.split(','))))).all()
    else:
        data = db_sess.query(User).filter(
            and_(User.id != current_user.id),
            User.potential_friends.notlike(f'%{current_user.id}%'),
            User.id.notin_(list(map(int, current_user.potential_friends.split(','))))).all()
    return render_template('add_friend.html', title='Добавление друга', data=data)


@app.route('/add_friend2', methods=['GET', 'POST'])
def add_friend2():
    form = AddFriend()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.email != current_user.email:
            if str(user.id) not in current_user.friends and str(user.id) not in current_user.potential_friends and str(
                    current_user.id) not in user.potential_friends:
                if user.potential_friends == '0':
                    user.potential_friends = str(current_user.id)
                else:
                    user.potential_friends = user.potential_friends + ',' + str(current_user.id)
                db_sess.commit()
                return redirect('/add_friend')
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


@app.route('/read_chat/chats')
def mirror2():
    return redirect('/chats')


@app.route('/read_chat/add_peoples/<int:id>')
def mirror3(id):
    return redirect(f'/add_peoples/{id}')


@app.route('/add_peoples/read_chat/<int:id>')
def mirror4(id):
    return redirect(f'/read_chat/{id}')


@app.route('/read_private_chat/chats')
def mirror5():
    return redirect(f'/chats')


@app.route('/read_private_chat/read_chat/<int:id>')
def mirror6(id):
    return redirect(f'/read_chat/{id}')


@app.route('/read_chat/read_private_chat/<int:id>')
def mirror7(id):
    return redirect(f'/read_private_chat/{id}')


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
    # text = public.content  # текст публикации
    data = db_sess.query(Comment).filter(
        Comment.publication == id).all()  # список объектов класса Comment, затем в html отображаем комментарии
    return render_template('read_publication.html', title='Публикация', form=form, post=public, data=data,
                           name=public.author_name)


@app.route('/like/<int:id>/<user>')
def like(id, user):
    post = db_sess.query(Publication).filter(Publication.id == id).first()
    post.likes += 1
    if post.flags == '0':
        post.flags = user
    else:
        post.flags = post.flags + ',' + user
    db_sess.commit()
    return redirect('/posts')


@app.route('/dislike/<int:id>/<user>')
def dislike(id, user):
    post = db_sess.query(Publication).filter(Publication.id == id).first()
    post.likes -= 1
    data = post.flags.split(',')
    data.remove(user)
    if data:
        post.flags = ','.join(data)
    else:
        post.flags = '0'

    db_sess.commit()
    return redirect('/posts')


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


@app.route('/delete_post/<int:id>')
def delete_post(id):
    post = db_sess.query(Publication).filter(Publication.id == id).first()
    data = post.photos
    for i in data.split(','):
        if i != '0':
            os.remove(os.path.join(app.config['UPLOAD_FOLDER3'], i))
    db_sess.query(Publication).filter(Publication.id == id).delete()
    db_sess.query(Comment).filter(Comment.publication == id).delete()
    db_sess.commit()
    return redirect('/posts')


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
def delete_friend(id):
    print(current_user.friends)
    user1 = db_sess.query(User).filter(User.id == current_user.id).first()
    user2 = db_sess.query(User).filter(User.id == id).first()
    data = user1.friends.split(',')
    data2 = user2.friends.split(',')
    data.remove(str(id))
    data2.remove(str(current_user.id))
    st = ','.join(data)
    st2 = ','.join(data2)
    if not st:
        st = '0'
    user1.friends = st
    if not st2:
        st2 = '0'
    user2.friends = st2
    db_sess.commit()
    print(user1.friends)
    return redirect('/profile')


@app.route('/profile')
def profile():
    friends = db_sess.query(User).filter(User.id.in_(list(map(int, current_user.friends.split(',')))))
    return render_template('profile.html', title='Профиль', friends=friends, roles=['ученик', 'учитель', 'модератор'])


@app.route('/chats')
def chats():
    data = db_sess.query(Chat).filter(Chat.peoples.like(f'%{current_user.id}%')).all()
    data2 = db_sess.query(PrivateChat).filter(
        or_(PrivateChat.user2 == current_user.id, PrivateChat.user1 == current_user.id)).all()
    return render_template('chats.html', title='Группы', data=data, data2=data2)


@app.route('/send_sticker/<int:id>/<sticker>')
def send_sticker(id, sticker):
    message = Messages(
        text='none',
        sender=current_user.id,
        name=current_user.name,
        photo=current_user.photo,
        chat=id,
        time=str(datetime.now()).split('.')[0][:-3].split()[1],
        sticker=sticker + '.png'
    )
    db_sess.add(message)
    db_sess.commit()
    return redirect(f'/read_chat/{id}')


@app.route('/send_sticker1/<int:id>/<sticker>')
def send_sticker1(id, sticker):
    message = PrivateMessages(
        text='none',
        sender=current_user.id,
        name=current_user.name,
        photo=current_user.photo,
        chat=id,
        time=str(datetime.now()).split('.')[0][:-3].split()[1],
        sticker=sticker + '.png'
    )
    db_sess.add(message)
    db_sess.commit()
    return redirect(f'/read_private_chat/{id}')


@app.route('/read_chat/<int:id>', methods=['GET', 'POST'])
def read_chat(id):
    form = AddMessage()
    if form.validate_on_submit():
        message = Messages(
            text=form.content.data,
            sender=current_user.id,
            name=current_user.name,
            photo=current_user.photo,
            chat=id,
            time=str(datetime.now()).split('.')[0][:-3].split()[1],
            sticker='none'
        )
        db_sess.add(message)
        db_sess.commit()
        return redirect(f'/read_chat/{id}')

    # chat = db_sess.query(Chat).filter(Chat.id == id).first()
    data = db_sess.query(Chat).filter(Chat.peoples.like(f'%{current_user.id}%')).all()
    data2 = db_sess.query(PrivateChat).filter(
        or_(PrivateChat.user2 == current_user.id, PrivateChat.user1 == current_user.id)).all()

    chat, = filter(lambda a: a.id == id, data)
    messages = db_sess.query(Messages).filter(Messages.chat == id).all()

    return render_template('read_chat.html', title='Группа', form=form, chat=chat, messages=messages, id=id,
                           admin=chat.admin, data=data, data2=data2, stickers=STICKERS)


@app.route('/read_private_chat/<int:id>', methods=['GET', 'POST'])
def read_private_chat(id):
    form = AddMessage()
    if form.validate_on_submit():
        message = PrivateMessages(
            text=form.content.data,
            sender=current_user.id,
            name=current_user.name,
            photo=current_user.photo,
            chat=id,
            time=str(datetime.now()).split('.')[0][:-3].split()[1]
        )
        db_sess.add(message)
        db_sess.commit()
        return redirect(f'/read_private_chat/{id}')

    # chat = db_sess.query(Chat).filter(Chat.id == id).first()
    data = db_sess.query(Chat).filter(Chat.peoples.like(f'%{current_user.id}%')).all()
    data2 = db_sess.query(PrivateChat).filter(
        or_(PrivateChat.user2 == current_user.id, PrivateChat.user1 == current_user.id)).all()

    chat, = filter(lambda a: a.id == id, data2)
    messages = db_sess.query(PrivateMessages).filter(PrivateMessages.chat == id).all()
    return render_template('read_private_chat.html', title='Группа', form=form, chat=chat, messages=messages, id=id,
                           data=data, data2=data2, stickers=STICKERS)


@app.route('/read_private_chat/delete_message1/<int:id>/<int:message>')
def delete_message1(id, message):
    db_sess.query(PrivateMessages).filter(PrivateMessages.id == message).delete()
    return redirect(f'/read_private_chat/{id}')


@app.route('/read_chat/check_private/<int:user>')
@app.route('/check_private/<int:user>')
def check_private(user):
    chat = db_sess.query(PrivateChat).filter(or_(and_(PrivateChat.user1 == current_user.id, PrivateChat.user2 == user),
                                                 and_(PrivateChat.user2 == current_user.id,
                                                      PrivateChat.user1 == user))).first()
    if chat:
        return redirect(f'/read_private_chat/{chat.id}')
    else:
        user1 = db_sess.query(User).filter(User.id == user).first()
        chat = PrivateChat(
            name1=current_user.name,
            name2=user1.name,
            user1=user1.id,
            user2=current_user.id,
            photo1=user1.photo,
            photo2=current_user.photo
        )
        db_sess.add(chat)
        db_sess.commit()
        if user1.chats == '0':
            user1.chats = str(current_user.id)
        else:
            user1.chats = user1.chats + ',' + str(current_user.id)
        user2 = db_sess.query(User).filter(User.id == current_user.id).first()
        if user2.chats == '0':
            user2.chats = str(user1.id)
        else:
            user2.chats = user2.chats + ',' + str(user1.id)
        db_sess.commit()
        return redirect(f'/read_private_chat/{chat.id}')


@app.route('/check_peoples/<int:id>')
@app.route('/read_chat/check_peoples/<int:id>')
def check_peoples(id):
    chat = db_sess.query(Chat).filter(Chat.id == id).first()
    data1 = db_sess.query(User).filter(
        and_(User.id.in_(list(map(int, chat.peoples.split(',')))), User.id != current_user.id))

    return render_template('check_peoples.html', title='Добавление участников', data1=data1, id=id, admin=chat.admin)


@app.route('/add_peoples/window/<int:id>/<user>')
def window(id, user):
    chat = db_sess.query(Chat).filter(Chat.id == id).first()
    chat.peoples = chat.peoples + ',' + user
    chat.count_peoples += 1
    db_sess.commit()
    return redirect(f'/add_peoples/{id}')


@app.route('/window1/<int:user>')
def window1(user):
    user1 = db_sess.query(User).filter(User.id == current_user.id).first()
    user2 = db_sess.query(User).filter(User.id == user).first()
    chat = PrivateChat(
        name1=current_user.name,
        name2=user2.name,
        user1=user2.id,
        user2=current_user.id,
        photo1=user2.photo,
        photo2=current_user.photo
    )
    db_sess.add(chat)
    db_sess.commit()
    if user2.chats == '0':
        user2.chats = str(current_user.id)
    else:
        user2.chats = user2.chats + ',' + str(current_user.id)
    # user2 = db_sess.query(User).filter(User.id == current_user.id).first()
    if user1.chats == '0':
        user1.chats = str(user2.id)
    else:
        user1.chats = user1.chats + ',' + str(user2.id)
    db_sess.commit()
    return redirect('/chats')


@app.route('/add_peoples/del/<int:id>/<user>')
def delete_from_chat(id, user):
    chat = db_sess.query(Chat).filter(Chat.id == id).first()
    data = chat.peoples.split(',')
    data.remove(user)
    chat.peoples = ','.join(data)
    chat.count_peoples -= 1
    db_sess.commit()
    return redirect(f'/add_peoples/{id}')


@app.route('/read_chat/del/<int:id>/<user>')
def quit(id, user):
    chat = db_sess.query(Chat).filter(Chat.id == id).first()
    data = chat.peoples.split(',')
    name = db_sess.query(User).filter(User.id == int(user)).first().name
    data.remove(user)
    chat.peoples = ','.join(data)
    chat.count_peoples -= 1
    message = Messages(
        text=f"{name} покинул(-а) группу",
        sender=0,
        name=current_user.name,
        photo=current_user.photo,
        chat=id,
        time=str(datetime.now()).split('.')[0][:-3]
    )
    db_sess.add(message)
    db_sess.commit()
    return redirect('/chats')


@app.route('/read_chat/delete_chat/<int:id>')
def delete_chat(id):
    db_sess.query(Chat).filter(Chat.id == id).delete()
    db_sess.query(Messages).filter(Messages.chat == id).delete()
    db_sess.commit()
    return redirect('/chats')


@app.route('/read_chat/delete_message/<int:id>/<int:message>')
def delete_message(id, message):
    db_sess.query(Messages).filter(Messages.id == message).delete()
    return redirect(f'/read_chat/{id}')


@app.route('/add_peoples/<int:id>', methods=['GET', 'POST'])
def add_peoples(id):
    form = AddPeoples()
    chat = db_sess.query(Chat).filter(Chat.id == id).first()
    data1 = db_sess.query(User).filter(User.id.notin_(list(map(int, chat.peoples.split(',')))))
    data2 = db_sess.query(User).filter(
        and_(User.id.in_(list(map(int, chat.peoples.split(',')))), User.id != chat.admin))
    flag1 = False
    flag2 = False
    if not list(data1):
        flag1 = True
    if not list(data2):
        flag2 = True
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.email != current_user.email:
            if str(user.id) not in chat.peoples and user.id != chat.admin:
                chat.peoples = chat.peoples + ',' + str(user.id)
                chat.count_peoples += 1
                db_sess.commit()
                return redirect(f'/add_peoples/{id}')
            else:
                return render_template('add_peoples.html',
                                       message="Этот пользователь уже в группе",
                                       data1=data1, data2=data2, id=id, flag1=flag1, flag2=flag2, admin=chat.admin,
                                       form=form)
        return render_template('add_peoples.html',
                               message="Такого пользователя нет (либо вы пытаетесь добавить самого себя)",
                               data1=data1, data2=data2, id=id, flag1=flag1, flag2=flag2, admin=chat.admin,
                               form=form)
    # chat = db_sess.query(Chat).filter(Chat.id == id).first()
    # data1 = db_sess.query(User).filter(User.id.notin_(list(map(int, chat.peoples.split(',')))))

    return render_template('add_peoples.html', title='Добавление участников', data1=data1, data2=data2, id=id,
                           flag1=flag1, flag2=flag2, admin=chat.admin, form=form)


@app.route('/add_chat', methods=['GET', 'POST'])
def add_chat():
    form = AddChat()
    if form.validate_on_submit():
        f = form.img.data
        if form.name.data not in ['7А', '7Б', '7В', '7Г', '8А', '8Б', '8В', '8Г', '9А', '9Б', '9В', '9Г', '10А', '10Б',
                                  '10В', '10Г', '11А', '11Б', '11В', '11Г']:

            if f.filename == '':
                chat = Chat(
                    name=form.name.data,
                    admin=current_user.id,
                    photo='chat.png',
                    peoples=str(current_user.id),
                    count_peoples=1

                )
                db_sess.add(chat)
                db_sess.commit()
                return redirect('/chats')
            else:
                type = f.filename.split('.')[-1]
                if type in ['png', 'jpg', 'jpeg', 'bmp']:
                    chat = Chat(
                        name=form.name.data,
                        admin=current_user.id,
                        photo='0',
                        peoples=str(current_user.id),
                        count_peoples=1

                    )
                    db_sess.add(chat)
                    db_sess.commit()
                    st = str(chat.id) + '.' + type
                    f.save(os.path.join(app.config['UPLOAD_FOLDER2'], st))
                    chat.photo = st
                    db_sess.commit()
                    return redirect('/chats')
        else:
            return render_template('add_chat.html', title='Добавление группы',
                                   form=form,
                                   message="Невозможно создать группу с таким названием")
    # data = db_sess.query(User).filter(User.id.notin_(current_user.friends))
    return render_template('add_chat.html', title='Добавление группы', form=form)


@app.route('/add_private', methods=['GET', 'POST'])
def add_private():
    form = AddPeoples()
    # chat = db_sess.query(Chat).filter(Chat.id == id).first()
    # user = db_sess.query(User).filter(User.id == current_user.id).first()
    data1 = db_sess.query(User).filter(
        and_(User.id.notin_(list(map(int, current_user.chats.split(',')))), User.id != current_user.id)).all()
    flag1 = False
    if not list(data1):
        flag1 = True
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.email != current_user.email:
            if str(user.id) not in current_user.chats:
                chat = PrivateChat(
                    name1=current_user.name,
                    name2=user.name,
                    user1=user.id,
                    user2=current_user.id,
                    photo1=user.photo,
                    photo2=current_user.photo
                )
                db_sess.add(chat)
                db_sess.commit()
                if user.chats == '0':
                    user.chats = str(current_user.id)
                else:
                    user.chats = user.chats + ',' + str(current_user.id)
                user2 = db_sess.query(User).filter(User.id == current_user.id).first()
                if user2.chats == '0':
                    user2.chats = str(user.id)
                else:
                    user2.chats = user2.chats + ',' + str(user.id)
                db_sess.commit()
                return redirect('/chats')
            else:
                return render_template('add_private.html',
                                       message="Этот пользователь уже есть в личных чатах",
                                       data1=data1, flag1=flag1,
                                       form=form)
        return render_template('add_private.html',
                               message="Такого пользователя нет (либо вы пытаетесь добавить самого себя)",
                               data1=data1, flag1=flag1,
                               form=form)
    # chat = db_sess.query(Chat).filter(Chat.id == id).first()
    # data1 = db_sess.query(User).filter(User.id.notin_(list(map(int, chat.peoples.split(',')))))

    return render_template('add_private.html', title='Добавление участников', data1=data1,
                           flag1=flag1, form=form)


@app.route('/timetable', methods=['GET', 'POST'])
def timetable():
    form = ChooseForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        num1 = int(form.form.data)
        st = str(num1 // 4 + 7)
        num2 = num1 % 4
        if num2 == 0:
            st += 'А'
        elif num2 == 1:
            st += 'Б'
        elif num2 == 2:
            st += 'В'
        else:
            st += 'Г'
        user.current_form = st
        db_sess.commit()
        return redirect('/timetable')
    # print(current_user.form)
    # print(db_sess.query(Timetable).all())
    data = db_sess.query(Timetable).filter(Timetable.form == current_user.current_form).all()
    # print(data)
    data = sorted(data, key=lambda a: a.day)
    data = list(map(lambda a: a.lessons.split(','), data))
    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница']
    nums = range(9)
    for i in range(5):
        data[i] = (days[i], data[i])

    return render_template('timetable.html', title='Расписание', data=data, nums=nums, time1=TIME1, time2=TIME2,
                           colors=COLORS, form=form)


@app.route('/refactor_timetable', methods=['GET', 'POST'])
def refactor_timetable():
    form = RefactorTimetable()
    message = ''
    if form.validate_on_submit():
        form1 = CONST[int(form.form.data)]
        lesson = form.lesson.data
        number = form.number.data
        day = form.day.data
        timetable = db_sess.query(Timetable).filter(and_(Timetable.form == form1, Timetable.day == day)).first()
        data = timetable.lessons.split(',')
        data[int(number)] = lesson
        timetable.lessons = ','.join(data)
        db_sess.commit()
        message = 'сделано!'
    return render_template('refactor_timetable.html', title='Редактирование расписания', form=form, message=message)


def setup():
    if not db_sess.query(Timetable).all():
        for i in ['7А', '7Б', '7В', '7Г', '8А', '8Б', '8В', '8Г', '9А', '9Б', '9В', '9Г', '10А', '10Б', '10В', '10Г',
                  '11А', '11Б', '11В', '11Г']:
            for j in range(5):
                lessons = Timetable(
                    form=i,
                    lessons=',,,,,,,,',
                    day=j
                )
                db_sess.add(lessons)
                db_sess.commit()


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
    flag1 = False
    flag2 = False
    if not friends:
        flag1 = True
    if not messages and not messages_bad:
        flag2 = True
    return render_template('main.html', title='Главная страница', friends=friends, messages_bad=messages_bad,
                           messages=messages, flag1=flag1, flag2=flag2)


if __name__ == '__main__':
    db_session.global_init("db/watch_cats.db")
    db_sess = db_session.create_session()
    print(os.getcwd() + '\statiс\profile_photos')
    setup()
    app.run(port=8080, host='127.0.0.1')
