# Generated by Django 5.0.6 on 2024-05-26 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("quizz", "0008_rename_quizzanswerettempt_quizzanswerattempt"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="QuizzAnswerAttempt",
            new_name="QuizzAttempt",
        ),
    ]
