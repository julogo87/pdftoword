from flask import Flask, render_template, request, send_file
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text')
        pdf_file = request.files['pdf_file']

        # Leer el PDF original
        reader = PdfReader(pdf_file)
        writer = PdfWriter()

        # Crear un archivo PDF en memoria para el recuadro
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)

        # Configuración del rectángulo
        x = 25  # Posición horizontal del rectángulo
        y = 450  # Posición vertical del rectángulo
        width = 100
        height = 50

        # Dibujar el rectángulo
        can.setStrokeColor(colors.black)
        can.setLineWidth(2)
        can.rect(x, y, width, height)

        # Dibujar el texto dentro del rectángulo
        text_object = can.beginText(x + 10, y + height - 20)
        text_object.setFont("Helvetica", 10)
        text_object.textLines(text)
        can.drawText(text_object)

        can.save()

        # Mover el puntero del archivo a la posición inicial
        packet.seek(0)

        # Leer el PDF con el recuadro
        new_pdf = PdfReader(packet)

        # Añadir el recuadro a cada página del PDF original
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            page.merge_page(new_pdf.pages[0])
            writer.add_page(page)

        # Guardar el nuevo PDF
        output = BytesIO()
        writer.write(output)
        output.seek(0)

        return send_file(output, as_attachment=True, download_name="modified.pdf", mimetype='application/pdf')

    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
