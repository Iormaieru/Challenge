import logging
from collections import Counter

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ArticleAnalyzer:
    def __init__(self, articles):
        try:
            self.articles = articles
            logging.info("ArticleAnalyzer initialized with %d articles.", len(articles))
        except Exception as e:
            logging.error(f"Error initializing ArticleAnalyzer: {e}")
            raise

    def calculate_category_distribution(self):
        try:
            category_distribution = Counter()
            for article in self.articles:
                category = article.get("category")
                category_distribution[category] += 1

            sorted_distribution = dict(
                sorted(category_distribution.items(), key=lambda x: x[1], reverse=True)
            )
            logging.info("Calculated category distribution.")
            return sorted_distribution

        except Exception as e:
            logging.error(f"Error calculating category distribution: {e}")
            raise

    def identify_popular_topics(self):
        try:
            category_counts = Counter()
            for article in self.articles:
                category = article.get("category")
                category_counts[category] += 1

            popular_topics = category_counts.most_common(5)
            logging.info("Identified popular topics.")
            return popular_topics

        except Exception as e:
            logging.error(f"Error identifying popular topics: {e}")
            raise


class SourceAnalyzer:
    def __init__(self, articles):
        try:
            self.articles = articles
            logging.info(
                "SourceAnalyzer initialized with %d sources and %d articles.",
                len(articles),
            )
        except Exception as e:
            logging.error(f"Error initializing SourceAnalyzer: {e}")
            raise

    def calculate_publication_frequency(self):
        self.sources = []
        for article in self.articles:
            source = article.get("source")
            if source not in self.sources:
                self.sources.append(source)
        try:
            publication_frequency = {}
            for source in self.sources:
                article_count = sum(
                    1 for article in self.articles if article.get("source") == source
                )
                if article_count > 0:
                    publication_frequency[source] = article_count

            sorted_frequency = dict(
                sorted(publication_frequency.items(), key=lambda x: x[1], reverse=True)
            )
            logging.info("Calculated publication frequency.")
            return sorted_frequency

        except Exception as e:
            logging.error(f"Error calculating publication frequency: {e}")
            raise
