# Generated by Django 4.1.5 on 2023-01-18 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cashflows', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            '''
            INSERT INTO cashflows_cashflowcategory
            SELECT * FROM my_app_cashflowcategory;
            ''',
            reverse_sql=(
                '''
                INSERT INTO my_app_cashflowcategory
                SELECT * FROM cashflows_cashflowcategory;
                '''
            )
        ),
        migrations.RunSQL(
            '''
            INSERT INTO cashflows_cashflow
            SELECT * FROM my_app_cashflow;
            ''',
            reverse_sql=(
                '''
                INSERT INTO my_app_cashflow
                SELECT * FROM cashflows_cashflow;
                '''
            )
        )
    ]