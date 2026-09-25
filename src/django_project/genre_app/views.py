from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, 
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT
)
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.serializers import ListGenreOutputSerializer
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.django_project.genre_app.serializers import CreateGenreInputSerializer
from src.django_project.genre_app.serializers import CreateGenreOutputSerializer
from src.core.genre.application.exceptions import InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.django_project.genre_app.serializers import DeleteGenreInputSerializer
from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.django_project.genre_app.serializers import UpdateGenreInputSerializer


class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request):
        use_case = ListGenre(repository=DjangoORMGenreRepository())
        output: ListGenre.Ouput = use_case.execute(input=ListGenre.Input())
        response_serializer = ListGenreOutputSerializer(output)

        return Response(
            status=HTTP_200_OK, 
            data=response_serializer.data
        )
    
    def create(self, request: Request) -> Response:
        serializer = CreateGenreInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateGenre.Input(**serializer.validated_data)
        use_case = CreateGenre(
            repository=DjangoORMGenreRepository(), 
            category_repository=DjangoORMCategoryRepository()
        )
        try:
            output = use_case.execute(input)
        except(InvalidGenre, RelatedCategoriesNotFound) as err:
            return Response(data={"error": str(err)}, status=HTTP_400_BAD_REQUEST)

        return Response(
            status=HTTP_201_CREATED, 
            data=CreateGenreOutputSerializer(instance=output).data
        )
    
    def update(self, request: Request, pk=None) -> Response:
        serializer = UpdateGenreInputSerializer(
            data={
                **request.data,
                "id": pk,
            }
        )
        serializer.is_valid(raise_exception=True)

        input = UpdateGenre.Input(**serializer.validated_data)
        use_case = UpdateGenre(
            repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository()
        )
        try:
            use_case.execute(request=input)
        except (InvalidGenre, RelatedCategoriesNotFound) as err:
            return Response(data={"error": str(err)}, status=HTTP_400_BAD_REQUEST)
        except GenreNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        

        return Response(status=HTTP_204_NO_CONTENT)
    
    def destroy(self, request: Request, pk=None) -> Response:
        serializer = DeleteGenreInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = DeleteGenre.Input(**serializer.validated_data)
        use_case = DeleteGenre(repository=DjangoORMGenreRepository())
        try:
            use_case.execute(input)
        except GenreNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    # def partial_update(self, request: Request, pk: UUID=None) -> Response:
    #     serializer = UpdateCategoryRequestSerializer(
    #         data={            
    #             **request.data,
    #             "id": pk,
    #         }, partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)

    #     input = UpdateCategoryRequest(**serializer.validated_data)
    #     use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
    #     try:
    #         use_case.execute(request=input)
    #     except CategoryNotFound:
    #         return Response(status=HTTP_404_NOT_FOUND)
        

    #     return Response(status=HTTP_204_NO_CONTENT)

