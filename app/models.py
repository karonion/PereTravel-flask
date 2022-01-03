from app import db, login_manager
from flask_login import (LoginManager, UserMixin, login_required,
                         login_user, current_user, logout_user)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, length
from datetime import datetime
from flask_ckeditor import CKEditorField


@login_manager.user_loader  # Пытаемся авторизовать пользователя при входе
def load_user(user_id):
    return db.session.query(User).get(user_id)


class Article(db.Model):  # Посты, БД
    __tablename__ = 'Article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False, unique=True)
    preview = db.Column(db.String(128))
    text = db.Column(db.String, nullable=False)
    autorsname = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    filepath = db.Column(db.String(128), default='default.jpg')
    rates = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Post %r>' % self.id


class User(db.Model, UserMixin):  # Юзеры, БД
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    First_Name = db.Column(db.String(100), nullable=False)
    Last_Name = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow())
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Feedback_db(db.Model):  # Обратная связь, БД
    __tablename__ = 'user_feedback'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(100))
    text = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __repr__(self):
        return '<Feedback %r>' % self.id


class LoginForm(FlaskForm):  # Логинизация, форма
    email = StringField('Email', validators=[Email(message='Перевірте коректність вводу'),
                                             DataRequired(message='Поле не може бути пустим')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Поле не може бути пустим')])
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField(label='Увійти')


class RegisterForm(FlaskForm):  # Регистрация, форма
    first_name = StringField("Ім'я", validators=[DataRequired(message='Поле не може бути пустим')])
    last_name = StringField('Фамілія', validators=[DataRequired(message='Поле не може бути пустим')])
    email = StringField('Email', validators=[Email(message='Перевірте коректність вводу'),
                                             DataRequired(message='Поле не може бути пустим')])
    password = PasswordField('Пароль', validators=[DataRequired(),
                                                   EqualTo('confirm_password', message='Паролі мають співпадати')])
    confirm_password = PasswordField('Повторіть пароль')
    submit = SubmitField(label='Реєстрація')


class FeedbackForm(FlaskForm):  # Обратная связь, форма
    contact = StringField('Контактні данні')
    text = TextAreaField(validators=[DataRequired(message='Поле не може бути пустим')], label='Текст')
    submit = SubmitField(label='Відправити')


class Addpost(FlaskForm):
    body = CKEditorField(validators=[DataRequired(message='Поле не може бути пустим'),
                                     length(min=30, message='Додайте опис до вашого маршруту!')])