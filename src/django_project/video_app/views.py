from uuid import UUID

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from src.core._shared.infrastructure.storage.local_storage import LocalStorage
from src.core.video.application.exceptions import InvalidVideo, RelationEntitiesNotFound, VideoNotFound
from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia
from src.core.video.application.use_cases.upload_video import UploadVideo
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.django_project.video_app.serializers import (
    CreateVideoInputSerializer,
    CreateVideoOutputSerializer,
)

class VideoViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        raise NotImplementedError

    def create(self, request: Request) -> Response:
        serializer = CreateVideoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = CreateVideoWithoutMedia(
            video_repository=DjangoORMVideoRepository(),
            category_repository=DjangoORMCategoryRepository(),
            genre_repository=DjangoORMGenreRepository(),
            cast_member_repository=DjangoORMCastMemberRepository(),
        )

        try:
            output = use_case.execute(
                CreateVideoWithoutMedia.Input(**serializer.validated_data)
            )
        except (InvalidVideo, RelationEntitiesNotFound) as err:
            return Response(data={"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            data=CreateVideoOutputSerializer(output).data,
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request: Request, pk: UUID = None):
        raise NotImplementedError

    def update(self, request: Request, pk: UUID = None):
        raise NotImplementedError

    def partial_update(self, request: Request, pk: UUID = None):
        file = request.FILES["video_file"]
        content = file.read()
        content_type = file.content_type

        upload_video = UploadVideo(
            video_repository=DjangoORMVideoRepository(),
            storage_service=LocalStorage()
        )

        try:
            upload_video.execute(
                input=UploadVideo.Input(
                    video_id=pk,
                    file_name=file.name,
                    content=content,
                    content_type=content_type
                )
            )
        except VideoNotFound:
            return Response(status=404)

        return Response(status=200)