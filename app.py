from flask import Flask, render_template, flash, request, session, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from models import *


@app.route('/')
def index():
    articles = Article.query.all()
    articles_dict = [dict(id=article.id, title=article.title, text=article.text) for article in articles]
    return render_template('index.html', articles=articles_dict)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        info = get_user_info(username, password)
        if type(info) != str:  # 验证
            user = User(id)
            login_user(user)
            session['login'] = True
            flash('You\'ve logged in successfully!')
            return redirect(url_for('index'))
        else:
            error = info

    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('login', None)
    flash('You have logged out successfully')
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if len(username) == 0:
            error = 'please input username'
        elif len(password) == 0:
            error = 'please input password'
        else:
            info = get_user_info(username)
            if info == 'username does not exist!':  # 用户名不存在，可以注册
                user = User(username=username, password=password)
                db.session.add(user)
                db.session.commit()
                flash('New user has been successfully added')
                return redirect(url_for('signup'))
            else:
                error = 'username already exists!'

    return render_template('signup.html', error=error)


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    error = None
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        if len(title) == 0:
            error = 'please input title'
        elif len(text) == 0:
            error = 'please input text'
        else:
            article = Article(title=title, text=text)
            db.session.add(article)
            db.session.commit()
            flash('New article has been successfully posted')
            return redirect(url_for('post'))

    return render_template('post.html', error=error)


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    error = None
    if request.method == 'POST':
        article_id = request.form.get('article_id')
        if len(article_id) == 0:
            error = 'please input article id'
        else:
            article = Article.query.filter(Article.id == article_id).all()
            if len(article) == 0:
                error = 'this article id does not exist'
            else:
                db.session.delete(article[0])
                db.session.commit()
                flash('this article has been successfully deleted')
                return redirect(url_for('delete'))

    return render_template('delete.html', error=error)


@login_manager.user_loader
def load_user(id):
    print(id)
    return User(id)


def get_user_info(username, password=None):
    user = User.query.filter(User.username == username).all()
    if len(user) == 0:
        return 'username does not exist!'

    if user[0].password == password:
        return user[0].id
    return 'wrong password'


if __name__ == '__main__':
    app.run(debug=True)
