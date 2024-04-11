# Generated by Django 4.2.3 on 2024-04-11 10:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LiveStreamLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default='qwerty', max_length=200)),
                ('data', models.JSONField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2024, 4, 11, 10, 57, 30, 836067, tzinfo=datetime.timezone.utc))),
            ],
        )
    ]
