# Generated by Django 5.0.6 on 2024-05-23 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quizz", "0002_rename_user_quizzuser"),
    ]

    operations = [
        migrations.AddField(
            model_name="quizz",
            name="is_private",
            field=models.BooleanField(default=False),
        ),
    ]
