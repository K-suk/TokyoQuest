# Generated by Django 4.2.19 on 2025-03-10 23:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_remove_user_id_user_user_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_id",
            field=models.CharField(
                default=uuid.uuid4,
                editable=False,
                max_length=255,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
