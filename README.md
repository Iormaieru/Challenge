# API para Análisis de Noticias

El presente proyecto tiene como finalidad extraer noticias de la API "NewsAPI". Al extraerlas, se continúa con un procesamiento de datos donde guardamos cada artículo con todo su contenido en una base de datos para un mejor manejo de la información.

Seguidamente, se extrae la información más relevante: título, autor, fecha, fuente y contenido. Se identifican las palabras clave más frecuentes en los títulos y contenidos, y se procede a categorizar cada noticia.

Continuando con el análisis básico, se calcula la frecuencia de publicación por fuente de noticias, se identifican los 5 temas más populares y se determina la distribución de artículos por categoría.

Se procede al análisis de los sentimientos de cada noticia, con una IMPORTANTE salvedad: el análisis se realiza con librerías entrenadas. Para obtener un mejor resultado, es necesario entrenar un modelo orientado a tal fin.

Por último, se genera un archivo JSON que contiene un resumen de los datos analizados (opté por el título y la URL de la publicación, pero se podría cambiar por el campo de preferencia), las 10 palabras clave más frecuentes, los 5 temas más populares con sus respectivos conteos, la distribución de artículos por categoría y un listado de las fuentes de noticias más activas.

El proyecto se puede correr de dos formas, de forma local y en Docker.

### Local

1. Crear un entorno virtual y activarlo.
2. Ejecutar el script `dependencies.sh`, ubicado en `backend/build/cmd/dependencies.sh`.
   - Observación: darle permiso de ejecución al script, en caso de ser necesario, con `chmod -R +x dependencies.sh`.
3. Una vez instaladas las dependencias, correr el script `run_backend.sh`, ubicado en `backend/build/cmd/run_backend.sh`.
4. Ejecutar las API con Postman o la herramienta de su preferencia.
5. Considerar que el endpoint debe apuntar a la URL `http://127.0.0.1:8000/`.
   - Observación: La ejecución en forma local utiliza la base de datos SQLite, que viene por defecto en Django.

### Docker

1. Crear el contenedor con `docker compose build --no-cache`.
2. Levantar el contenedor con `docker compose up`.
3. Ejecutar las API con Postman o la herramienta de su preferencia.
4. Considerar que el endpoint debe apuntar a la URL `http://0.0.0.0:5008/`.
   - Observación: La ejecución en Docker utiliza la base de datos PostgreSQL, que se crea en un contenedor con el proyecto.

## Descripción de API

1. **/api/v1/get-news/**: Se encarga de obtener las noticias desde la API de "News API". Limpia el contenido antes de almacenarlo en la base de datos, por ejemplo, no guarda noticias que vengan con `title=NULL o title=[Removed]` o `contenido=NULL o contenido=[Removed]`.
2. **/api/v1/analyze-news/**: Se encarga de hacer el análisis de la información, categoriza cada artículo de noticia y guarda la categoría en la base de datos. Asimismo, identifica las palabras clave más frecuentes en los títulos y contenidos.
3. **/api/v1/analyze-sentiments/**: Se encarga de clasificar las noticias como positivas, neutras o negativas. Tal como se mencionó anteriormente, se utilizan librerías con modelos preentrenados. Para una clasificación más eficiente, hay que entrenar los modelos con el fin requerido.
4. **/api/v1/generate-report-and-download/**: Se encarga de generar un informe y descargar un archivo JSON, el cual se guarda en `backend/data/download/*_data_summary.json`.

Swagger: Aquí se puede ver la documentación de la API
`http://127.0.0.1:8000/api/schema/swagger-ui/`

--------------------------------------------------------- o ---------------------------------------------------------------

# Script para obtención y análisis de artículos de NEWS API

Este script realiza la acción completa de la API desarrollada en Django, obteniendo como resultado final un archivo con su análisis.

## Pre-requisitos

Es necesario tener instalado Python 3.10 o superior.

## Forma de ejecución

1. Crear un entorno virtual y activarlo.
2. Ejecutar el script `dependencies.sh`, ubicado en `backend/build/cmd/dependencies.sh`.
   - Observación: Darle permiso de ejecución al script si es necesario con `chmod +x dependencies.sh`.
3. Una vez instaladas las dependencias, ejecutar el script `run_backend.sh`, ubicado en `backend/build/cmd/run_backend.sh`.
4. Abrir el script `app.py`, ubicado en la carpeta `backend/Script/app.py`.
5. Al final del script, añadir la API KEY.
6. Ejecutar el script.
7. El archivo final se guarda en el siguiente directorio: `backend/data/download`
