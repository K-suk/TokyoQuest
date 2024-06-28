from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Quest, QuestCompletion, Report, Ticket, TicketIssuance, Review

class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = ['id', 'title', 'description', 'location', 'reward', 'date_created', 'tags']

class QuestCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestCompletion
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

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
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    quest = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'quest', 'rating', 'comment', 'created_at']