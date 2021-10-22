import os
from flask import Flask, flash, request, redirect, url_for, render_template, session
from werkzeug.utils import secure_filename
from read import read
from solver import solver

# Configure application
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        location = str(UPLOAD_FOLDER) + '/' + file.filename
        filename = 'static/uploads/' + filename
        session["raw_sudoku"], session["display_raw_sudoku"] = read(filename)
        session["sudoku_location"] = filename
        sudoku = session["display_raw_sudoku"]
        return render_template('check.html', filename=filename, sudoku=sudoku)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/<filename>')
def display_image(filename, path):
    return redirect(url_for('static', filename), code=301)

@app.route('/check', methods=['POST'])
def check():
    if request.method == "POST":
        if "raw_sudoku" and "display_raw_sudoku" and "sudoku_location" in session:
            raw_sudoku = session["raw_sudoku"]
            display_raw_sudoku = session["display_raw_sudoku"]
            f = request.form
            for key in f.keys():
                for value in f.getlist(key):
                    if value:
                        session["raw_sudoku"][int(key[0])][int(key[1])] = int(value)
                        session["display_raw_sudoku"][int(key[0])][int(key[1])] = int(value)
            solved_sudoku, message_indicator = solver(raw_sudoku, display_raw_sudoku)
            session["solved_sudoku"] = solved_sudoku
            sudoku = solved_sudoku
            filename = session["sudoku_location"]
        return render_template('again.html', filename=filename, sudoku=sudoku, message_indicator=message_indicator)

@app.route('/again', methods=['POST'])
def again():
    if request.method == "POST":
        if "sudoku_location" in session:
            os.remove(session["sudoku_location"])
    session.clear()
    return render_template('index.html')