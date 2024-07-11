# quests/models.py
from django.db import models
from django.conf import settings

class Tag(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Quest(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    imgUrl = models.URLField(max_length=200, null=True, blank=True)
    exampleUrl = models.URLField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200)
    badget = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='quests')

class QuestCompletion(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    completion_date = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to='media/', null=True, blank=True)
    
class Ticket(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    level = models.IntegerField(blank=True, null=True)
    link = models.CharField(max_length=100)
    issued_to = models.ManyToManyField(settings.AUTH_USER_MODEL, through='TicketIssuance', related_name='tickets')

class TicketIssuance(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    
class Review(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Report(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()