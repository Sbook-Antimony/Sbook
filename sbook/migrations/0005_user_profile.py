# Generated by Django 5.0.6 on 2024-05-22 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sbook", "0004_remove_user_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="profile",
            field=models.ImageField(null=True, upload_to=""),
        ),
    ]
