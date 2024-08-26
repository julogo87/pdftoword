from flask import Flask, request, send_file
import os
from pdf2docx import Converter

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_pdf_to_word():
    if 'pdf_file' not in request.files:
        return "No file uploaded", 400

    pdf_file = request.files['pdf_file']
    pdf_path = os.path.join("uploads", pdf_file.filename)
    word_path = pdf_path.replace('.pdf', '.docx')

    pdf_file.save(pdf_path)

    # Convert PDF to Word
    cv = Converter(pdf_path)
    cv.convert(word_path)
    cv.close()

    return send_file(word_path, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(debug=True)
