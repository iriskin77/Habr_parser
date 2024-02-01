from rest_framework import serializers
from .models import Hub, Author, Texts, Task


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
