import json
import time
from uuid import UUID

import pika
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient

from src.core.video.domain.value_objects import MediaStatus
from src.django_project.cast_member_app.models import CastMember as CastMemberModel
from src.django_project.category_app.models import Category as CategoryModel
from src.django_project.genre_app.models import Genre as GenreModel
from src.django_project.video_app.models import Video as VideoModel
from src.django_project.video_app.repository import DjangoORMVideoRepository


@pytest.mark.django_db(transaction=True)
class TestVideoProcessingE2E:
    def setup_method(self):
        VideoModel.objects.all().delete()
        GenreModel.objects.all().delete()
        CategoryModel.objects.all().delete()
        CastMemberModel.objects.all().delete()

    def test_full_video_processing_flow(self) -> None:
        api_client = APIClient()

        # 1. Setup de Entidades: Criar instâncias de Category, Genre e CastMember via APIs
        category_response = api_client.post(
            "/api/categories/",
            data={"name": "Ação", "description": "Categoria de filmes de ação"},
            format="json",
        )
        assert category_response.status_code == status.HTTP_201_CREATED
        category_id = category_response.data["id"]

        genre_response = api_client.post(
            "/api/genres/",
            data={"name": "Aventura", "categories": [str(category_id)]},
            format="json",
        )
        assert genre_response.status_code == status.HTTP_201_CREATED
        genre_id = genre_response.data["id"]

        cast_member_response = api_client.post(
            "/api/cast_members/",
            data={"name": "Keanu Reeves", "type": "ACTOR"},
            format="json",
        )
        assert cast_member_response.status_code == status.HTTP_201_CREATED
        cast_member_id = cast_member_response.data["id"]

        # 2. Criação do Vídeo: Criar um Video utilizando a API de vídeos
        video_response = api_client.post(
            "/api/videos/",
            data={
                "title": "Matrix Resurrections",
                "description": "Ficção científica e ação",
                "year_launched": 2021,
                "opened": True,
                "rating": "L",
                "duration": 148,
                "categories_id": [str(category_id)],
                "genres_id": [str(genre_id)],
                "cast_members_id": [str(cast_member_id)],
            },
            format="json",
        )
        assert video_response.status_code == status.HTTP_201_CREATED
        video_id = video_response.data["id"]

        # Validação pós-criação no banco
        video_repository = DjangoORMVideoRepository()
        saved_video = video_repository.get_by_id(UUID(video_id))
        assert saved_video is not None
        assert saved_video.video is None
        assert saved_video.published is False

        # 3. Upload: Realizar o upload de uma mídia utilizando a API correspondente
        video_file = SimpleUploadedFile(
            name="matrix_sample.mp4",
            content=b"sample video bytes content",
            content_type="video/mp4",
        )

        upload_response = api_client.patch(
            f"/api/videos/{video_id}/",
            data={"video_file": video_file},
            format="multipart",
        )
        assert upload_response.status_code == status.HTTP_200_OK

        video_with_media = video_repository.get_by_id(UUID(video_id))
        assert video_with_media.video is not None
        assert video_with_media.video.status == MediaStatus.PENDING

        # 4. Processamento de Evento: Publicar mensagem na fila videos.converted simulando o transcoder
        queue_name = "videos.converted"
        rabbit_host = "localhost"
        rabbit_port = 5672

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbit_host, port=rabbit_port)
        )
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)

        encoded_location = "/path/to/encoded/video"
        message_payload = {
            "error": "",
            "video": {
                "resource_id": f"{video_id}.VIDEO",
                "encoded_video_folder": encoded_location,
            },
            "status": "COMPLETED",
        }

        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(message_payload),
        )
        connection.close()

        # 5. Validação: Consumir ou aguardar até que o status do video.video seja MediaStatus.COMPLETED
        # Como o startconsumer pode estar rodando ou pode ser processado pelo consumer:
        # Se startconsumer estiver rodando como processo em background, ele consome a fila e atualiza o banco.
        # Caso o teste rode sem worker externo ativo, lemos a fila com basic_get e processamos.
        processed = False
        start_time = time.time()
        timeout = 5  # segundos de tolerância para o worker ativo processar

        while time.time() - start_time < timeout:
            current_video = video_repository.get_by_id(UUID(video_id))
            if current_video and current_video.video and current_video.video.status == MediaStatus.COMPLETED:
                processed = True
                break
            time.sleep(0.5)

        if not processed:
            # Caso o processo do consumer externo não esteja ligado durante o pytest,
            # instanciamos o consumer diretamente para consumir da fila e processar:
            from src.core.video.infra.video_converted_consumer import VideoConvertedRabbitMQConsumer

            consumer = VideoConvertedRabbitMQConsumer(host=rabbit_host, queue=queue_name)
            conn = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=rabbit_port))
            ch = conn.channel()
            method_frame, header_frame, body = ch.basic_get(queue=queue_name, auto_ack=True)
            if body:
                consumer.on_message(body)
            conn.close()

        # Validação final no repositório / banco de dados
        final_video = video_repository.get_by_id(UUID(video_id))
        assert final_video is not None
        assert final_video.video is not None
        assert final_video.video.status == MediaStatus.COMPLETED
        assert final_video.video.encoded_location == encoded_location
        assert final_video.published is True
