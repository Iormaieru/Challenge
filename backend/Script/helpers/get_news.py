import json
import logging
import os
import sys

import pandas as pd
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
from categorize_news import ArticleProcessor

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class NewsAPIFetcher:
    def __init__(self, api_key=None):
        try:
            self.base_url = "https://newsapi.org/v2/everything"
            self.api_key = api_key
            self.articles = []
            self.article_processor = ArticleProcessor()
            logging.info("NewsAPIFetcher initialized successfully.")
        except Exception as e:
            logging.error(f"Error initializing NewsAPIFetcher: {e}")
            raise

    def get_news(self, query=None):
        url = f"{self.base_url}?q={query}&sortBy=publishedAt&language=es&apiKey={self.api_key}"
        logging.info(f"Fetching news from URL: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()

            if len(response.json()["articles"]) == 0:
                logging.info("No articles found for the given query.")

            logging.info("News data fetched successfully from NewsAPI.")

            data = response.json()
            if data.get("status") != "ok":
                logging.error(
                    f"NewsAPI error: {data.get('message', 'Unknown error occurred')}"
                )
                return {"error": data.get("message", "Unknown error occurred")}

            for article in data["articles"]:
                article["source"] = article["source"]["name"]
                article["publishedAt"] = pd.to_datetime(article["publishedAt"])
                article["content"] = article["content"].replace("\n", " ")
                article["description"] = article["description"].replace("\n", " ")

                for key in article.keys():
                    if article[key] is None:
                        article[key] = "[Removed]"

            df = pd.DataFrame(data["articles"])
            logging.info(f"DataFrame created with {len(df)} articles.")

            filtered_df = df[
                (df["title"].notnull())
                & (df["title"] != "[Removed]")
                & (df["description"].notnull())
                & (df["description"] != "[Removed]")
                & (df["content"].notnull())
                & (df["content"] != "[Removed]")
            ]
            logging.info(
                f"Filtered DataFrame created with {len(filtered_df)} articles."
            )

            filtered_data = filtered_df.to_dict(orient="records")
            return filtered_data

        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {str(e)}")
            return {"error": f"Request error: {str(e)}"}

        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return {"error": f"Error: {str(e)}"}

    def fetch_news(self, query):
        self.articles = []

        try:
            for q in query:
                articles = self.get_news(q)
                if not isinstance(articles, dict) and "error" in articles:
                    self.articles.extend(articles)

            logging.info(f"Fetched {len(self.articles)} articles in total.")

        except Exception as e:
            logging.error(f"Error fetching news: {e}")
            raise
