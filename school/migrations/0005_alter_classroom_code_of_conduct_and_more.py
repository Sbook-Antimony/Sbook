# Generated by Django 5.0.6 on 2024-06-15 16:44

import mdeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sbook", "0018_alter_user_username"),
        ("school", "0004_remove_classroom_members"),
    ]

    operations = [
        migrations.AlterField(
            model_name="classroom",
            name="code_of_conduct",
            field=mdeditor.fields.MDTextField(null=True),
        ),
        migrations.AlterField(
            model_name="classroom",
            name="courses",
            field=models.ManyToManyField(
                null=True, related_name="classrooms", to="sbook.course"
            ),
        ),
        migrations.AlterField(
            model_name="classroom",
            name="description",
            field=mdeditor.fields.MDTextField(null=True),
        ),
        migrations.AlterField(
            model_name="classroom",
            name="levels",
            field=models.ManyToManyField(
                null=True, related_name="classrooms", to="sbook.level"
            ),
        ),
        migrations.AlterField(
            model_name="classroom",
            name="series",
            field=models.ManyToManyField(
                null=True, related_name="classrooms", to="sbook.serie"
            ),
        ),
    ]