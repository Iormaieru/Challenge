import json
import logging
import os
import uuid

from api.models.article import Article
from api.models.source import Source
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from functions.generate_inform import GenerateInform
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class GenerateReportAndDownload(APIView):
    @csrf_exempt
    def get(self, request):
        try:
            articles = Article.objects.all()
            sources = Source.objects.all()
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
            }

            unique_filename = str(uuid.uuid4())[:5]

            json_filename = os.path.join(
                os.path.dirname(__file__),
                f"../../data/download/{unique_filename}_data_summary.json",
            )
            json_filename = os.path.abspath(json_filename)

            with open(json_filename, "w") as json_file:
                json.dump(data_summary, json_file)
            logging.info("Data summary JSON created.")

            with open(json_filename, "r") as json_file:
                response = HttpResponse(
                    json_file.read(), content_type="application/json"
                )
                response["Content-Disposition"] = (
                    "attachment; filename=data_summary.json"
                )
                logging.info("Prepared JSON file for download.")
                return response

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

        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"Error creating or reading JSON file: {e}")
            return Response(
                {"error": "Error processing JSON file."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
