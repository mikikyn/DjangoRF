from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer


class MovieReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class DirectorReviewListView(generics.ListAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


@api_view(['GET', 'PUT', 'DELETE'])
def DirectorDetailView(request, id):
    try:
        director = Director.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Director not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = DirectorSerializer(director).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = DirectorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        director.name = request.data.get('name')
        director.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=DirectorSerializer(director).data)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def DirectorCreateView(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        data = DirectorSerializer(directors, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = DirectorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        name = request.data.get('name')
        director = Director(
            name=name
        )
        director.save()

        return Response(status=status.HTTP_201_CREATED, data=DirectorSerializer(director).data)


@api_view(['GET', 'PUT', 'DELETE'])
def MovieDetailView(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieSerializer(movie).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        movie.title = request.data.get('title')
        movie.description = request.data.get('description')
        movie.duration = request.data.get('duration')
        movie.director_id = request.data.get('director_id')
        movie.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=MovieSerializer(movie).data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def MovieCreateView(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        data = MovieSerializer(instance=movies, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        duration = serializer.validated_data.get('duration')
        director = serializer.validated_data.get('director')
        movie = Movie(
            title=title,
            description=description,
            duration=duration,
            director=director
        )
        movie.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=MovieSerializer(movie).data)

@api_view(['GET', 'PUT', 'DELETE'])
def ReviewDetailView(request, id):
    try:
        review = Review.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewSerializer(review).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        review.text = request.data.get('text')
        review.stars = request.data.get('stars')
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewSerializer(review).data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def ReviewCreateView(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(instance=reviews, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        text = request.data.get('text')
        stars = request.data.get('stars')
        movie_id = request.data.get('movie_id')
        review = Review(
            text=text,
            stars=stars,
            movie_id=movie_id
        )
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewSerializer(review).data)


@api_view(['GET'])
def test_api_view(request):
    dict_ = {
        'str': 'Hello World!',
        'int': 100,
        'float': 2.77,
        'bool': True,
        'list': [1, 2, 3],
        'dict': {'key': 'value'}
    }
    return Response(data=[dict_])
