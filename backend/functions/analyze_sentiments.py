import logging

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob


class SentimentAnalyzer:
    def __init__(self):
        try:
            self.vader_analyzer = SentimentIntensityAnalyzer()
        except Exception as e:
            logging.error(f"Error al inicializar SentimentIntensityAnalyzer: {e}")
            raise

    def analyze_sentiment(self, text):
        try:
            vader_score = self.vader_analyzer.polarity_scores(text)
        except Exception as e:
            logging.error(f"Error al analizar el texto con VADER: {e}")
            raise

        try:
            text_blob_score = TextBlob(text).sentiment.polarity
        except Exception as e:
            logging.error(f"Error al analizar el texto con TextBlob: {e}")
            raise

        try:
            combined_score = (vader_score["compound"] + text_blob_score) / 2

            if combined_score >= 0.05:
                return "positivo"
            elif combined_score <= -0.05:
                return "negativo"
            else:
                return "neutral"
        except Exception as e:
            logging.error(f"Error al calcular la puntuación combinada: {e}")
            raise
