# Generated by Django 5.0.6 on 2024-05-10 07:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secondarytransferstation',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waste_management.area'),
        ),
    ]
