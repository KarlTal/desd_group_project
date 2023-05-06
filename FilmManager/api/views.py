import requests
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *


# API endpoint for getting all films.
@api_view(['GET'])
def get_films(request):
    films = Film.objects.all()
    serializer = FilmSerializer(films, many=True)
    return Response(serializer.data)


# API endpoint for adding a new film.
@api_view(['POST'])
def add_film(request):
    serializer = CreateFilmSerializer(data=request.data)

    if serializer.is_valid():
        # Fetch film data using the title provided in the form
        film_name = serializer.validated_data['title']
        film_data = get_film_info(film_name)

        if film_data is not None:
            # Update serializer data with fetched film data
            serializer.validated_data.update(film_data)

            # Save the Film instance
            film_instance = serializer.save()
            film_instance.trailer = film_instance.trailer.replace('watch?v=', 'embed/')

            # Save the image file
            film_instance.image.save(f"{film_name}.jpg", film_data['image'])
            film_instance.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Invalid film title. No data found."}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_410_GONE)


# API endpoint for deleting a film.
@api_view(['POST'])
def delete_film(request):
    film_id = request.data.get('id', None)

    if not film_id:
        return Response({"error": "No film id provided."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        film = Film.objects.get(id=film_id)
        film.delete()
        return Response({"message": "Film deleted successfully."}, status=status.HTTP_200_OK)
    except Film.DoesNotExist:
        return Response({"error": "Film not found."}, status=status.HTTP_404_NOT_FOUND)


# API endpoint for updating a film.
@api_view(['POST'])
def update_film(request):
    film_id = request.data.get('id', None)

    if not film_id:
        return Response({"error": "No film id provided."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        film = Film.objects.get(id=film_id)
    except Film.DoesNotExist:
        return Response({"error": "Film not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = FilmSerializer(film, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Request film data from the OMDb API endpoint.
def get_film_info(film_name):
    api_key = "45b608d"

    response = requests.get(f"http://www.omdbapi.com/?t={film_name}&apikey={api_key}")
    data = response.json()

    try:
        # Download the image
        image_response = requests.get(data['Poster'])

        # Create a Django File object
        image_file = ContentFile(image_response.content)

        film_data = {
            'age_rating': data['Rated'],
            'duration': int(data['Runtime'].split()[0]),  # Convert runtime from string to integer
            'description': data['Plot'],
            'image': image_file,
        }

        return film_data
    except:
        return None
