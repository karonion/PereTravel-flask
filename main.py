from flask import Flask,render_template,url_for,request,redirect,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
UPLOAD_FOLDER = r'C:\Users\Игорь\PycharmProjects\PereTravel\static\uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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


@app.route('/')
def main():
    article_scope = Article.query.order_by(Article.date.desc())
    return render_template('main.html', article_scope=article_scope)


@app.route('/login')
def log_in():
    return render_template('login.html')


@app.route('/admin')
def adminn():
    return render_template('/admin/admin.html')


@app.route('/register')
def sign_in():
    return render_template('register.html')

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




if __name__ == '__main__':
    app.run(debug=True)
