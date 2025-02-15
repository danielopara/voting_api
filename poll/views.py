from django.shortcuts import render
from .models import Poll
from .serializers import PollSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.
class PollView():
    @api_view(['POST'])
    def create_poll(request):
        user = PollSerializer(data = request.data)
        if user.is_valid():
            user.save()
            return Response({'status': True, 'message': 'poll created successfully', 'data': user.data}, status=status.HTTP_201_CREATED)
        
        return Response({'status': False, 'message': 'poll was not created', 'errors': user.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(['GET'])
    def get_all_polls(request):
        title = request.GET.get("title")
        polls = Poll.objects.all()
        
        allowed_queries = {"title"}

        if any(query not in allowed_queries for query in request.GET.keys()):
            return Response({"message": "invalid query"}, status=status.HTTP_400_BAD_REQUEST)

        if title:
            polls = polls.filter(title__icontains=title)
        
            
        serializer = PollSerializer(polls, many=True)
        return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)