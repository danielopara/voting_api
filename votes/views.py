from django.shortcuts import render
from .models import Votes
from app_user.models import AppUser
from candidate.models import Candidate
from poll.models import Poll
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import VoteSerializer
from rest_framework.response import Response

# Create your views here.
class VoterView():
    @api_view(['POST'])
    def create_vote(request):
        candidate_id = request.data.get('candidate')
        voter_id = request.data.get('voter')
        
            
        try:
            candidate = Candidate.objects.get(candidates_id = candidate_id)
        except Candidate.DoesNotExist:
            return Response({'status': False, 'data': "candidate does not exist"},
                            status=status.HTTP_400_BAD_REQUEST)
            
        try:
            voter = AppUser.objects.get(usr_id=voter_id)
        except AppUser.DoesNotExist:
            return Response({'status': False, 'data': "candidate does not exist"},
                            status=status.HTTP_400_BAD_REQUEST)
            
        
        if Votes.objects.filter(poll=candidate.poll, voter=voter).exists():
            return Response({'status': False, 'data': "cannot vote for 2x for a poll"},
                            status=status.HTTP_400_BAD_REQUEST)
            
        
        serializer = VoteSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            vote_response = {
                "votes_id": serializer.data['votes_id'],
                "poll": serializer.data['poll'],
                "candidate": candidate.candidate.full_name,
                "voter": voter.full_name
            }
            return Response({"success": True, "data": vote_response}, status=status.HTTP_201_CREATED)
        
        return Response({"success": False, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)            
        