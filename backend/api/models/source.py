from django.db import models


class Source(models.Model):
    id_str_new = models.CharField(max_length=100, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
