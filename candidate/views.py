from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import CandidateSerializer
from .models import Candidate
from rest_framework.response import Response
from app_user.models import AppUser
from poll.models import Poll

# Create your views here.
@api_view(['POST'])
def create_candidate(request):
    user_id = request.data.get('candidate')
    poll_id = request.data.get('poll')
    
    try:
        user = AppUser.objects.get(usr_id=user_id)
    except AppUser.DoesNotExist:
        return Response({"status": False, "data": "user not found"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        poll = Poll.objects.get(id=poll_id)
    except Poll.DoesNotExist:
        return Response({"status": False, "data": "poll not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if Candidate.objects.filter(poll=poll, candidate=user).exists():
        return Response({"status": False, "data": "user already exists in poll"}, status=status.HTTP_400_BAD_REQUEST)
    
    candidate_data = {"poll": poll.id, "candidate": user.usr_id}
    serializer = CandidateSerializer(data=candidate_data)
    if serializer.is_valid():
        serializer.save()
        candidate = {
            "candidates_id": serializer.data['candidates_id'],
            "poll": poll.title,
            "candidate": user.full_name
        }
        return Response({"success": True, "data": candidate}, status=status.HTTP_201_CREATED)
    return Response({"success": False, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_candidate(request):
    poll = request.GET.get('poll')
    candidate = request.GET.get('candidate')
    
    allowed_queries = {'poll', 'candidate'}
    query_keys = set(request.GET.keys())
    
    if query_keys - allowed_queries:
        return Response({'message': 'invalid query'}, status=status.HTTP_400_BAD_REQUEST)
    
    candidates = Candidate.objects.select_related('poll', 'candidate').all()
    
    if poll:
        candidates = candidates.filter(poll__title__icontains = poll)
        
    if candidate:
        candidates = candidates.filter(candidate__full_name__icontains = candidate)
    candidates_list = [
        {
            "candidates_id": candidate.candidates_id,
            "poll": candidate.poll.title,
            "candidate": candidate.candidate.full_name
        } for candidate in candidates
    ]
    return Response({'success': True, 'data':candidates_list}, status=status.HTTP_200_OK)