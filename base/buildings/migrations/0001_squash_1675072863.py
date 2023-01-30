# Generated by Django 4.1.5 on 2023-01-30 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('epims_id', models.CharField(max_length=50, verbose_name='ePIMS ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('nia', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='NIA')),
                ('ftes_capacity', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='FTEs Capacity')),
                ('image', models.ImageField(default='images/default.png', upload_to='images')),
                ('cost_centre', models.CharField(default='', max_length=50, verbose_name='Cost Centre')),
                ('region', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='buildings.region')),
            ],
        ),
    ]
