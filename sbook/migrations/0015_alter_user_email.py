# Generated by Django 5.0.6 on 2024-06-12 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sbook", "0014_remove_serie_levels_course_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
