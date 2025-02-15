from django.db import models
from app_user.models import AppUser
from poll.models import Poll

# Create your models here.
class Candidate(models.Model):
    candidates_id= models.CharField(max_length=20, primary_key=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="candidates")
    candidate = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="candidates")
    
    def __str__(self):
        return f"{self.candidate.full_name} - {self.poll.title}"