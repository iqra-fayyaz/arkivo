# Generated by Django 5.1.6 on 2025-05-23 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('displayApp', '0003_alter_project_grade_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
