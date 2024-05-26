from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
import os
import zipfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        images = convert_from_path(filepath)
        image_filenames = []

        for i, image in enumerate(images):
            image_filename = f"{filename}_page_{i + 1}.png"
            image_filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_filepath, 'PNG')
            image_filenames.append(image_filepath)

        # Create a zip file
        zip_filename = f"{filename}.zip"
        zip_filepath = os.path.join(app.config['UPLOAD_FOLDER'], zip_filename)
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            for image_file in image_filenames:
                zipf.write(image_file, os.path.basename(image_file))

        return send_file(zip_filepath, as_attachment=True)

    return jsonify(error="File upload failed"), 500

if __name__ == '__main__':
    app.run(debug=True)
