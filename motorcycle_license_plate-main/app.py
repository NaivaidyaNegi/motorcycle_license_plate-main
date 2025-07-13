from flask import Flask, request, redirect, url_for, render_template, flash
import os
import uuid
import re
from main import process_video  # Now safely importe
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_safe_filename(filename):
    return re.match(r'^[\w\-. ]+$', filename) is not None

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['video']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        unique_id = str(uuid.uuid4())
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{unique_id}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Process the uploaded video
        plates = process_video(filepath)

        return render_template('result.html', filename=filename)
    else:
        flash('Invalid file type')
        return redirect(request.url)

@app.route('/result/<filename>')
def result(filename):
    if not is_safe_filename(filename):
        return render_template('error.html', message="Invalid or unsafe file.")
    return render_template('result.html', filename=filename)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True, use_reloader=False)

