# Generated by Django 5.0.6 on 2024-05-24 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("note", "0005_note_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="note",
            name="description",
            field=models.TextField(),
        ),
    ]
