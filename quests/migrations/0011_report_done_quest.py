# Generated by Django 4.2.13 on 2024-06-21 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quests", "0010_report"),
    ]

    operations = [
        migrations.AddField(
            model_name="report",
            name="done_quest",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]