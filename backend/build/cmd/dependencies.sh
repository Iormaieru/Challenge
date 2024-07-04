#!/bin/bash

echo "Installing dependencies..."

# Instalar dependencias
pip install -r requirements.txt

# Descargar modelos de spaCy
python3 -m spacy download es_core_news_sm

# Descargar recursos de NLTK
python3 -m nltk.downloader stopwords
python3 -m nltk.downloader words
python3 -m nltk.downloader punkt
python3 -m nltk.downloader vader_lexicon

# Descargar recursos de TextBlob
python3 -m textblob.download_corpora

# Actualizar setuptools y wheel
pip install -U setuptools wheel

echo "Dependencies installed successfully!"
