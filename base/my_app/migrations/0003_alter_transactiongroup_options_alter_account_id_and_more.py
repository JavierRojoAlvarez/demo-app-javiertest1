# Generated by Django 4.1.5 on 2023-01-18 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_cashflow_cashflowcategory_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cashflow',
        ),
        migrations.DeleteModel(
            name='CashflowCategory',
        ),
    ]
