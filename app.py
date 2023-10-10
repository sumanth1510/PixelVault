from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, template_folder="client/templates")
UPLOAD_FOLDER = 'database'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/')
def index():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(
        os.path.join(UPLOAD_FOLDER, f))]

    files.sort(key=lambda x: os.path.getctime(
        os.path.join(UPLOAD_FOLDER, x)), reverse=True)

    return render_template('index.html', images=files)


@app.route('/upload', methods=['POST'])
def upload_files():
    if 'images' not in request.files:
        return redirect(url_for('index'))

    files = request.files.getlist('images')

    if not files or all([f.filename == '' for f in files]):
        return redirect(url_for('index'))

    for file in files:
        if file:
            filename = secure_filename(file.filename)
            file_save_path = os.path.join(UPLOAD_FOLDER, filename)

            name, ext = os.path.splitext(filename)

            counter = 0
            while os.path.exists(file_save_path):
                counter += 1
                filename = f"{name} ({counter}){ext}"
                file_save_path = os.path.join(UPLOAD_FOLDER, filename)

            file.save(file_save_path)

    return render_template('success.html')


@app.route('/image/<filename>')
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/download/<filename>')
def download_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


@app.route('/<path:filename>')
def serve_static_file(filename):
    return send_from_directory("", filename)


if __name__ == '__main__':
    app.run(debug=True)
