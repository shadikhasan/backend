# Generated by Django 5.0.4 on 2024-05-05 09:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managers', '0002_alter_landfillmanager_landfill_alter_stsmanager_sts_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manager',
            name='id',
        ),
        migrations.AlterField(
            model_name='manager',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='manager', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
