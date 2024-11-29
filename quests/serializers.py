from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Quest, QuestCompletion, Report, SavedQuest, Tag, Ticket, TicketIssuance, Review, TravelPlan

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class QuestListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Quest
        fields = ['id', 'title', 'imgUrl', 'tags']  # 必要最小限のフィールド

class QuestDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Quest
        fields = [
            'id', 'title', 'description', 'tips', 'location', 'badget', 
            'date_created', 'tags', 'imgUrl', 'exampleUrl', 
            'latitude', 'longitude'  # latitudeとlongitudeを追加
        ]

class QuestCompletionSerializer(serializers.ModelSerializer):
    quest = QuestDetailSerializer(read_only=True)

    class Meta:
        model = QuestCompletion
        fields = ['id', 'user', 'quest', 'completion_date', 'media']

class SavedQuestSerializer(serializers.ModelSerializer):
    quest = QuestDetailSerializer(read_only=True)
    
    class Meta:
        model = SavedQuest
        fields = '__all__'
        
class TravelPlanSerializer(serializers.ModelSerializer):
    quests = QuestDetailSerializer(many=True)

    class Meta:
        model = TravelPlan
        fields = '__all__'

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