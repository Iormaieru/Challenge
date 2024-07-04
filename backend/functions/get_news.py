import logging

import pandas as pd
import requests
from core.settings import config
from newsapi import NewsApiClient

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class NewsAPIFetcher:
    def __init__(self):
        try:
            self.base_url = "https://newsapi.org/v2/top-headlines"
            self.api_key = config("NEWS_API_KEY")
            logging.info("NewsAPIFetcher initialized successfully.")
        except Exception as e:
            logging.error(f"Error initializing NewsAPIFetcher: {e}")
            raise

    def get_news(self, query=None, date=None):
        url = f"{self.base_url}?q={query}&from={date}&to={date}&sortBy=popularity&apiKey={self.api_key}"
        logging.info(f"Fetching news from URL: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()
            logging.info("News data fetched successfully from NewsAPI.")

            data = response.json()
            if data.get("status") != "ok":
                logging.error(
                    f"NewsAPI error: {data.get('message', 'Unknown error occurred')}"
                )
                return {"error": data.get("message", "Unknown error occurred")}

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
