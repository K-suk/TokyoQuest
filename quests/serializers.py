from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Quest, QuestCompletion, Report, Tag, Ticket, TicketIssuance, Review

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class QuestSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Quest
        fields = ['id', 'title', 'description', 'location', 'badget', 'date_created', 'tags', 'imgUrl', 'exampleUrl']

class QuestCompletionSerializer(serializers.ModelSerializer):
    quest = QuestSerializer(read_only=True)

    class Meta:
        model = QuestCompletion
        fields = ['id', 'user', 'quest', 'completion_date']

class ReportSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'user', 'report_date', 'content']

class TicketIssuanceSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TicketIssuance
        fields = ['id', 'user', 'issue_date', 'used']

class TicketSerializer(serializers.ModelSerializer):
    issued_to = UserSerializer(many=True)

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'level', 'link', 'issued_to']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    quest = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'quest', 'rating', 'comment', 'created_at']