from api.models.article import Article
from django.db import DatabaseError
from django.views.decorators.csrf import csrf_exempt
from functions.categorize_news import ArticleProcessor
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class GetPopularAndCategoriesNews(APIView):
    @csrf_exempt
    def get(self, request):
        try:
            articles = Article.objects.all()
            processor = ArticleProcessor()

            articles_info = [
                {
                    "id": article.id,
                    "title": article.title,
                    "author": article.author,
                    "published_at": article.published_at,
                    "source": article.source.name,
                    "content": article.content,
                    "description": article.description,
                }
                for article in articles
            ]

            df, keywords = processor.process_articles(articles_info)

            for index, row in df.iterrows():
                article_id = row["id"]
                category = row["category"]

                article = Article.objects.get(id=article_id)
                article.category = category
                article.save()

            popular_news = df.to_dict(orient="records")
            categories = df["category"].value_counts().to_dict()

            return Response(
                {"popular_news": popular_news, "categories": categories},
                status=status.HTTP_200_OK,
            )

        except Article.DoesNotExist:
            return Response(
                {"error": "Artículo no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except DatabaseError as e:
            return Response(
                {"error": "Error en la base de datos: " + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            return Response(
                {"error": "Error inesperado: " + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
