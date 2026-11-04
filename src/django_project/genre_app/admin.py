from django.contrib import admin

from src.django_project.genre_app.models import Genre

# Register your models here.
class GenreAdmin(admin.ModelAdmin):
    pass

admin.site.register(Genre, GenreAdmin)