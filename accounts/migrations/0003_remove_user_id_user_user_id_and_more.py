# Generated by Django 4.2.19 on 2025-03-10 23:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_remove_user_account_id_remove_user_done_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="id",
        ),
        migrations.AddField(
            model_name="user",
            name="user_id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="contact_address",
            field=models.CharField(
                blank=True, max_length=150, null=True, verbose_name="contact_address"
            ),
        ),
    ]
