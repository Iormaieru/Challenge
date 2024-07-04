#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.urls import re_path

from .views.analyze_news import AnalyzeNews
from .views.analyze_sentimients_views import AnalyzeSentimentsView
from .views.generate_report_and_download import GenerateReportAndDownload
from .views.get_news_view import GetNewsView
from .views.get_popular_and_categories_news import GetPopularAndCategoriesNews

app_name = "api"

urlpatterns = [
    re_path(
        r"^v1/get-news/$",
        GetNewsView.as_view(),
        name="get_news",
    ),
    re_path(
        r"^v1/get-popular-and-categories-news/$",
        GetPopularAndCategoriesNews.as_view(),
        name="get_popular_and_categories_news",
    ),
    re_path(
        r"^v1/analyze-news/$",
        AnalyzeNews.as_view(),
        name="analyze_news",
    ),
    re_path(
        r"^v1/analyze-sentiments/$",
        AnalyzeSentimentsView.as_view(),
        name="analyze_sentiments",
    ),
    re_path(
        r"^v1/generate-report-and-download/$",
        GenerateReportAndDownload.as_view(),
        name="generate_report_and_download",
    ),
]
