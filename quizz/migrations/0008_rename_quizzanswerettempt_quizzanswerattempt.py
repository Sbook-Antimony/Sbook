# Generated by Django 5.0.6 on 2024-05-25 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("quizz", "0007_rename_couses_quizz_courses_quizzanswerettempt"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="QuizzAnswerEttempt",
            new_name="QuizzAnswerAttempt",
        ),
    ]
