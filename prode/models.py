from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import timedelta

class Team(models.Model):
    name = models.CharField(max_length=50)
    flag = models.ImageField(upload_to='prode/images/flags/')
    def __str__(self):
        return self.name

class Match(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='+')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='+')
    team1_score = models.PositiveIntegerField(default=0)
    team2_score = models.PositiveIntegerField(default=0)
    def end_match(self):
        now = timezone.now() 
        return self.end <= now

    def get_endscore(self):
        winner = None
        if (self.end_match() == True):
            if (self.team1_score > self.team2_score):
                winner = self.team1
            elif (self.team1_score < self.team1_score):
                winner = self.team2
            elif (self.team1_score == self.team2_score):
                winner = "tie"
        return winner

    def is_unavailable(self):
        now = timezone.now()
        start = self.start - timedelta(hours=1)
        return now >= start

    def __str__(self):
        return (self.team1.name + " vs " + self.team2.name)
        
class Bet(models.Model):
    user = models.ForeignKey(User, related_name='bets', blank=True, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='bets') 
    team1_score = models.PositiveIntegerField(default=0)
    team2_score = models.PositiveIntegerField(default=0)
    result = models.PositiveIntegerField(default=0, null=True)

    def get_result(self):
        if (self.match.get_endscore() == self.match.team1) and (self.team1_score > self.team2_score):
            self.result = 3
        elif (self.match.get_endscore() == self.match.team2) and (self.team2_score > self.team1_score):
            self.result = 3
        elif (self.match.get_endscore() == "tie") and (self.team1_score == self.team2_score):
            self.result = 3
        elif (self.match.team1_score == self.team1_score) and (self.match.team2_score == self.team2_score):
            self.result = 6
        else: 
            self.result = 0
        return self.result

    class Meta:
        unique_together = ('user', 'match')

    def __str__(self):
        return (str(self.match))

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    global_score = models.PositiveIntegerField(default=0)
    global_ranking = models.PositiveIntegerField(default=0)
        