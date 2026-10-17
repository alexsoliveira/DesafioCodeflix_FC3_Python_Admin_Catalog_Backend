import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.core.video.domain.value_objects import Rating
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.video_app.repository import DjangoORMVideoRepository


@pytest.fixture
def related_ids():
    category = Category(name="Movie")
    genre = Genre(name="Drama")
    cast_member = CastMember(name="Keanu Reeves", type=CastMemberType.ACTOR)
    DjangoORMCategoryRepository().save(category)
    DjangoORMGenreRepository().save(genre)
    DjangoORMCastMemberRepository().save(cast_member)
    return category.id, genre.id, cast_member.id


def payload(category_id, genre_id, cast_member_id, **overrides):
    return {
        "title": "title",
        "description": "description",
        "year_launched": 2019,
        "opened": True,
        "rating": "L",
        "duration": 1,
        "categories_id": [str(category_id)],
        "genres_id": [str(genre_id)],
        "cast_members_id": [str(cast_member_id)],
        **overrides,
    }


@pytest.mark.django_db
class TestCreateVideoAPI:
    def test_create_video_without_media(self, related_ids):
        response = APIClient().post("/api/videos", data=payload(*related_ids), format="json")

        assert response.status_code == status.HTTP_201_CREATED
        video = DjangoORMVideoRepository().get_by_id(response.data["id"])
        assert video.title == "title"
        assert video.rating == Rating.L
        assert video.opened is True
        assert video.categories == {related_ids[0]}

    def test_accepts_trailing_slash(self, related_ids):
        response = APIClient().post("/api/videos/", data=payload(*related_ids), format="json")

        assert response.status_code == status.HTTP_201_CREATED

    def test_invalid_payload_returns_400(self):
        response = APIClient().post("/api/videos", data={}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data

    def test_invalid_rating_returns_400(self, related_ids):
        response = APIClient().post(
            "/api/videos", data=payload(*related_ids, rating="X"), format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "rating" in response.data

    def test_invalid_video_returns_400(self, related_ids):
        response = APIClient().post(
            "/api/videos", data=payload(*related_ids, title="a" * 255 + "b"), format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_related_entities_not_found_returns_400(self):
        response = APIClient().post(
            "/api/videos",
            data=payload(uuid.uuid4(), uuid.uuid4(), uuid.uuid4()),
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Categories with provided IDs not found" in response.data["error"]
        assert "Cast members with provided IDs not found" in response.data["error"]
        assert "Genres with provided IDs not found" in response.data["error"]
