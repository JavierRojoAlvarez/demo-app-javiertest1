# Generated by Django 3.1.5 on 2021-04-13 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_auto_20210408_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receivedinvoice',
            name='pdf',
            field=models.FileField(upload_to='received-invoices/', verbose_name='PDF File'),
        ),
    ]
