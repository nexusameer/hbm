# Generated by Django 3.2.8 on 2021-12-07 20:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hbm_app', '0024_auto_20211207_0002'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ahweektransaction',
            old_name='article_number',
            new_name='article',
        ),
        migrations.RenameField(
            model_name='ahweektransaction',
            old_name='transaction_type',
            new_name='type_transaction',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='cell_actual_forecast_number_of_units',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='cell_actual_forecast_revenue',
        ),
        migrations.AddField(
            model_name='customer',
            name='cell_actual_number_of_units',
            field=models.CharField(blank=True, help_text='AH Week: Enter cell coordinate (e.g. A1) for number of unit column in Actual, if any', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='cell_actual_revenue',
            field=models.CharField(blank=True, help_text='AH Week: Enter cell coordinate (e.g. A1) for the revenue column in the Actual, if any', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ahweektransaction',
            name='actual_gross_profit',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Realisatie - Brutowinst', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='ahweektransaction',
            name='actual_loss',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Realisatie - Afboekingen', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='ahweektransaction',
            name='actual_revenue',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Realisatie - Omzet', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='ahweektransaction',
            name='forecast_revenue',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Prognose - Omzet', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='ahweektransaction',
            name='week',
            field=models.IntegerField(help_text='Week'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cell_forecast_number_of_units',
            field=models.CharField(blank=True, help_text='AH Week: Enter cell coordinate (e.g. A1) for number of unit column in the forcast, if any', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cell_forecast_revenue',
            field=models.CharField(blank=True, help_text='AH Week: Enter cell coordinate (e.g. A1) for the revenue column in the forcast, if any', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='column_gross_profit',
            field=models.CharField(blank=True, help_text='AH Week: Describe column name for the gross profit column, if any.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='column_loss',
            field=models.CharField(blank=True, help_text='AH Week: Describe column name for the loss column, if any.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='column_number_of_units',
            field=models.CharField(blank=True, help_text='AH Week: Describe column name for the number of units column, if any.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='column_purchase_price',
            field=models.CharField(blank=True, help_text='AH Week: Describe column name for the purchase price column, if any.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='column_revenue',
            field=models.CharField(blank=True, help_text='AH Week: Describe column name for the revenue column, if any.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='column_sale_price',
            field=models.CharField(blank=True, help_text='AH Week: Describe column name for the sale price column, if any.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='days_list',
            field=models.CharField(blank=True, default='Maandag, Dinsdag, Woensdag, Donderdag, Vrijdag, Zaterdag, Zondag', help_text='AH Day: Enter the names of the days, seperated by comma.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='row_days',
            field=models.PositiveIntegerField(blank=True, help_text='AH Day: Enter row where the days are located.', null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
