from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMember,
    CreateCastMemberRequest,
)
from src.core.cast_member.application.use_cases.delete_cast_member import (
    DeleteCastMember,
    DeleteCastMemberRequest,
)
from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFound,
    InvalidCastMemberData,
)
from src.core.cast_member.application.use_cases.list_cast_member import (
    ListCastMember,
    ListCastMemberRequest,
)
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMember,
    UpdateCastMemberRequest,
)
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.serializers import (
    CreateCastMemberRequestSerializer,
    CreateCastMemberResponseSerializer,
    DeleteCastMemberRequestSerializer,
    ListCastMemberResponseSerializer,
    UpdateCastMemberRequestSerializer,
)


class CastMemberViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListCastMember(repository=DjangoORMCastMemberRepository())
        output = use_case.execute(request=ListCastMemberRequest())

        serializer = ListCastMemberResponseSerializer(instance=output)
        return Response(
            status=HTTP_200_OK,
            data=serializer.data,
        )

    def create(self, request: Request) -> Response:
        serializer = CreateCastMemberRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = CreateCastMember(repository=DjangoORMCastMemberRepository())
        input_data = CreateCastMemberRequest(**serializer.validated_data)

        try:
            output = use_case.execute(request=input_data)
        except InvalidCastMemberData as err:
            return Response(
                data={"error": str(err)},
                status=HTTP_400_BAD_REQUEST,
            )

        return Response(
            status=HTTP_201_CREATED,
            data=CreateCastMemberResponseSerializer(instance=output).data,
        )

    def update(self, request: Request, pk=None) -> Response:
        serializer = UpdateCastMemberRequestSerializer(
            data={
                **request.data,
                "id": pk,
            }
        )
        serializer.is_valid(raise_exception=True)

        use_case = UpdateCastMember(repository=DjangoORMCastMemberRepository())
        input_data = UpdateCastMemberRequest(**serializer.validated_data)

        try:
            use_case.execute(request=input_data)
        except InvalidCastMemberData as err:
            return Response(
                data={"error": str(err)},
                status=HTTP_400_BAD_REQUEST,
            )
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def destroy(self, request: Request, pk=None) -> Response:
        serializer = DeleteCastMemberRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = DeleteCastMember(repository=DjangoORMCastMemberRepository())
        input_data = DeleteCastMemberRequest(id=serializer.validated_data["id"])

        try:
            use_case.execute(request=input_data)
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)
