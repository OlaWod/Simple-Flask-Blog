from flask import Flask, render_template, flash, request, session, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from models import *

@app.route('/')
def show_entries():
    entries = Entries.query.all()
    entries_dict = [dict(title=x.title, text=x.text) for x in entries]
    return render_template('show_entries.html', entries=entries_dict)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('username') != app.config.get('USERNAME'):
            error = 'Invalid username'
        elif request.form.get('password') != app.config.get('PASSWORD'):
            error = 'Invalid password'
        else:
            session['login'] = True
            flash('You\'re loginned successfully!')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('login', None)
    flash('You have logouted successfully')
    return redirect(url_for('show_entries'))

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('login'):
        abort(401)

    entry = Entries(title=request.form.get('title'), text=request.form.get('text'))
    db.session.add(entry)
    db.session.commit()

    flash('New entry has beensuccessfully posted')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run(debug=True)
