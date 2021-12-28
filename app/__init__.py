from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager


app = Flask(__name__, template_folder='static/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a really really really really really long secret key'
db = SQLAlchemy(app)
UPLOAD_FOLDER = r'C:\Users\Игорь\PycharmProjects\PereTravel\app\static\uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager(app)

class Feedback_db(db.Model):  # Обратная связь, БД
    __tablename__ = 'user_feedback'
    id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(100))
    text = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __repr__(self):
        return '<Feedback %r>' % self.id


from views import *


if __name__ == '__main__':
    app.run(debug=True)

