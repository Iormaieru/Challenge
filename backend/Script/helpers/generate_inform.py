import logging
from collections import Counter

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from unidecode import unidecode


class GenerateInform:
    def __init__(self):
        pass

    def get_article_details(self, articles):
        """
        Obtiene los detalles de los artículos (título y URL).
        """
        article_details = []
        try:
            for article in articles:
                article_info = {
                    "title": article["title"],
                    "resumme": article["description"],
                    "url": article["url"],
                }
                article_details.append(article_info)
        except Exception as e:
            print(f"Error al obtener detalles de los artículos: {str(e)}")
        return article_details

    def calculate_top_keywords(self, articles, top_n=10):
        """
        Calcula las 10 palabras clave más frecuentes en los artículos.
        """
        try:
            keywords_freqs = self.get_top_keywords(articles)
            top_keywords = [
                {"keyword": key, "frequency": value}
                for key, value in keywords_freqs.items()
            ][:top_n]
        except Exception as e:
            print(f"Error al calcular las palabras clave más frecuentes: {str(e)}")
            top_keywords = []
        return top_keywords

    def calculate_popular_topics(self, articles, top_n=5):
        """
        Calcula los 5 temas más populares basados en la categoría de los artículos.
        """
        try:
            topic_counter = Counter()
            for article in articles:
                topic_counter[article["category"]] += 1
            popular_topics = [
                {"topic": topic, "count": count}
                for topic, count in topic_counter.most_common(top_n)
            ]
        except Exception as e:
            print(f"Error al calcular los temas más populares: {str(e)}")
            popular_topics = []
        return popular_topics

    def calculate_category_distribution(self, articles):
        """
        Calcula la distribución de artículos por categoría.
        """
        category_distribution = {}
        try:
            for article in articles:
                category = article["category"]
                if category in category_distribution:
                    category_distribution[category] += 1
                else:
                    category_distribution[category] = 1
        except Exception as e:
            print(
                f"Error al calcular la distribución de artículos por categoría: {str(e)}"
            )
            category_distribution = {}
        return category_distribution

    def calculate_publication_frequency(self, sources, articles, top_n=5):
        """
        Calcula la frecuencia de publicación por fuente de noticias.
        """
        publication_frequency = {}
        try:
            for article in articles:
                source = article["source"]
                if source in publication_frequency:
                    publication_frequency[source] += 1
                else:
                    publication_frequency[source] = 1

            sorted_sources = sorted(
                publication_frequency.items(), key=lambda x: x[1], reverse=True
            )
            active_sources = {source[0]: source[1] for source in sorted_sources[:top_n]}
        except Exception as e:
            print(
                f"Error al calcular la frecuencia de publicación por fuente de noticias: {str(e)}"
            )
            active_sources = {}

        return active_sources

    def get_active_sources(self, publication_frequency, top_n=5):
        """
        Obtiene las fuentes de noticias más activas.
        """
        try:
            sorted_sources = sorted(
                publication_frequency.items(), key=lambda x: x[1], reverse=True
            )
            active_sources = {source[0]: source[1] for source in sorted_sources[:top_n]}
        except Exception as e:
            print(f"Error al obtener las fuentes de noticias más activas: {str(e)}")
            active_sources = {}
        return active_sources

    def get_top_keywords(self, articles, max_features=10):
        """
        Obtiene las 10 palabras clave más frecuentes en los artículos.
        """
        try:
            texts = []
            for article in articles:
                title = article["title"] if "title" else ""
                content = article["content"] if "content" else ""
                description = article["description"] if "description" else ""
                full_text = f"{title} {content} {description}"
                texts.append(full_text)

            logging.info(f"Full texts: {texts}")

            texts = [unidecode(text).lower() for text in texts]

            stop_words = stopwords.words("spanish")
            custom_stop_words = [
                "más",
                "mas",
                "muy",
                "de",
                "y",
                "la",
                "el",
                "que",
                "en",
                "a",
                "los",
                "las",
                "con",
                "para",
                "por",
                "es",
                "un",
                "una",
                "se",
                "no",
                "al",
                "del",
                "primer",
                "segundo",
                "tercer",
                "cuarto",
                "quinto",
                "sexto",
                "séptimo",
                "octavo",
                "noveno",
            ]
            stop_words.extend(custom_stop_words)

            vectorizer = CountVectorizer(
                stop_words=stop_words, max_features=max_features
            )
            X = vectorizer.fit_transform(texts)
            keywords = vectorizer.get_feature_names_out()
            word_counts = X.toarray().sum(axis=0)
            keyword_freqs = {keywords[i]: word_counts[i] for i in range(len(keywords))}
            sorted_keywords = dict(
                sorted(keyword_freqs.items(), key=lambda item: item[1], reverse=True)
            )
            logging.info(f"Sorted keywords: {sorted_keywords}")
        except Exception as e:
            logging.error(
                f"Error al obtener las palabras clave más frecuentes: {str(e)}"
            )
            sorted_keywords = {}
        return sorted_keywords
