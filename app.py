import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
from fpdf import FPDF

# Función para leer el archivo Excel
def leer_excel(archivo_excel):
    excel_data = pd.read_excel(archivo_excel)
    return excel_data

# Función para leer el contenido del PDF
def leer_pdf(archivo_pdf):
    reader = PdfReader(archivo_pdf)
    contenido_pdf = ""
    for page in reader.pages:
        contenido_pdf += page.extract_text()
    return contenido_pdf

# Función para modificar el PDF y agregar datos
def modificar_pdf(contenido_pdf, dato_a_agregar):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Agregar contenido original del PDF
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, contenido_pdf)

    # Agregar el dato extraído del Excel
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Nuevo dato agregado: {dato_a_agregar}", ln=True)

    # Guardar el nuevo PDF
    archivo_modificado = "archivo_modificado.pdf"
    pdf.output(archivo_modificado)
    return archivo_modificado

# Interfaz de Streamlit
st.title("Buscar y Modificar PDF con Datos de Excel")

# Subir el archivo Excel
archivo_excel = st.file_uploader("Sube un archivo Excel", type=["xlsx"])
# Subir el archivo PDF
archivo_pdf = st.file_uploader("Sube un archivo PDF", type=["pdf"])

if archivo_excel is not None and archivo_pdf is not None:
    # Leer el archivo Excel
    excel_data = leer_excel(archivo_excel)
    dato_a_buscar = excel_data['columna_donde_esta_el_dato'][0]  # asumiendo que tienes una columna llamada 'columna_donde_esta_el_dato'

    # Leer el contenido del PDF
    contenido_pdf = leer_pdf(archivo_pdf)

    # Buscar el dato en el PDF
    if dato_a_buscar in contenido_pdf:
        st.success(f"El dato '{dato_a_buscar}' fue encontrado en el PDF.")
        
        # Modificar el PDF y agregar el dato
        archivo_modificado = modificar_pdf(contenido_pdf, dato_a_buscar)
        st.download_button(
            label="Descargar PDF Modificado",
            data=open(archivo_modificado, "rb").read(),
            file_name=archivo_modificado,
            mime="application/pdf"
        )
    else:
        st.warning(f"El dato '{dato_a_buscar}' no se encontró en el PDF.")
