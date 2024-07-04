import logging

from api.models.article import Article
from django.views.decorators.csrf import csrf_exempt
from functions.analyze_sentiments import SentimentAnalyzer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class AnalyzeSentimentsView(APIView):
    @csrf_exempt
    def get(self, request):
        try:
            articles = Article.objects.all()
            logging.info("Fetched all articles.")

            sentiment_analyzer = SentimentAnalyzer()

            articles_info = []
            for article in articles:
                try:
                    sentiment = sentiment_analyzer.analyze_sentiment(article.title)
                    articles_info.append(
                        {
                            "title": article.title,
                            "sentiment": sentiment,
                        }
                    )
                except Exception as e:
                    logging.error(
                        f"Error analyzing sentiment for article '{article.title}': {e}"
                    )

            logging.info("Analyzed sentiments for articles.")
            return Response({"articles": articles_info}, status=status.HTTP_200_OK)

        except Article.DoesNotExist as e:
            logging.error(f"Error fetching articles: {e}")
            return Response(
                {"error": "Error fetching articles."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
