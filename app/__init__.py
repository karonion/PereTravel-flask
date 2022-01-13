from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_ckeditor import CKEditor


app = Flask(__name__, template_folder='static/templates')
'''SQL Настройки'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'xb6ghWhmodomaUkH8ZS5Kfec4'
db = SQLAlchemy(app)
'''Настройки загрузки файлов'''
UPLOAD_FOLDER = r'C:\Users\Игорь\PycharmProjects\PereTravel\app\static\uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
'''Настройки login-manager'''
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Будь-ласка, авторизуйтесь'
'''Настройки почтового сервера'''
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'ig.vasylenko2@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'ig.vasylenko2@gmail.com'
app.config['MAIL_PASSWORD'] = '1dn2qy36'
mail = Mail(app)
'''Настройки CKEditor, формы для работы с текстом'''
app.config['CKEDITOR_PKG_TYPE'] = 'full-al'
app.config['CKEDITOR_LANGUAGE'] = 'ru'
app.config['CKEDITOR_WIDTH'] = '1500'
app.config['CKEDITOR_HEIGHT'] = '500'
app.config['CKEDITOR_FILE_UPLOADER'] = 'http://127.0.0.1:5000/upload'
ckeditor = CKEditor(app)


from views import *


if __name__ == '__main__':
    app.run(debug=True)

