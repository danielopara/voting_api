from django.db import models
from app_user.models import AppUser
from candidate.models import Candidate

# Create your models here.
class Votes(models.Model):
    votes_id=models.CharField(max_length=20, primary_key=True)
    poll=models.CharField(max_length=30)
    candidate=models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="voters")
    voter=models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="voters")
    
    def __str__(self):
        return f"{self.voter.full_name}"