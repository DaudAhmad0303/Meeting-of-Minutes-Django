# Generated by Django 4.1.3 on 2022-11-27 07:03

import datetime
from django.db import migrations, models
import django.db.models.deletion
import userProjects.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userAuthentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='userProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectName', models.CharField(max_length=200)),
                ('creationDate', models.DateTimeField(default=datetime.datetime(2022, 11, 27, 12, 3, 1, 520362))),
                ('projectCreator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myProjects', to='userAuthentication.user')),
            ],
        ),
        migrations.CreateModel(
            name='userProjectRecording',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myRecording', models.FileField(upload_to=userProjects.models.getFilePath)),
                ('folderName', models.CharField(max_length=200)),
                ('fileName', models.CharField(max_length=200)),
                ('associatedProject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='associatedRecording', to='userProjects.userproject')),
            ],
        ),
    ]