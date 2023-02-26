from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
# Create your views here.

@api_view(['GET', 'POST']) # Add POST to the accepted methods
def books(request):
    return Response('list of books', status=status.HTTP_200_OK)


# class-based view
class BookList(APIView):
    def get(self, request):
        # from url?author=...
        author = request.GET.get('author')
        if author:
            return Response({'message': f'list of books by {author}'}, status.HTTP_200_OK)
        
        return Response({'message': 'list of books'}, status.HTTP_200_OK)
    

    def post(self, request):
        title = request.data.get('title') # get data from json sended in content textarea
        return Response({'message': f'new book created Name:{title}'}, status.HTTP_201_CREATED)

class SingleBook(APIView):
    def get(self, request, pk):
        return Response({'message':f'Book with pk(id) = {pk}'}, status.HTTP_200_OK)
    
    def put(self, request, pk):
        # get pk from url and get title from content form sended as json
        return Response({'message':f'Book with pk = {pk} and title = {request.data.get("title")}'}, 
                        status.HTTP_200_OK) 
