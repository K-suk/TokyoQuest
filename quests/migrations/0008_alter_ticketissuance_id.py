# Generated by Django 4.2.13 on 2024-06-21 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quests", "0007_ticket_level"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticketissuance",
            name="id",
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]