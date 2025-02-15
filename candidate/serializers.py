from rest_framework import serializers
from .models import Candidate
from voting_api.utils import create_unique_id

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'
        read_only_fields = ('candidates_id',)
        
    def create(self, validated_data):
        candidates_id = create_unique_id("CND", Candidate, "candidates_id")
        return Candidate.objects.create( candidates_id=candidates_id, poll=validated_data['poll'], candidate=validated_data['candidate'])