from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Quest, QuestCompletion, Report, Tag, Ticket, TicketIssuance, Review

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class QuestSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    imgUrl = serializers.URLField(required=False, allow_blank=True)
    exampleUrl = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = Quest
        fields = ['id', 'title', 'description', 'location', 'badget', 'date_created', 'tags', 'imgUrl', 'exampleUrl']
        read_only_fields = ('id', 'date_created')

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        quest = Quest.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'])
            quest.tags.add(tag)
        return quest

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'])
            instance.tags.add(tag)
        return instance

class QuestCompletionSerializer(serializers.ModelSerializer):
    quest = QuestSerializer(read_only=True)

    class Meta:
        model = QuestCompletion
        fields = ['id', 'user', 'quest', 'completion_date', 'media']

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