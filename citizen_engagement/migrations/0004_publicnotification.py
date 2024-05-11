# Generated by Django 5.0.6 on 2024-05-11 02:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citizen_engagement', '0003_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_read', models.BooleanField(default=False)),
            ],
        ),
    ]