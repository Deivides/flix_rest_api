from django.db.models import Avg
from rest_framework import serializers
from actors.serializers import ActorSerializers
from movies.models import Movie
from genres.serializers import GenreSerializer


class MovieModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'

    def validate_release_date(self, value):
        if value.year < 1900:
            raise serializers.ValidationError('the previous release date may be before 1990')
        return value

    def validate_resume(self, value):
        if len(value) > 500:
            raise serializers.ValidationError('resume cannot be longer than 200 characters')
        return value


class MovieListDetailSerializer(serializers.ModelSerializer):
    actors = ActorSerializers(many=True)
    genre = GenreSerializer()
    rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'actors', 'release_date', 'rate', 'resume']

    def get_rate(self, obj):
        rate = obj.reviews.aggregate(Avg('stars'))['stars__avg']

        if rate:
            return round(rate, 1)
        return None
