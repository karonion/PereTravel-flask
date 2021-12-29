from app import db, login_manager
from flask_login import (LoginManager, UserMixin, login_required,
                         login_user, current_user, logout_user)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField, Form
from datetime import datetime


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
    email = StringField('Email', validators=[Email(message='Проверьте правильность ввода'),
                                             DataRequired(message='Поле не может быть пустым')])
    password = PasswordField('Password', validators=[DataRequired(message='Поле не может быть пустым')])
    remember = BooleanField('Remember Me')
    submit = SubmitField()


class RegisterForm(FlaskForm):  # Регистрация, форма
    first_name = StringField('Имя', validators=[DataRequired(message='Поле не может быть пустым')])
    last_name = StringField('Фамилия', validators=[DataRequired(message='Поле не может быть пустым')])
    email = StringField('Email', validators=[Email(message='Проверьте правильность ввода'),
                                             DataRequired(message='Поле не может быть пустым')])
    password = PasswordField('Пароль', validators=[DataRequired(),
                                                   EqualTo('confirm_password', message='Пароли должны совпадать')])
    confirm_password = PasswordField('Повторите пароль')
    submit = SubmitField()


class FeedbackForm(FlaskForm):  # Обратная связь, форма
    contact = StringField('Контактные данные')
    text = TextAreaField(validators=[DataRequired(message='Поле не может быть пустым')])
    submit = SubmitField()





