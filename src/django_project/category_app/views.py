from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK

class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        return Response(status=HTTP_200_OK, data=[
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
        ]) 
