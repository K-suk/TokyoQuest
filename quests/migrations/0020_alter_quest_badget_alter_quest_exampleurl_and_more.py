# Generated by Django 4.2.13 on 2024-07-16 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quests", "0019_alter_quest_badget_alter_quest_exampleurl_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quest",
            name="badget",
            field=models.CharField(blank=True, max_length=1500, null=True),
        ),
        migrations.AlterField(
            model_name="quest",
            name="exampleUrl",
            field=models.URLField(blank=True, max_length=1500, null=True),
        ),
        migrations.AlterField(
            model_name="quest",
            name="imgUrl",
            field=models.URLField(blank=True, max_length=1500, null=True),
        ),
        migrations.AlterField(
            model_name="quest",
            name="location",
            field=models.CharField(max_length=1500),
        ),
    ]
