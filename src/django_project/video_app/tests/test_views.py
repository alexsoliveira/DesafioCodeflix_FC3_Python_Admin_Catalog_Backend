from pathlib import Path
from unittest.mock import patch
import uuid

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient

from src.core._shared.infrastructure.storage.local_storage import LocalStorage
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.core.video.domain.value_objects import MediaStatus, Rating
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
        response = APIClient().post("/api/videos/", data=payload(*related_ids), format="json")

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
        response = APIClient().post("/api/videos/", data={}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data

    def test_invalid_rating_returns_400(self, related_ids):
        response = APIClient().post(
            "/api/videos/", data=payload(*related_ids, rating="X"), format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "rating" in response.data

    def test_invalid_video_returns_400(self, related_ids):
        response = APIClient().post(
            "/api/videos/", data=payload(*related_ids, title="a" * 255 + "b"), format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_related_entities_not_found_returns_400(self):
        response = APIClient().post(
            "/api/videos/",
            data=payload(uuid.uuid4(), uuid.uuid4(), uuid.uuid4()),
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Categories with provided IDs not found" in response.data["error"]
        assert "Cast members with provided IDs not found" in response.data["error"]
        assert "Genres with provided IDs not found" in response.data["error"]


@pytest.mark.django_db
class TestUploadVideoAPI:
    def test_upload_video_media_end_to_end(self, tmp_path: Path, related_ids):
        # 1. Cria um vídeo via POST /api/videos/
        client = APIClient()
        create_response = client.post("/api/videos/", data=payload(*related_ids), format="json")
        assert create_response.status_code == status.HTTP_201_CREATED
        video_id = create_response.data["id"]

        # 2. Prepara o arquivo simulado para envio
        video_content = b"fake video content for testing"
        video_file_name = "test_video.mp4"
        uploaded_file = SimpleUploadedFile(
            name=video_file_name,
            content=video_content,
            content_type="video/mp4",
        )

        # 3. Faz o PATCH /api/videos/<id>/ com multipart/form-data usando o LocalStorage isolado no tmp_path
        with patch.object(LocalStorage, "__init__", lambda self, bucket=None: setattr(self, "_bucket", tmp_path)):
            patch_response = client.patch(
                f"/api/videos/{video_id}/",
                data={"video_file": uploaded_file},
                format="multipart",
            )

        assert patch_response.status_code == status.HTTP_200_OK

        # 4. Verifica se o vídeo foi atualizado no banco de dados com a mídia associada
        repository = DjangoORMVideoRepository()
        updated_video = repository.get_by_id(uuid.UUID(video_id))
        assert updated_video is not None
        assert updated_video.video is not None
        assert updated_video.video.name == video_file_name
        assert updated_video.video.raw_location == f"videos/{video_id}/{video_file_name}"
        assert updated_video.video.status == MediaStatus.PENDING

        # 5. Verifica se o arquivo físico foi realmente persistido no storage
        expected_saved_file = tmp_path / "videos" / video_id / video_file_name
        assert expected_saved_file.exists()
        assert expected_saved_file.read_bytes() == video_content
