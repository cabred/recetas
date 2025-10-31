# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

# Base de datos simulada (Crystal Clear: mínima pero funcional)
recetas = [
    {"id": 1, "nombre": "Tacos al Pastor", "descripcion": "Marinar carne con achiote, cocinar y servir con piña."},
    {"id": 2, "nombre": "Enchiladas Verdes", "descripcion": "Rellenar tortillas con pollo, bañar en salsa verde y queso."}
]

@app.route('/')
def index():
    return render_template('index.html', recetas=recetas)

@app.route('/receta/<int:id>')
def ver_receta(id):
    receta = next((r for r in recetas if r['id'] == id), None)
    return render_template('receta.html', receta=receta)

@app.route('/receta/pdf/<int:id>')
def generar_pdf(id):
    receta = next((r for r in recetas if r['id'] == id), None)
    if not receta:
        return "Receta no encontrada", 404

    # Generar PDF en memoria
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"Receta - {receta['nombre']}")

    # Contenido del documento
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(100, 700, f"Receta: {receta['nombre']}")
    pdf.setFont("Helvetica", 14)
    pdf.drawString(100, 660, "Descripción:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 640, receta['descripcion'])

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True,
                     download_name=f"{receta['nombre']}.pdf",
                     mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
