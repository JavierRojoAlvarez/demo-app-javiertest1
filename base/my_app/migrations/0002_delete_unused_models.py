# Generated by Django 4.1.5 on 2023-01-18 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_squash'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AssetType',
        ),
        migrations.DeleteModel(
            name='ProfitCentre',
        ),
    ]