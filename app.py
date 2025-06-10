from flask import Flask, render_template, request, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
import sqlite3
from datetime import datetime


app = Flask(__name__)

@app.context_processor
def inject_datetime():
    return {'datetime': datetime}

app.secret_key = 'secretkey'

DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM Logins WHERE username = ? AND password = ?', (username, password)).fetchone()
        if user:
            session['user'] = username
            return redirect(url_for('home'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    query = '''
        SELECT b.name, b.description, d.sale_price
        FROM Bean b
        JOIN DailyBean d ON b.id = d.bean_id
        WHERE d.sale_price >= 0.00
        ORDER BY d.id ASC
        LIMIT 1
    '''
    bean = db.execute(query).fetchone()
    return render_template('home.html', bean=bean)


@app.route('/catalogue')
def catalogue():
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    query = '''
        SELECT b.name, b.description, d.sale_price
        FROM Bean b
        JOIN DailyBean d ON b.id = d.bean_id
        WHERE d.sale_price >= 0.00
    '''
    beans = db.execute(query).fetchall()
    return render_template('catalogue.html', beans=beans)


@app.route('/distributor')
def distributor():
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    distributors = db.execute('SELECT * FROM Distributor').fetchall()
    return render_template('distributor.html', distributors=distributors)


@app.route('/add_distributor', methods=['GET', 'POST'])
def add_distributor():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']
        email = request.form['email']

        db = get_db()
        db.execute("""
            INSERT INTO Distributor (name, city, state, country, phone, email)
            VALUES (?, ?, ?, ?, ?, ?)""", (name, city, state, country, phone, email))
        db.commit()
        return redirect(url_for('distributor'))

    return render_template('add_distributor.html')


@app.route('/edit_distributor/<int:id>', methods=['GET', 'POST'])
def edit_distributor(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    distributor = db.execute('SELECT * FROM Distributor WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']
        email = request.form['email']

        db.execute('''
            UPDATE Distributor
            SET name = ?, city = ?, state = ?, country = ?, phone = ?, email = ?
            WHERE id = ?''',
            (name, city, state, country, phone, email, id))
        db.commit()
        return redirect(url_for('distributor'))

    return render_template('edit_distributor.html', distributor=distributor)


UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        file = request.files['file']

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db.execute('INSERT INTO Upload (title, filename, author) VALUES (?, ?, ?)',
                       (title, filename, author))
            db.commit()
            return redirect(url_for('upload'))

    uploads = db.execute('SELECT * FROM Upload').fetchall()
    return render_template('upload.html', uploads=uploads)


@app.route('/order_status')
def order_status():
    if 'user' not in session:
        return redirect(url_for('login'))

    # Data dummy
    orders = [
        {'order_id': 'INV001', 'bean': 'Arabica', 'status': 'Shipped', 'date': '2025-06-10'},
        {'order_id': 'INV002', 'bean': 'Robusta', 'status': 'Processing', 'date': '2025-06-09'},
        {'order_id': 'INV003', 'bean': 'Cubita', 'status': 'Delivered', 'date': '2025-06-08'},
    ]

    return render_template('order_status.html', orders=orders)


if __name__ == '__main__':
    app.run(debug=True)
