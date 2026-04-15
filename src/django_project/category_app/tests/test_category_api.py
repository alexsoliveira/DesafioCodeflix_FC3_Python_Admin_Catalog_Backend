from django.test import TestCase
from rest_framework.test import APITestCase
from django_project.category_app.repository import DjangoORMCategoryRepository
from core.category.domain.category import Category

class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        category_movie=Category(
            name="Filme",
            description="Categoria para filmes",
        )
        category_documentario=Category(
            name="Documentário",
            description="Categoria para documentários",
        )
        repository = DjangoORMCategoryRepository()
        repository.save(category_movie)
        repository.save(category_documentario)
              
        url = "/api/categories/"
        response = self.client.get(url)
        
        expected_data = [
            {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active
            },
            {
                "id": str(category_documentario.id),
                "name": category_documentario.name,
                "description": category_documentario.description,
                "is_active": category_documentario.is_active
            }
        ]
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.data, expected_data)

