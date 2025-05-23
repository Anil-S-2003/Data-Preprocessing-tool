from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pandas as pd
import string

app = Flask(__name__)
app.secret_key = "secret_key"
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MongoDB Setup
client = MongoClient('localhost', 27017)
db = client['user1']
users = db['userCollection']

# Home (Login Page)
@app.route('/')
def home():
    return redirect(url_for('login'))

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        user = users.find_one({'username': uname})
        if user and check_password_hash(user['password'], pwd):
            session['username'] = uname
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        cpwd = request.form['confirm_password']
        if pwd != cpwd:
            flash('Passwords do not match.')
        elif users.find_one({'username': uname}):
            flash('Username already exists.')
        else:
            users.insert_one({'username': uname, 'password': generate_password_hash(pwd)})
            flash('Signup successful. Please login.')
            return redirect(url_for('login'))
    return render_template('signup.html')

# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    results = None
    message = None
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            if filename.endswith('.csv'):
                df = pd.read_csv(filepath)
            elif filename.endswith('.xlsx'):
                df = pd.read_excel(filepath)
            else:
                flash("Unsupported file format.")
                return redirect(url_for('dashboard'))

            empty_cells = []
            for row_idx, row in df.iterrows():
                for col_idx, value in enumerate(row):
                    if pd.isna(value) or str(value).strip() == "":
                        cell_ref = f"{string.ascii_uppercase[col_idx]}{row_idx + 2}"  # +2 for header row
                        empty_cells.append({
                            "row": row_idx + 1,
                            "column": df.columns[col_idx],
                            "index": cell_ref
                        })

            if empty_cells:
                results = empty_cells
            else:
                message = "No empty cells found."

    return render_template('dashboard.html', results=results, message=message)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if __name__ == '__main__':
    app.run(debug=True)
