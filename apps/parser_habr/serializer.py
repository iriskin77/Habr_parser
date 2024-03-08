from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework import serializers, status
from .models import Hub, Author, Texts, Task, Hub


class TextsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Texts
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'


class HubSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hub
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'


# @extend_schema(tags=["Posts"])
# @extend_schema_view(
#     retrieve=extend_schema(
#         summary="Детальная информация о посте",
#         responses={
#             status.HTTP_200_OK: HubSerializer,
#             status.HTTP_400_BAD_REQUEST: HubSerializer,
#             status.HTTP_401_UNAUTHORIZED: HubSerializer,
#             status.HTTP_403_FORBIDDEN: HubSerializer,
#             status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
#                 response=None,
#                 description='Описание 500 ответа'),
#         },
#     ),
# )
