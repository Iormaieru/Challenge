import json
import logging
import os
import sys
import uuid

from decouple import Config, UndefinedValueError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
env_file_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../build/env/local.env")
)
config = Config(env_file_path)

from datetime import datetime

from helpers.analyze_news import ArticleAnalyzer, SourceAnalyzer
from helpers.analyze_sentiments import SentimentAnalyzer
from helpers.categorize_news import ArticleProcessor
from helpers.generate_inform import GenerateInform
from helpers.get_news import NewsAPIFetcher


class NewsApp:
    def __init__(self, api_key):
        self.api_key = api_key
        self.fetcher = NewsAPIFetcher(api_key)
        self.articles = []
        self.sources = []
        self.sentiments = []
        self.count_sentiments = {}
        self.categories = []
        self.popular_topics = []
        self.category_distribution = {}
        self.publication_frequency = {}
        self.summary = {}
        self.inform = ""

        logging.info("NewsApp initialized with API key.")

    def fetch_news(self, query):
        try:
            for q in query:
                self.articles = self.fetcher.get_news(q)
            logging.info("Fetched %d sources.", len(self.sources))
        except Exception as e:
            logging.error(f"Error fetching news: {e}")
            raise

    def categorize_news(self):
        try:
            article_processor = ArticleProcessor()
            df, keywords = article_processor.process_articles(self.articles)
            for index, row in df.iterrows():
                title = row["title"]
                category = row["category"]
                for article in self.articles:
                    if article.get("title") == title:
                        article["category"] = category

            logging.info("Categorized news.")
        except Exception as e:
            logging.error(f"Error categorizing news: {e}")
            raise

    def analyze_news(self):
        try:
            article_analyzer = ArticleAnalyzer(self.articles)
            self.category_distribution = (
                article_analyzer.calculate_category_distribution()
            )
            self.popular_topics = article_analyzer.identify_popular_topics()
            logging.info("Analyzed news.")
        except Exception as e:
            logging.error(f"Error analyzing news: {e}")
            raise

    def analyze_sources(self):
        try:
            source_analyzer = SourceAnalyzer(self.articles)
            self.publication_frequency = (
                source_analyzer.calculate_publication_frequency()
            )
            logging.info("Analyzed sources.")
        except Exception as e:
            logging.error(f"Error analyzing sources: {e}")
            raise

    def analyze_sentiments(self):
        try:
            sentiment_analyzer = SentimentAnalyzer()
            article_sentiments = []
            count_sentiments = {"positive": 0, "neutral": 0, "negative": 0}
            for sentence in self.articles:
                if sentence:
                    title = sentence.get("title")
                    sentiments = sentiment_analyzer.analyze_sentiment(title)
                    article_sentiments.append({"title": title, "sentiment": sentiments})

                    if sentiments == "positive":
                        count_sentiments["positive"] += 1
                    elif sentiments == "neutral":
                        count_sentiments["neutral"] += 1
                    elif sentiments == "negative":
                        count_sentiments["negative"] += 1

            self.sentiments = article_sentiments
            self.count_sentiments = count_sentiments

            logging.info("Analyzed sentiments.")
        except Exception as e:
            logging.error(f"Error analyzing sentiments: {e}")
            raise

    def generate_inform(self):
        try:
            articles = self.articles
            sources = [article["source"] for article in articles]
            generate_inform = GenerateInform()

            resume_articles = generate_inform.get_article_details(articles)
            logging.info("Obtained article details.")

            keywords = generate_inform.calculate_top_keywords(articles, 10)
            logging.info("Calculated top keywords.")

            for i in range(len(keywords)):
                keywords[i] = keywords[i].items()
                keywords[i] = dict(keywords[i])
                keywords[i]["frequency"] = int(keywords[i]["frequency"])

            popular_topics = generate_inform.calculate_popular_topics(articles, 5)
            logging.info("Calculated popular topics.")

            category_distribution = generate_inform.calculate_category_distribution(
                articles
            )
            logging.info("Calculated category distribution.")

            publication_frequency = generate_inform.calculate_publication_frequency(
                sources, articles, 5
            )
            logging.info("Calculated publication frequency.")

            data_summary = {
                "resume_articles": resume_articles,
                "top_keywords": keywords,
                "popular_topics": popular_topics,
                "category_distribution": category_distribution,
                "active_sources": publication_frequency,
                "sentiments": self.count_sentiments,
            }

            unique_filename = str(uuid.uuid4())[:5]

            json_filename = os.path.join(
                os.path.dirname(__file__),
                f"../../backend/data/download/{unique_filename}_data_summary.json",
            )
            json_filename = os.path.abspath(json_filename)

            with open(json_filename, "w") as json_file:
                json.dump(data_summary, json_file)
            logging.info("Data summary JSON created.")

        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"Error creating or reading JSON file: {e}")
            raise

        except AttributeError as e:
            if str(e) == "'list' object has no attribute 'get'":
                logging.error(
                    "Error: 'self.articles' should be a list of dictionaries with 'source' key."
                )
            else:
                logging.error(f"AttributeError: {e}")
            raise

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    try:
        api_key = "4ece4c892c32445b9bb722698d2ab7b2"
        print("NEWS_API_KEY loaded successfully")
    except UndefinedValueError:
        print("Failed to load NEWS_API_KEY")
    except Exception as e:
        print(f"An error occurred: {e}")

    app = NewsApp(api_key)

    try:
        app.fetch_news(
            query=[
                "senado",
                # "congreso",
                # "futbol",
                # "wall street",
                # "virus",
                # "programación",
            ]
        )
        app.categorize_news()
        app.analyze_news()
        app.analyze_sources()
        app.analyze_sentiments()
        app.generate_inform()

        logging.info("Process completed successfully.")

    except Exception as e:
        logging.error(f"Error running NewsApp: {e}")


if __name__ == "__main__":
    main()
