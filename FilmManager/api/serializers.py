from rest_framework import serializers

from UWEFlix.models import *


class CreateFilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['title', 'trailer']


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'
