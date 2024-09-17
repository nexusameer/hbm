# Generated by Django 3.2.8 on 2021-12-02 15:33

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hbm_app', '0016_alter_ahdaytransaction_sold_units'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='cell_week',
            field=models.CharField(blank=True, help_text='AH: Enter cell coordinate (e.g. A1) where the weeknumber is located, if any.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='cell_year',
            field=models.CharField(blank=True, help_text='AH: Enter cell coordinate (e.g. A1) where the year is located, if any.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='column_transaction_type',
            field=models.CharField(blank=True, help_text='AH: Describe column name for the transaction type column, if any.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='days_list',
            field=models.CharField(blank=True, default='Maandag, Dinsdag, Woensdag, Donderdag, Vrijdag, Zaterdag, Zondag', help_text='AH: Enter the names of the days, seperated by comma.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='row_days',
            field=models.PositiveIntegerField(blank=True, help_text='AH: Enter row where the days are located.', null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='customer',
            name='tab_name',
            field=models.CharField(default='Lijst', help_text='Note: Fill in name of the Excel sheet', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='column_article',
            field=models.CharField(blank=True, help_text='Describe column name for the article column, if any.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='column_date',
            field=models.CharField(blank=True, help_text='VOMAR: Describe column name for the date column, if any.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='column_loss_units',
            field=models.CharField(blank=True, help_text='VOMAR: Describe column name for the lost units column, if any.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='column_margin',
            field=models.CharField(blank=True, help_text='VOMAR: Describe column name for the margin column, if any.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='column_sold_units',
            field=models.CharField(blank=True, help_text='Describe column name for the units sold column, if any.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='column_store',
            field=models.CharField(blank=True, help_text='VOMAR: Describe column name for the store column, if any.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.CharField(help_text='Note: Enter from what email address the emails are sent. ', max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='interval',
            field=models.PositiveIntegerField(default=1, help_text='Note: Enter number of days that represent the frequency of the schedule.', validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='row_headers',
            field=models.IntegerField(help_text='Enter row where the header is located.'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='start_date',
            field=models.DateField(default=datetime.date.today, help_text='Note: Enter start date from when the schedule should be created. Value is only taken into account during creation of the record. ', verbose_name='Date'),
        ),
    ]
