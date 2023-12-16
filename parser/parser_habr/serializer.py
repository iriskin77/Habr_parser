from rest_framework import serializers
from .models import Hub, Author, Texts


class TextsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Texts
        fields = '__all__'

class Authorerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'

class HubSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hub
        fields = '__all__'
