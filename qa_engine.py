"""
Motor de Preguntas y Respuestas

Este módulo implementa un sistema que:
1. Convierte documentos en embeddings vectoriales
2. Realiza búsqueda semántica para encontrar información relevante
3. Genera respuestas usando GPT-4o basadas en el contexto encontrado

Tecnologías utilizadas:
- OpenAI Embeddings (text-embedding-3-small)
- OpenAI GPT-4o-mini para generación de respuestas
- Búsqueda por similitud coseno

"""

# Importaciones del sistema y librerías externas
import os # Manejar variables de entorno (OPENAI_API_KEY)
import textwrap #Dividir texto largo en bloques manejables
import time #Pausas cuando la API alcanza rate-limit
import numpy as np #Operaciones numéricas rápidas con vectores
from openai import OpenAI, RateLimitError, APIStatusError 

#CONFIGURACIÓN
MAX_CHARS = 2000   # Tamaño máximo de cada fragmento de texto
TOP_K     = 5      # Número de fragmentos más relevantes a enviar a GPT

# Verificar que la API key esté configurada
api_key = os.getenv("OPENAI_API_KEY") #Lee la variable de entorno del sistema operativo. Devuelve None si no existe
if not api_key: #Entra cuando la clave no está bien definida o es cadena vacía
    raise RuntimeError("  Falta OPENAI_API_KEY. Configura la variable de entorno.")#Lanza una excepción y detiene el programa
# Inicializar cliente de OpenAI
client = OpenAI(api_key=api_key) #Se conecta el scrip con la API

#FUNCIONES

def _chunk(text, max_chars=MAX_CHARS): #Divide un texto largo en fragmentos más pequeños.
    
    return textwrap.wrap(text, max_chars, break_long_words=False) # No corta palabras a la mitad

def _embed(texts): #Convierte textos en embeddings vectoriales usando OpenAI.
    
    while True: #Bucle infinito hasta que se haga un return
        try:

            # Crear embeddings usando el modelo de OpenAI
            resp = client.embeddings.create( 
                model="text-embedding-3-small",  # Llama a la API de OpenAI para obtener embeddings
                input=texts,
                timeout=60  # Espera máxima de 60 segundos para recibir la respuesta
            )

            # Convertir a arrays numpy y normalizar
            vecs = [np.array(d.embedding, dtype=np.float32) for d in resp.data] #Convierte cada embedding en una lista np.array

            normalized_vecs = [v / np.linalg.norm(v) for v in vecs] #Normaliza cada vector
            return normalized_vecs
        except RateLimitError:
            # Si se excede el límite de velocidad, esperar y reintentar
            print(" Rate limit alcanzado - pausando 20 segundos...")
            time.sleep(20) #Espera antes de reintentar

# CONSTRUCCIÓN DE LA BASE DE DATOS 

def build_db(documents): #Construye una base de datos vectorial a partir de documentos.
    
    db = [] #Aquí guardaremos todos los fragmentos
    
    # Procesar cada documento
    for doc_id, (fname, full_text) in enumerate(documents):
        print(f"• Procesando {fname}...")
        
        # Dividir el texto en fragmentos manejables
        parts = _chunk(full_text) #Divide en fragmentos de 2000 caracteres
        
        # Convertir fragmentos a embeddings
        vecs = _embed(parts) #Obtiene un vector por fragmento
        # vecs = [] ;
        # Almacenar cada fragmento con su vector
        for part_id, (snippet, vec) in enumerate(zip(parts, vecs)):
            db.append({
                "file": fname,      # Nombre del archivo original
                "part": part_id,    # Número de fragmento
                "text": snippet,    # Texto del fragmento
                "vec": vec          # Vector embedding
            })
    
    print(f" Base de datos construida con {len(db)} fragmentos")
    return db

#PREGUNTAS Y RESPUESTAS

def ask_question(db, question, k=TOP_K, lang="es"): #Responde una pregunta usando búsqueda semántica y generación de texto.
    
    # Convertir pregunta a embedding
    q_vec = _embed([question])[0]
    # q_vec = []
    # Calcular similitud con todos los fragmentos
    # Usamos producto punto entre vectores normalizados
    scores = [float(np.dot(item["vec"], q_vec)) for item in db]
    
    # Obtener los k fragmentos más relevantes
    top_idx = np.argsort(scores)[-k:][::-1]  # Ordenar por score descendente
    
    #Construir contexto con los fragmentos encontrados de la pregunta por el usuario
    context = ""
    for rank, idx in enumerate(top_idx, 1):
        item = db[idx]
        context += f"[{rank}] {item['text']}\n" 
    
    #Configurar mensajes para GPT se da contexto como desarrollador
    system_msg = (
        "Eres un asistente especializado en análisis de currículos. "
        "Tu tarea es responder preguntas sobre la información contenida en los CVs. "
        "Instrucciones importantes:\n"
        "• Usa ÚNICAMENTE la información del CONTEXTO proporcionado\n"
        "• Responde de forma clara, concisa y en español\n"
        "• Si la información no está en el contexto, di 'No encontrado en el CV'\n"
        "• Sé específico y menciona el nombre del archivo cuando sea relevante"
    )
    
    user_msg = f"CONTEXTO:\n{context}\n\nPREGUNTA: {question}"
    
    #Generar respuesta usando GPT-4o
    try:
        chat_resp = client.chat.completions.create(
            model="gpt-4o-mini",  # Modelo más económico
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user",   "content": user_msg},
            ],
            temperature=0.2,  # Baja temperatura para respuestas más consistentes
        )
        answer = chat_resp.choices[0].message.content.strip() if chat_resp.choices[0].message.content else "No se pudo generar una respuesta."
        
    except APIStatusError as e:
        # Manejar errores de la API de OpenAI
        answer = f"Error de OpenAI (código {e.status_code}): {str(e)}"
    except Exception as e:
        # Manejar otros errores inesperados
        answer = f" Error inesperado: {str(e)}"

    # Mostrar información de fragmentos que se usaron y la puntuación de cada uno
    print("\n Fragmentos utilizados:")
    for r, idx in enumerate(top_idx, 1):
        item = db[idx]
        score = scores[idx]
        print(f" [{r}] {item['file']} (parte {item['part']}) - Score: {score:.3f}")

    #Mostrar respuesta final
    print("\n Respuesta:")
    print(answer)
