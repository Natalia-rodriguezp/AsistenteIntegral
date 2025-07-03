"""
Procesador de Documentos

Este módulo se encarga de:
1. Extraer texto de archivos PDF y DOCX
2. Cargar múltiples documentos desde una carpeta
3. Manejar errores de lectura de archivos

"""

# Importaciones necesarias para procesamiento de documentos
from docx import Document  # Librería para abrir archivos Word
from PyPDF2 import PdfReader  # Librería para archivos PDF
import os  # Para obtener la dirección del sistema operativo

#Se define una función para extraer texto de un .docx
def extract_text_from_docx(file_path):
    """
    file_path es la ruta completa del archivo .docx 
    Devuelve una cadena con todo el texto o una cadena vacía si algo falla
    """
    try: #Control de excepciones 
        # Abrir el documento Word y almacenar en .docx
        doc = Document(file_path) #Carga el Word en memoria
        # Extraer texto de todos los párrafos, filtrando líneas vacías
        text_parts = []
        #Se define un bucle:
        for paragraph in doc.paragraphs: #Recorre cada párrafo
            if paragraph.text.strip():  # Solo incluir párrafos con contenido
                text_parts.append(paragraph.text)
        return "\n".join(text_parts)
    #En caso de que haya una excepción entra al siguiente bloque de código:
    except Exception as e:
        print(f" Error al leer {file_path}: {str(e)}")
        return ""
#Función extraer texto de un .pdf
def extract_text_from_pdf(file_path):
    
    try:
        # Abrir el archivo PDF
        reader = PdfReader(file_path)
        # Extraer texto de todas las páginas
        text_parts = []
        for page in reader.pages: #Bucle por cada página
            page_text = page.extract_text() #PyPDF2 intenta sacar el texto
            if page_text:  # Solo incluir páginas con texto
                text_parts.append(page_text)
        return "\n".join(text_parts)
    except Exception as e:
        print(f"Error al leer {file_path}: {str(e)}")
        return ""

#FUNCIÓN PPAL: 
def load_resumes(folder_path): #Carga todos los documentos PDF y DOCX de una carpeta.
    
    texts = []
    
    # Verificar que la carpeta existe
    if not os.path.exists(folder_path):
        print(f" La carpeta '{folder_path}' no existe.")
        return texts #Devuelvo lista vacía
    
    # Obtener lista de archivos en la carpeta
    try:
        files = os.listdir(folder_path)
    except PermissionError:
        print(f"  No tienes permisos para acceder a '{folder_path}'.")
        return texts
    
    # Procesar cada archivo de la carpeta
    for file in files:
        # Construir ruta completa al archivo
        path = os.path.join(folder_path, file)
        
        # Verificar que es un archivo (no una carpeta)
        if not os.path.isfile(path):
            continue
            
        # Procesar según la extensión del archivo y llamar a la función correcta
        if file.lower().endswith(".docx"):
            print(f" Procesando Word: {file}")
            text = extract_text_from_docx(path)
            if text:  # Solo agregar si se extrajo texto exitosamente
                texts.append((file, text))
                
        elif file.lower().endswith(".pdf"):
            print(f" Procesando PDF: {file}")
            text = extract_text_from_pdf(path)
            if text:  # Solo agregar si se extrajo texto exitosamente
                texts.append((file, text))
    
    return texts
