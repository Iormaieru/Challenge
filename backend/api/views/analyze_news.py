import logging

from api.models.article import Article
from api.models.source import Source
from django.views.decorators.csrf import csrf_exempt
from functions.analyze_news import ArticleAnalyzer, SourceAnalyzer
from functions.generate_inform import GenerateInform
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class AnalyzeNews(APIView):
    @csrf_exempt
    def get(self, request):
        try:
            articles = Article.objects.all()
            sources = Source.objects.all()
            logging.info("Fetched all articles and sources.")

            article_analyzer = ArticleAnalyzer(articles)
            source_analyzer = SourceAnalyzer(sources, articles)
            keyword_topics = GenerateInform()

            category_distribution = article_analyzer.calculate_category_distribution()
            keywords = keyword_topics.calculate_top_keywords(articles, 10)
            logging.info("Calculated top keywords.")
            for i in range(len(keywords)):
                keywords[i] = keywords[i].items()
                keywords[i] = dict(keywords[i])
                keywords[i]["frequency"] = int(keywords[i]["frequency"])

            publication_frequency = source_analyzer.calculate_publication_frequency()

            logging.info("Analyses completed successfully.")
            return Response(
                {
                    "category_distribution": category_distribution,
                    "popular_topics": keywords,
                    "publication_frequency": publication_frequency,
                },
                status=status.HTTP_200_OK,
            )

        except Article.DoesNotExist as e:
            logging.error(f"Error fetching articles: {e}")
            return Response(
                {"error": "Error fetching articles."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Source.DoesNotExist as e:
            logging.error(f"Error fetching sources: {e}")
            return Response(
                {"error": "Error fetching sources."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
