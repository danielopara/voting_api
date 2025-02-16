from .models import Votes
from app_user.models import AppUser
from candidate.models import Candidate
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import VoteSerializer
from rest_framework.response import Response

# Create your views here.
class VoterView():
    @api_view(['GET'])
    def get_all(request):
       poll = request.GET.get('poll')
       candidate = request.GET.get('candidate')
       
       allowed_queries = {'poll', 'candidate'}
       query_keys = set(request.GET.keys())  
       
       if query_keys - allowed_queries:
           return Response({'success': False, 'data': 'invalid query'}, status=status.HTTP_400_BAD_REQUEST)
       
       votes = Votes.objects.select_related('candidate').all()
       
       if poll:
           votes = votes.filter(poll__icontains = poll)
    
       if candidate:
           votes = votes.filter(candidate__candidate__full_name__icontains = candidate)
       
       votes_list = [
           {
               'id': vote.votes_id,
               'poll': vote.poll,
               'candidate': vote.candidate.candidate.full_name,
               'voter': vote.voter.full_name,
           } for vote in votes
       ]
       
       serializer = VoteSerializer(votes, many=True)
       return Response({'success': True, 'data': votes_list}, status=status.HTTP_200_OK)
    
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
        