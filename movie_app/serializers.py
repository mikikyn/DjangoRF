from rest_framework import serializers
from .models import Director, Movie, Review


class ReviewSerializer(serializers.ModelSerializer):
    movies = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'movies']


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Director
        fields = ['id', 'name', 'movies_count']

    def get_movies_count(self, director):
        return director.movies.count()


class MovieSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()
    reviews = ReviewSerializer(many=True, read_only=True, required=False)
    average_rate = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'director', 'reviews', 'average_rate', 'description', 'duration']


    def get_average_rate(self, movie):
        reviews = movie.reviews.all()
        if reviews:
            sum_reviews = sum([i.stars for i in reviews])
            average = sum_reviews / len(reviews)
            return average
        return None
