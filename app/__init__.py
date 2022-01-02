from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_ckeditor import CKEditor


app = Flask(__name__, template_folder='static/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a really really really really really long secret key'
db = SQLAlchemy(app)
UPLOAD_FOLDER = r'C:\Users\Игорь\PycharmProjects\PereTravel\app\static\uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Будь-ласка, авторизуйтесь'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'ig.vasylenko2@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'ig.vasylenko2@gmail.com'
app.config['MAIL_PASSWORD'] = '1dn2qy36'
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
app.config['CKEDITOR_LANGUAGE'] = 'ru'
app.config['CKEDITOR_WIDTH'] = '1000'
app.config['CKEDITOR_HEIGHT'] = '1000'
app.config['CKEDITOR_FILE_UPLOADER'] = 'http://127.0.0.1:5000/images/'
mail = Mail(app)
ckeditor = CKEditor(app)


from views import *


if __name__ == '__main__':
    app.run(debug=True)

