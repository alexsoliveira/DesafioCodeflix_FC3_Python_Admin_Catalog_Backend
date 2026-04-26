from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, 
    HTTP_200_OK,
    HTTP_404_NOT_FOUND
)
from uuid import UUID
from core.category.application.use_cases.list_category import (
    ListCategory, 
    ListCategoryRequest,
)
from core.category.application.use_cases.exceptions import CategoryNotFound
from django_project.category_app.repository import DjangoORMCategoryRepository
from core.category.application.use_cases.get_category import (
    GetCategory, 
    GetCategoryRequest
)
from .serializers import (
    ListCategoryResponseSerializer,
    RetrieveCategoryRequestSerializer,
    RetrieveCategoryResponseSerializer
)

class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request):
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        response = use_case.execute(request=ListCategoryRequest())

        serializer = ListCategoryResponseSerializer(instance=response)
        return Response(
            status=HTTP_200_OK, 
            data=serializer.data
        )

    def retrieve(self, request: Request, pk=None):
        serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
                
        use_case = GetCategory(repository=DjangoORMCategoryRepository())

        try:
            result = use_case.execute(request=GetCategoryRequest(id=serializer.validated_data["id"]))
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        category_output = RetrieveCategoryResponseSerializer(instance=result)
        return Response(
            status=HTTP_200_OK, 
            data=category_output.data
        )