# Generated by Django 5.0.6 on 2024-05-31 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizz', '0012_quizzattempt_mark'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizzattempt',
            name='mark',
        ),
        migrations.AddField(
            model_name='quizzattempt',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]