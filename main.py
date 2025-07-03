"""
Asistente Integral - Sistema de Análisis de Currículos
=====================================================

Este script principal coordina el proceso completo de:
1. Carga de documentos (PDF/DOCX) desde la carpeta 'data'
2. Construcción de una base de datos vectorial para búsqueda semántica
3. Interfaz de chat interactiva para consultar información de los CVs

"""

# Importaciones de módulos 
from resume_processor import load_resumes  # Módulo para cargar y procesar documentos
from qa_engine import build_db, ask_question  # Módulo para Motor de preguntas y respuestas
import sys  # Libreria para funcionalidades generales del sistema 

def main(): 
    """
    Se crea la función principal que ejecuta el flujo completo del asistente.
    
    Flujo:
    1. Carga documentos de la carpeta 'data'
    2. Construye base de datos vectorial
    3. Inicia bucle interactivo de preguntas
    """
    
    # PASO 1: CARGA DE DOCUMENTOS
    print("Cargando hojas de vida...")
    # Carga todos los archivos PDF y DOCX de la carpeta 'data'
    # Retorna una lista de los archivos con su nombre y contenido: [(nombre_archivo, contenido_texto),...]
    resumes = load_resumes("data") #Se carga en un array

    # Validación: verificar que se encontraron documentos
    if not resumes:
        print("No se encontraron archivos en la carpeta 'data'.")
        print("Asegúrate de tener archivos PDF o DOCX en la carpeta 'data'.")
        return

    # Mostrar número de documentos cargados
    print(f" {len(resumes)} documentos cargados.")

    # PASO 2: CONSTRUCCIÓN DE BASE DE DATOS VECTORIAL 
    # Convierte los documentos en embeddings y los almacena para búsqueda semántica
    # Esto permite encontrar información relevante basada en significado, no solo palabras clave
    collection = build_db(resumes) #Construye el listado de documentos
    print("Vector de documentos listo.") #Muestra que terminó de contruir el listado de docs

    #PASO 3: Mensajes de la interfaz de consola
    #Se muestran los mensajes:
    print("\n Asistente Integral SAS Listo.")
    print("Escribe tu pregunta (o 'salir' para terminar):")
    print("   Ejemplos de preguntas:")
    print("   - ¿Qué experiencia tiene en ingeniería civil de proyectos?")
    print("   - ¿Ha gestionado proyectos de sostenibilidad?")
    print("   - ¿Quién tiene experiencia en gestión de proyectos?")
    print("   - ¿Donde estudió x persona?")

    # Bucle principal de interacción para evitar que se cierre el programa
    while True:
        # Se captura la pregunta 
        question = input("\n> ").strip()
        
        # Si es = a salir se da un mensaje de hasta luego
        if question.lower() == "salir":
            print("¡Hasta luego!")
            break
            
        # Si viene vacía pide que escribas algo
        if not question:
            print(" Escribe algo.")
            continue
            
        # Procesar la pregunta 
        # Esto buscará información relevante en los CVs y generará una respuesta
        ask_question(collection, question) #Funcion qa engine

        #FIN FUNCIÓN MAIN

# Llamado de la función main para que se ejecute el programa 
main()
