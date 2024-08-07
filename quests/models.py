# quests/models.py
from django.db import models
from django.conf import settings
from django.utils.deconstruct import deconstructible
import os
import uuid

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Quest(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    tips = models.TextField(null=True, blank=True)
    imgUrl = models.URLField(max_length=1500, null=True, blank=True)
    exampleUrl = models.URLField(max_length=1500, null=True, blank=True)
    location = models.CharField(max_length=1500)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    badget = models.CharField(max_length=1500, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='quests')

@deconstructible
class PathAndRename:
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        # 拡張子を取得
        ext = filename.split('.')[-1]
        # 新しいファイル名を生成（ここではUUIDを使用）
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        # タグ名を取得（タグが複数ある場合、最初のタグを使用）
        tag_name = instance.quest.tags.first().name if instance.quest.tags.exists() else 'default'
        # 新しいファイルパスを生成
        return os.path.join(self.path, str(instance.user.id), tag_name, filename)

path_and_rename = PathAndRename("media")

class QuestCompletion(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    completion_date = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to=path_and_rename, null=True, blank=True)
    
class SavedQuest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quest = models.ForeignKey('Quest', on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'quest')

class TravelPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quests = models.ManyToManyField(Quest, related_name='travel_plans')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name}'s Travel Plan"
    
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