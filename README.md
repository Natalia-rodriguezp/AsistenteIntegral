# Asistente Integral - Sistema de Análisis de Currículos

Un sistema inteligente de preguntas y respuestas que permite analizar y consultar información de múltiples currículos en formato PDF y DOCX.

## Arquitectura del Sistema

```
AsistenteIntegral/
├── main.py              # Script principal - Coordina todo el flujo
├── resume_processor.py  # Procesamiento de documentos PDF/DOCX
├── qa_engine.py         # Motor de preguntas y respuestas
├── data/                # Carpeta con los currículos a analizar
├── requirements.txt     # Librerias del proyecto
└── README.md            # Este archivo
```

## Instalación y Configuración

### 1. Clonar o descargar el proyecto

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual
```bash
venv\Scripts\activate
```

### 4. Instalar librerias
```bash
pip install -r requirements.txt
```

### 5. Configurar API Key de OpenAI
```bash
set OPENAI_API_KEY=tu_api_key_aqui

### 6. Agregar currículos
Coloca tus archivos PDF y DOCX en la carpeta `data/`

##  Uso del Sistema

### Ejecutar el asistente
```bash
python main.py
```

### Flujo de trabajo
1. **Carga de documentos**: El sistema carga automáticamente todos los PDF y DOCX de la carpeta `data/`
2. **Procesamiento**: Convierte los documentos en embeddings vectoriales para búsqueda semántica
3. **Interfaz interactiva**: Inicia un chat donde puedes hacer preguntas sobre los currículos

### Ejemplos de preguntas
- ¿Qué experiencia tiene en ingeniería civil de proyectos?
- ¿Ha gestionado proyectos de sostenibilidad?
- ¿Quién tiene experiencia en gestión de proyectos?
- ¿Donde estudió?

## Componentes Técnicos

### main.py
- **Función**: Coordinador principal del sistema
- **Responsabilidades**:
  - Carga de documentos
  - Construcción de base de datos vectorial
  - Interfaz de usuario interactiva
  - Manejo de comandos de salida

### resume_processor.py
- **Función**: Procesamiento de documentos
- **Responsabilidades**:
  - Extracción de texto de PDFs
  - Extracción de texto de archivos DOCX
  - Validación de archivos y manejo de errores
  - Filtrado de contenido vacío

### qa_engine.py
- **Función**: Motor de preguntas y respuestas
- **Responsabilidades**:
  - Conversión de texto a embeddings vectoriales
  - Búsqueda semántica por similitud coseno
  - Generación de respuestas con GPT-4o
  - Manejo de rate limits y errores de API

## Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **OpenAI API**: 
  - `text-embedding-3-small` para embeddings
  - `gpt-4o-mini` para generación de respuestas
- **PyPDF2**: Procesamiento de archivos PDF
- **python-docx**: Procesamiento de archivos DOCX
- **NumPy**: Operaciones vectoriales y matemáticas

## Parámetros de Configuración

En `qa_engine.py` puedes ajustar:

```python
MAX_CHARS = 2000    # Tamaño máximo de cada fragmento de texto
TOP_K = 5          # Número de fragmentos más relevantes a usar
```

## Cómo Funciona el Motor de preguntas y respuestas

1. **División**: Los documentos se dividen en fragmentos de 2000 caracteres
2. **Embeddings**: Cada fragmento se convierte en un vector numérico
3. **Búsqueda**: La pregunta se convierte en vector y se busca similitud
4. **Contexto**: Se seleccionan los 5 fragmentos más relevantes
5. **Generación**: GPT-4o genera una respuesta basada en el contexto

## Limitaciones y Consideraciones

- **API Key**: Requiere una clave válida de OpenAI
- **Costo**: Cada consulta genera costos en la API de OpenAI
- **Tamaño**: Documentos muy grandes pueden ser costosos de procesar




---


