# Generated by Django 4.2.13 on 2024-07-10 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quests", "0014_quest_exampleurl_quest_imgurl"),
    ]

    operations = [
        migrations.AddField(
            model_name="questcompletion",
            name="media",
            field=models.FileField(blank=True, null=True, upload_to="media/"),
        ),
    ]
