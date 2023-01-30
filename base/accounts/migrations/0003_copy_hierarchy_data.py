# Generated by Django 4.1.5 on 2023-01-23 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_copy_account_type_data'),
    ]

    operations = [
        migrations.RunSQL(
            '''
            INSERT INTO accounts_hierarchy1
            SELECT * FROM my_app_hierarchy1;
            ''',
            reverse_sql=(
                '''
                INSERT INTO my_app_hierarchy1
                SELECT * FROM accounts_hierarchy1;
                '''
            ),
            elidable=True
        ),
        migrations.RunSQL(
            '''
            INSERT INTO accounts_hierarchy2
            SELECT * FROM my_app_hierarchy2;
            ''',
            reverse_sql=(
                '''
                INSERT INTO my_app_hierarchy2
                SELECT * FROM accounts_hierarchy2;
                '''
            ),
            elidable=True
        ),
        migrations.RunSQL(
            '''
            INSERT INTO accounts_hierarchy3
            SELECT * FROM my_app_hierarchy3;
            ''',
            reverse_sql=(
                '''
                INSERT INTO my_app_hierarchy3
                SELECT * FROM accounts_hierarchy3;
                '''
            ),
            elidable=True
        ),
        migrations.RunSQL(
            '''
            INSERT INTO accounts_hierarchy4
            SELECT * FROM my_app_hierarchy4;
            ''',
            reverse_sql=(
                '''
                INSERT INTO my_app_hierarchy4
                SELECT * FROM accounts_hierarchy4;
                '''
            ),
            elidable=True
        ),
    ]
