# Generated by Django 5.0.6 on 2024-06-12 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("quizz", "0017_rename_data_quizz_questions_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quizz",
            name="classrooms",
        ),
    ]
