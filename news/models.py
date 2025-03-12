# news/models.py
from django.db import models

class News(models.Model):
    headline = models.CharField(max_length=255)
    link = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    images = models.URLField(null=True)

    def __str__(self):
        return self.headline
