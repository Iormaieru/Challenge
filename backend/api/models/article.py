from django.db import models

from .source import Source


class Article(models.Model):
    author = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=1000, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(max_length=1000, null=True, blank=True)
    url_to_image = models.URLField(max_length=1000, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ["title", "published_at"]
