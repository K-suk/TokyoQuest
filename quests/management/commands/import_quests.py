import json
from django.core.management.base import BaseCommand
from quests.models import Quest, Tag

class Command(BaseCommand):
    help = 'Import quests from a JSON file'

    def handle(self, *args, **kwargs):
        with open('quests_data.json', 'r', encoding='utf-8') as file:
            quests_data = json.load(file)

        self.save_to_django(quests_data)

    def save_to_django(self, quests):
        for quest_data in quests:
            tags = quest_data.pop("tags")
            quest, created = Quest.objects.get_or_create(
                title=quest_data['title'],
                defaults=quest_data
            )
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                quest.tags.add(tag)
            quest.save()