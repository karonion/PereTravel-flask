from flask import Flask, render_template, url_for, request, redirect, send_from_directory
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a really really really really long secret key'
db = SQLAlchemy(app)
UPLOAD_FOLDER = r'C:\Users\Игорь\PycharmProjects\PereTravel\static\uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager(app)


class Article(db.Model):
    __tablename__ = 'Article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False, unique=True)
    preview = db.Column(db.String(128))
    text = db.Column(db.String, nullable=False)
    autorsname = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    filepath = db.Column(db.String(128), default='http://127.0.0.1:5000/images/default.jpeg')
    rates = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Post %r>' % self.id


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):
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


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def main():
    article_scope = Article.query.order_by(Article.date.desc())
    return render_template('main.html', article_scope=article_scope)


@app.route('/login', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect('/')
        return 'wrong password\email'
    return render_template('login.html', form=form)


@app.route('/admin')
@login_required
def adminn():
    return render_template('/admin/admin.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        first_name = request.form['FirstName']
        last_name = request.form['LastName']
        email = request.form['Email']
        password = request.form['Password']
        password_hash = generate_password_hash(password)
        user = User(First_Name=first_name, Last_Name=last_name, email=email, password_hash=password_hash)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return e
    else:
        return render_template('/register.html')


@app.route('/addpost', methods=['POST', 'GET'])
def addpost():
    if request.method == 'POST':
        title = request.form['title']
        preview = request.form['preview']
        text = request.form['text']
        name = request.form['autorsname']
        file = request.files['filepath']
        filename = 'default.jpeg'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        article = Article(title=title, preview=preview, text=text, autorsname=name, filepath=filename)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/addpost')
        except Exception as e:
            return e
    else:
        return render_template('/addpost.html')


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
