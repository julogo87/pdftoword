from flask import Flask, request, render_template, send_file, redirect, url_for
import os
from werkzeug.utils import secure_filename
from io import BytesIO
import fitz  # PyMuPDF

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def replace_text_in_pdf(file_path, old_text, new_text):
    # Abrir el PDF con PyMuPDF
    doc = fitz.open(file_path)
    for page in doc:
        text_instances = page.search_for(old_text)
        for inst in text_instances:
            page.insert_text(inst, new_text, fontsize=12, color=(0, 0, 0))
    
    # Guardar el PDF modificado en memoria
    output = BytesIO()
    doc.save(output)
    doc.close()
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

