from rest_framework import serializers
from .models import Votes
from candidate.models import Candidate
from voting_api.utils import create_unique_id
from django.shortcuts import get_object_or_404

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields = '__all__'
        read_only_fields = ('votes_id', 'poll')
    
    def create(self, validated_data):
        voters_id = create_unique_id("VOT", Votes, "votes_id")
        # candidate = get_object_or_404(Candidate, candidates_id=validated_data['candidate'])
        candidate = validated_data['candidate']
        poll=candidate.poll
        return Votes.objects.create(
            votes_id=voters_id,
            poll=poll,
            candidate=candidate,
            voter=validated_data['voter']
        )