from flask import render_template, request, redirect, send_from_directory, url_for, flash
from app import app
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename
from models import *
from models import db
from flask_ckeditor import upload_fail, upload_success
import os
from __init__ import Message, Email, mail

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS  # Функция проверки формата загружаемого фото


@app.route('/images/<path:filename>')  # Путь загужаемых файлов
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:  # разрешённые форматы фото для загрузки
        return upload_fail(message='Тільки фото!')
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
    url = url_for('uploaded_file', filename=f.filename)
    return upload_success(url, filename=f.filename)


@app.route('/')  # Отображение всех постов
def main():
    article_scope = Article.query.order_by(Article.date.desc())  # Сортировка по дате создания
    return render_template('main.html', article_scope=article_scope)


@app.route('/login', methods=['post', 'get'])  # Логинизация
def login():
    message = ''
    if current_user.is_authenticated:  # Если авторизванный человек логинизируется
        message = 'Ви вже авторизовані!'
        return render_template('main.html', message=message)
    form = LoginForm()
    if form.validate_on_submit():  # Если нажал кнопку отправки формы
        user = db.session.query(User).filter(User.email == form.email.data).first()  # Сверяемся с первым результатом в БД
        if user and user.check_password(form.password.data):  # Проверяем хэш пароля на соответствие
            login_user(user, remember=form.remember.data)
            return redirect('/')  # Если пароль совпал
        else:
            flash(r'Невірний пароль або логін', 'alert alert-warning')
            return redirect(url_for('login'))
    return render_template('login.html', form=form, message=message)


@app.route('/admin')
@login_required
def admin():
    return render_template('/admin/admin.html')


@app.route('/addpost', methods=['POST', 'GET'])  # Добавление поста
@login_required
def addpost():
    form = Addpost()
    if request.method == 'POST':
        title = request.form['title']
        preview = request.form['preview']
        text = form.body.data  # Ссылка на CKEditor
        name = request.form['autorsname']
        file = request.files['filepath']
        filename = 'default.jpeg'
        if file and allowed_file(file.filename):  # Загрузка фото-первью
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        article = Article(title=title, preview=preview, text=text, autorsname=name, filepath=filename)
        try:  # Запись в БД
            db.session.add(article)
            db.session.commit()
            msg = Message(f'Новий пост!', sender='ig.vasylenko2@gmail.com', recipients=['karonion4ik@gmail.com'])  # Оправка емеил сообщения администратору
            msg.body = f'Був доданий новий пост від користувача {name}, {datetime.utcnow().date()}'
            mail.send(msg)
            flash("Пост відправлений на модерацію, ми опрацюємо його найближчим часом", 'alert alert-success')
            return redirect(url_for('main'))
        except Exception as e:
            return e
    else:
        return render_template('/addpost.html', form=form)


@app.route('/post/<int:id>')  # Пост подробно
def get_exect_post(id):
    article_exect = Article.query.get(id)
    return render_template('post.html', article_exect=article_exect)


@app.route('/logout/')  # Логаут
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['post', 'get'])
def register():
    message = ''
    if current_user.is_authenticated:  # Если человек уже авторизован, перенаправляем на главную
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password
        password_hash = generate_password_hash(password.data)  # Преобразуем пароль в хэш
        user = User(First_Name=first_name, Last_Name=last_name, email=email, password_hash=password_hash)  # Записываем в БД
        try:
            db.session.add(user)
            db.session.commit()
            msg = Message(f'Вдала реєстрація!', sender='ig.vasylenko2@gmail.com', recipients=[f'{email}'])  # Отправка сообщения пользователю
            msg.html = render_template(r'Registration-email.html', login=email, password=password.data)
            mail.send(msg)
            flash('Вдала реєстрація! Скористуйтесь логіном та паролем. Вони відправлені Вам на пошту.', 'alert alert-success')
            return redirect(url_for('login'))
        except Exception as e:
            return e
    return render_template('register.html', form=form)


@app.route('/feedback', methods=['get', 'post'])  # Обратная связь
def send_feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        contact = form.contact.data
        text = form.text.data
        feedback = Feedback_db(contact=contact, text=text)  # Записываем в БД
        try:
            db.session.add(feedback)
            db.session.commit()
            flash("Дякуємо за зворотній звя'язок!", 'alert alert-success')  # Редирект на главную
            return redirect(url_for('main'))
        except Exception as e:
            return e
    return render_template('/feedback.html', form=form)

@app.route('/getfeedback')
@login_required
def get_feedback():
    feedback_scope = Feedback_db.query.order_by(Feedback_db.created.desc())
    return render_template('getfeedback.html', feedback_scope=feedback_scope)
