# Generated by Django 4.2.11 on 2024-05-03 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('featurs', '0025_remove_secondarytransferstation_gpslatitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rolepermission',
            name='Permission',
        ),
        migrations.RemoveField(
            model_name='rolepermission',
            name='Role',
        ),
        migrations.DeleteModel(
            name='Permission',
        ),
        migrations.DeleteModel(
            name='RolePermission',
        ),
    ]
