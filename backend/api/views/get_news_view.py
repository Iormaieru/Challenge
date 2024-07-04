from datetime import datetime

from api.models.article import Article
from api.models.source import Source
from django.views.decorators.csrf import csrf_exempt
from functions.get_news import NewsAPIFetcher
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class GetNewsView(APIView):
    @csrf_exempt
    def get(self, request):
        date_new = datetime.now().strftime("%Y-%m-%d")
        query_new = ["apple", "tesla"]
        for query in query_new:
            result = NewsAPIFetcher().get_news(date=date_new, query=query)

        if isinstance(result, dict) and "error" in result:
            return Response(
                {"error": result["error"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        articles = result

        if not articles:
            return Response(
                {"error": "No articles found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        for item in articles:
            source_data = item["source"]
            source_id = source_data.get("id")
            source_name = source_data.get("name")

            if not source_id:
                source_id = source_name

            source, _ = Source.objects.get_or_create(
                id_str_new=source_id, defaults={"name": source_name}
            )

            article, created = Article.objects.update_or_create(
                title=item["title"],
                defaults={
                    "source": source,
                    "author": item.get("author"),
                    "description": item.get("description"),
                    "url": item["url"],
                    "url_to_image": item.get("urlToImage"),
                    "published_at": item["publishedAt"],
                    "content": item.get("content"),
                },
            )

        return Response(
            {"message": "News fetched and stored successfully", "articles": articles},
            status=status.HTTP_200_OK,
        )
