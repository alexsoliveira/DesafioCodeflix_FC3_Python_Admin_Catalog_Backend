import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_create_and_edit_category(self) -> None:
        api_client = APIClient()
    
        # Verifica que lista de categorias está vazia
        list_response = api_client.get('/api/categories/')
        assert list_response.data == {"data": []}

        # Cria uma categoria
        create_response = api_client.post(''
            '/api/categories/', 
            data={
                'name': 'Filme', 
                'description': 'Categoria para filmes'
            },
        )
        assert create_response.status_code == 201
        created_category_id = create_response.data["id"]
    
        # Verifica que categoria apareceu na listagem
        list_response = api_client.get('/api/categories/')
        assert list_response.data == {
            "data": [
                {
                    "id": str(created_category_id),
                    "name": "Filme",
                    "description": "Categoria para filmes",
                    "is_active": True
                }
            ]
        }

        # Edita a categoria criada
        update_response = api_client.put(
            f'/api/categories/{created_category_id}/',
            data={
                'name': 'Filme', 
                'description': 'Categoria para filmes',
                'is_active': False
            }
        )
        assert update_response.status_code == 204

        # Verifica que categoria foi editada aparecendo na listagem
        list_response = api_client.get('/api/categories/')
        assert list_response.data == {
            "data": [
                {
                    "id": str(created_category_id),
                    "name": "Filme",
                    "description": "Categoria para filmes",
                    "is_active": False
                }
            ]
        }