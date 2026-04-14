from django.test import TestCase
from rest_framework.test import APITestCase

class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        url = "/api/categories/"
        response = self.client.get(url)
        
        expected_data = [
            {
                "id": "9b1c9e5e-8c3a-4d9b-9f0a-1a2b3c4d5e6f",
                "name": "Filme",
                "description": "Categoria para filmes",
                "is_active": True
            },
            {
                "id": "1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p",
                "name": "Série",
                "description": "Categoria para séries",
                "is_active": True
            }
        ]
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.data, expected_data)

