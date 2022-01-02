from flask import render_template, request, redirect, send_from_directory, url_for
from app import app
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename
from models import *
from models import db
import os
from __init__ import Message, Email, mail

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/')
def main():
    article_scope = Article.query.order_by(Article.date.desc())
    return render_template('main.html', article_scope=article_scope)


@app.route('/login', methods=['post', 'get'])
def login():
    message = ''
    if current_user.is_authenticated:
        message = 'Вы уже авторизованы!'
        return render_template('main.html', message=message)
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect('/')
        return 'wrong password\email'
    return render_template('login.html', form=form, message=message)


@app.route('/admin')
@login_required
def admin():
    return render_template('/admin/admin.html')


@app.route('/addpost', methods=['POST', 'GET'])
@login_required
def addpost():
    form = Addpost()
    if request.method == 'POST':
        title = request.form['title']
        preview = request.form['preview']
        text = form.body.data
        name = request.form['autorsname']
        file = request.files['filepath']
        filename = 'default.jpeg'
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        article = Article(title=title, preview=preview, text=text, autorsname=name, filepath=filename)
        try:
            db.session.add(article)
            db.session.commit()
            msg = Message(f'Новий пост!', sender='ig.vasylenko2@gmail.com', recipients=['karonion4ik@gmail.com'])
            msg.body = f'Був доданий новий пост від користувача {name}, {datetime.utcnow().date()}'
            mail.send(msg)
            return redirect('/')
        except Exception as e:
            return e
    else:
        return render_template('/addpost.html', form=form)


@app.route('/post/<int:id>')
def get_exect_post(id):
    article_exect = Article.query.get(id)
    return render_template('post.html', article_exect=article_exect)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['post', 'get'])
def register():
    message = ''
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password
        password_hash = generate_password_hash(password.data)
        user = User(First_Name=first_name, Last_Name=last_name, email=email, password_hash=password_hash)
        try:
            db.session.add(user)
            db.session.commit()
            msg = Message(f'Вдала реєстрація!', sender='ig.vasylenko2@gmail.com', recipients=[f'{email}'])
            msg.html = render_template(r'Registration-email.html', login=email, password=password.data)
            mail.send(msg)
            message = 'Вдала реєстрація! Скористуйтесь логіном та паролем. Вони відправлені вам на пошту'
            return 'successful'
        except Exception as e:
            return e
    return render_template('register.html', form=form)


@app.route('/feedback', methods=['get', 'post'])
def send_feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        contact = form.contact.data
        text = form.text.data
        feedback = Feedback_db(contact=contact, text=text)
        try:
            db.session.add(feedback)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return e
    return render_template('/feedback.html', form=form)

@app.route('/getfeedback')
@login_required
def get_feedback():
    feedback_scope = Feedback_db.query.order_by(Feedback_db.created.desc())
    return render_template('getfeedback.html', feedback_scope=feedback_scope)
