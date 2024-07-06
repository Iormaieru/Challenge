import json
import os
from collections import Counter

import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from unidecode import unidecode


class ArticleProcessor:
    def __init__(self, categories_path=None):
        if categories_path is None:
            categories_path = os.path.join(
                os.path.dirname(__file__), "../../data/config/categories.json"
            )
            categories_path = os.path.abspath(categories_path)
            self.categories_path = categories_path
        else:
            self.categories_path = categories_path

        self.categories = self.load_categories()

    def load_categories(self):
        try:
            categories_path = os.path.abspath(self.categories_path)
            with open(categories_path, "r", encoding="utf-8") as file:
                categories = json.load(file)
            return categories
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo {self.categories_path}")
        except json.JSONDecodeError:
            raise ValueError(
                f"Error al decodificar el archivo JSON {self.categories_path}"
            )

    def process_articles(self, articles):
        try:
            df = pd.DataFrame.from_dict(articles)
        except ValueError as e:
            raise ValueError("Error al convertir los artículos a DataFrame: " + str(e))

        df["text"] = (
            df["title"].fillna("")
            + " "
            + df["content"].fillna("")
            + " "
            + df["description"].fillna("")
        )
        texts = [unidecode(text).lower() for text in df["text"]]

        try:
            stop_words = stopwords.words("spanish")
            vectorizer = CountVectorizer(stop_words=stop_words, max_features=10)
            X = vectorizer.fit_transform(texts)
            keywords = vectorizer.get_feature_names_out()
        except Exception as e:
            raise ValueError("Error al vectorizar los textos: " + str(e))

        df["category"] = df["text"].apply(self.categorize_article)

        return df, keywords

    def categorize_article(self, text):
        word_counter = Counter()
        for category, keywords in self.categories.items():
            count = sum(1 for keyword in keywords if keyword in text.lower())
            word_counter[category] += count

        if word_counter:
            return word_counter.most_common(1)[0][0]
        else:
            return "otros"
