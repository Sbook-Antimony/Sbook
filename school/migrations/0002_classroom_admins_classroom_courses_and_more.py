# Generated by Django 5.0.6 on 2024-06-12 17:52

import django.db.models.deletion
import mdeditor.fields
import profile_images
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sbook", "0016_alter_course_profile_alter_level_profile_and_more"),
        ("school", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="classroom",
            name="admins",
            field=models.ManyToManyField(
                related_name="admins_classrooms", to="sbook.user"
            ),
        ),
        migrations.AddField(
            model_name="classroom",
            name="courses",
            field=models.ManyToManyField(related_name="classrooms", to="sbook.course"),
        ),
        migrations.AddField(
            model_name="classroom",
            name="description",
            field=mdeditor.fields.MDTextField(default="nothing here..."),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="classroom",
            name="levels",
            field=models.ManyToManyField(related_name="classrooms", to="sbook.level"),
        ),
        migrations.AddField(
            model_name="classroom",
            name="members",
            field=models.ManyToManyField(related_name="classrooms", to="sbook.user"),
        ),
        migrations.AddField(
            model_name="classroom",
            name="profile",
            field=models.ImageField(
                default=profile_images.get_random_file, upload_to="profiles/classroom"
            ),
        ),
        migrations.AddField(
            model_name="classroom",
            name="school",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="classrooms",
                to="school.school",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="classroom",
            name="series",
            field=models.ManyToManyField(related_name="classrooms", to="sbook.serie"),
        ),
        migrations.AddField(
            model_name="classroom",
            name="students",
            field=models.ManyToManyField(
                related_name="teached_classrooms", to="sbook.user"
            ),
        ),
        migrations.AddField(
            model_name="classroom",
            name="teachers",
            field=models.ManyToManyField(
                related_name="teaches_classrooms", to="sbook.user"
            ),
        ),
    ]
