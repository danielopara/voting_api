from rest_framework import serializers
from .models import Poll

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model= Poll
        fields = '__all__'
    
    def create(self, validated_data):
        return Poll.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            start_date=validated_data['start_date'],
            end_data=validated_data['end_date'],
        )