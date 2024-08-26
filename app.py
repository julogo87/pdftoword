from flask import Flask, request, render_template, send_file, redirect, url_for
import os
from werkzeug.utils import secure_filename
from io import BytesIO
import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def replace_text_in_pdf(file_path, old_text, new_text):
    with pdfplumber.open(file_path) as pdf:
        output = BytesIO()
        c = canvas.Canvas(output, pagesize=letter)

        for page in pdf.pages:
            text = page.extract_text()
            if text and old_text in text:
                text = text.replace(old_text, new_text)
            
            # Escribir el texto modificado en un nuevo PDF
            text_lines = text.split("\n")
            y = 750
            for line in text_lines:
                c.drawString(10, y, line)
                y -= 15

            c.showPage()  # Crear una nueva página en el PDF

        c.save()
        output.seek(0)
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
                return send_file(output, as_attachment=True, download_name=filename, mimetype='application/pdf')

            return send_file(file_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


