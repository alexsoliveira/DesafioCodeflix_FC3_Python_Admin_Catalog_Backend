import uuid
from django.db import models
from uuid import uuid4

class Genre(models.Model):
    app_label = 'genre_app'

    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=255)
    categories = models.ManyToManyField('category_app.Category', related_name='genres')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'genres'
