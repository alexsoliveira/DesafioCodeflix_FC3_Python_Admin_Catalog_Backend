import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.video.domain.value_objects import Rating
from src.django_project.cast_member_app.models import CastMember as CastMemberModel
from src.django_project.category_app.models import Category as CategoryModel
from src.django_project.genre_app.models import Genre as GenreModel
from src.django_project.video_app.models import Video as VideoModel
from src.django_project.video_app.repository import DjangoORMVideoRepository


@pytest.mark.django_db(transaction=True)
class TestCreateVideoWithoutMedia:
    def setup_method(self):
        VideoModel.objects.all().delete()
        GenreModel.objects.all().delete()
        CategoryModel.objects.all().delete()
        CastMemberModel.objects.all().delete()

    def test_user_can_create_video_without_media(self) -> None:
        api_client = APIClient()

        category_id = api_client.post(
            "/api/categories/", data={"name": "Filme", "description": "Categoria para filmes"}
        ).data["id"]
        genre_id = api_client.post(
            "/api/genres/", data={"name": "Drama", "categories": [str(category_id)]}
        ).data["id"]
        cast_member_id = api_client.post(
            "/api/cast_members/", data={"name": "Keanu Reeves", "type": "ACTOR"}
        ).data["id"]

        response = api_client.post(
            "/api/videos",
            data={
                "title": "title",
                "description": "description",
                "year_launched": 2019,
                "opened": True,
                "rating": "L",
                "duration": 1,
                "categories_id": [str(category_id)],
                "genres_id": [str(genre_id)],
                "cast_members_id": [str(cast_member_id)],
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert list(response.data.keys()) == ["id"]

        saved_video = DjangoORMVideoRepository().get_by_id(response.data["id"])
        assert saved_video is not None
        assert saved_video.title == "title"
        assert saved_video.description == "description"
        assert saved_video.launch_year == 2019
        assert saved_video.opened is True
        assert saved_video.published is False
        assert saved_video.rating == Rating.L
        assert saved_video.duration == 1
        assert {str(i) for i in saved_video.categories} == {str(category_id)}
        assert {str(i) for i in saved_video.genres} == {str(genre_id)}
        assert {str(i) for i in saved_video.cast_members} == {str(cast_member_id)}

    def test_user_gets_errors_when_related_entities_do_not_exist(self) -> None:
        api_client = APIClient()

        response = api_client.post(
            "/api/videos",
            data={
                "title": "title",
                "description": "description",
                "year_launched": 2019,
                "opened": True,
                "rating": "L",
                "duration": 1,
                "categories_id": [str(uuid.uuid4())],
                "genres_id": [str(uuid.uuid4())],
                "cast_members_id": [str(uuid.uuid4())],
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == (
            "Categories with provided IDs not found,"
            "Cast members with provided IDs not found,"
            "Genres with provided IDs not found"
        )
        assert VideoModel.objects.count() == 0

    def test_user_gets_errors_when_payload_is_invalid(self) -> None:
        response = APIClient().post(
            "/api/videos",
            data={"title": "", "rating": "INVALID"},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert set(response.data.keys()) == {
            "title", "description", "year_launched", "rating", "duration"
        }
        assert VideoModel.objects.count() == 0
