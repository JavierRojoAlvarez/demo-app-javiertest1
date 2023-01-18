# Generated by Django 4.1.5 on 2023-01-18 13:55

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('my_app', '0001_squash'), ('my_app', '0002_delete_unused_models')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('description', models.CharField(default='', max_length=50)),
                ('is_live', models.BooleanField(default=True, verbose_name='Live')),
            ],
            options={
                'ordering': ('description',),
            },
        ),
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Account Types',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
                ('revenue_expenditure', models.CharField(choices=[('R', 'Revenue'), ('E', 'Expenditure')], max_length=50, verbose_name='Revenue/Expenditure')),
                ('treatment', models.CharField(choices=[('Lessee', 'Lessee'), ('Lessor', 'Lessor')], max_length=50, null=True, verbose_name='Treatment')),
                ('start', models.DateField(blank=True, null=True)),
                ('end', models.DateField(blank=True, null=True)),
                ('signed', models.BooleanField(default=False)),
                ('building', models.ManyToManyField(blank=True, to='buildings.building')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='ContractType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Contract Types',
            },
        ),
        migrations.CreateModel(
            name='CostType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Cost Types',
            },
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Hierarchy1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Hierarchy2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('hierarchy1', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='my_app.hierarchy1')),
            ],
        ),
        migrations.CreateModel(
            name='Hierarchy3',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('hierarchy2', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='my_app.hierarchy2')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('group', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='my_app.transactiongroup', verbose_name='Transaction Group')),
            ],
            options={
                'verbose_name_plural': 'Transaction Types',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('comment', models.TextField(blank=True, default='', max_length=200, null=True)),
                ('actual_expected', models.CharField(choices=[('E', 'Expected'), ('A', 'Actual')], default='E', max_length=50, verbose_name='Actual/Expected')),
                ('period', models.CharField(blank=True, max_length=50, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('treatment', models.CharField(blank=True, choices=[('Accounting', 'Accounting'), ('Budgeting', 'Budgeting')], default='', max_length=50, null=True, verbose_name='Treatment')),
                ('time_index', models.IntegerField(blank=True, default=0, null=True)),
                ('contract', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_app.contract')),
                ('transaction_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_app.transactiontype', verbose_name='Transaction Type')),
            ],
        ),
        migrations.CreateModel(
            name='PseudoEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('account', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='my_app.account')),
                ('direction', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='my_app.direction')),
                ('transaction_type', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='my_app.transactiontype', verbose_name='Transaction Type')),
            ],
            options={
                'verbose_name_plural': 'Pseudo Entries',
            },
        ),
        migrations.CreateModel(
            name='Hierarchy4',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('hierarchy3', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='my_app.hierarchy3')),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('liability', models.DecimalField(decimal_places=2, default=0, max_digits=20, null=True)),
                ('account', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='my_app.account')),
                ('contract', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='my_app.contract')),
                ('direction', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='my_app.direction')),
                ('transaction', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='my_app.transaction')),
            ],
            options={
                'verbose_name_plural': 'entries',
            },
        ),
        migrations.AddField(
            model_name='contract',
            name='contract_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_app.contracttype', verbose_name='Contract Type'),
        ),
        migrations.AddField(
            model_name='contract',
            name='organisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organisations.organisation', verbose_name='Counterparty'),
        ),
        migrations.AddField(
            model_name='account',
            name='account_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.accounttype'),
        ),
        migrations.AddField(
            model_name='account',
            name='hierarchy4',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.hierarchy4'),
        ),
        migrations.CreateModel(
            name='ContractPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, default='', max_length=200, null=True)),
                ('actual_expected', models.CharField(choices=[('E', 'Expected'), ('A', 'Actual')], default='E', max_length=50, verbose_name='Actual/Expected')),
                ('period', models.CharField(blank=True, max_length=50, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('treatment', models.CharField(blank=True, choices=[('Accounting', 'Accounting'), ('Budgeting', 'Budgeting')], default='', max_length=50, null=True, verbose_name='Treatment')),
                ('time_index', models.IntegerField(blank=True, default=0, null=True)),
                ('contract', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_app.contract')),
                ('transaction_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_app.transactiontype', verbose_name='Transaction Type')),
                ('date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='contract',
            name='treatment',
            field=models.CharField(blank=True, choices=[('Lessee', 'Lessee'), ('Lessor', 'Lessor')], max_length=50, null=True, verbose_name='Treatment'),
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('option', models.IntegerField()),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('building', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='buildings.building')),
                ('cost_type', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='my_app.costtype')),
            ],
        ),
        migrations.AlterField(
            model_name='contract',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
