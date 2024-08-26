from flask import Flask, request, render_template, send_file, redirect, url_for
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def replace_text_in_pdf(file_path, old_text, new_text):
    reader = PdfReader(file_path)
    writer = PdfWriter()
    for page in reader.pages:
        text = page.extract_text()
        if old_text in text:
            text = text.replace(old_text, new_text)
            page_text = page.extract_text()
            page_text = page_text.replace(old_text, new_text)
            writer.add_page(page)
    output = BytesIO()
    writer.write(output)
    return output

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        old_text = request.form.get('old_text')
        new_text = request.form.get('new_text')

        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            if old_text and new_text:
                output = replace_text_in_pdf(file_path, old_text, new_text)
                output.seek(0)
                return send_file(output, as_attachment=True, download_name=filename, mimetype='application/pdf')

            return send_file(file_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

