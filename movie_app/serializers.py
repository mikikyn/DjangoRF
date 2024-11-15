from rest_framework import serializers
from .models import Director, Movie, Review


class ReviewSerializer(serializers.ModelSerializer):
    movies = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'movies']

    def validate_stars(self, stars):
        if stars < 1 or stars > 5:
            raise serializers.ValidationError("Значение поля 'stars' должно быть от 1 до 5.")
        return stars

    def validate_movie(self, movie):
        if not movie:
            raise serializers.ValidationError("Фильм обязателен для указания.")
        return movie

    def validate_text(self, text):
        if len(text) < 15:
            raise serializers.ValidationError("Отзыв должен содержать не менее 15 символов.")
        return text


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Director
        fields = ['id', 'name', 'movies_count']

    def get_movies_count(self, director):
        return director.movies.count()

    def validate_name(self, name):
        if len(name) < 3:
            raise serializers.ValidationError("Имя режиссера должно содержать не менее 3 символов.")
        if Director.objects.filter(name__iexact=name).exists():
            raise serializers.ValidationError("Режиссер с таким именем уже существует.")
        return name


class MovieSerializer(serializers.ModelSerializer):
    director = serializers.PrimaryKeyRelatedField(queryset=Director.objects.all())
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


    def validate_duration(self, duration):
        if duration <= 0:
            raise serializers.ValidationError("Длительность фильма должна быть больше 0.")
        return duration


    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Название фильма не может быть пустым.")
        return value


    def validate_description(self, description):
        if len(description) < 50:
            raise serializers.ValidationError("Описание фильма должно содержать не менее 50 символов.")
        return description
