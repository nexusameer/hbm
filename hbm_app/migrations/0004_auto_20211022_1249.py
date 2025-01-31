# Generated by Django 3.2.8 on 2021-10-22 12:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hbm_app', '0003_transaction_article'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action_Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Error_Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='column_article',
            field=models.CharField(default='Artikel nummer', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='column_date',
            field=models.CharField(default='Datum', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='column_loss_units',
            field=models.CharField(default='Derving', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='column_margin',
            field=models.CharField(default='Netto Commerciële Marge', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='column_sold_units',
            field=models.CharField(default='Verkocht', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='column_store',
            field=models.CharField(default='Filiaal Nummer', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='row_headers',
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
    ]
