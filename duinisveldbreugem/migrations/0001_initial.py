# Generated by Django 3.2.8 on 2024-02-28 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_type', models.CharField(max_length=56)),
                ('customer_number', models.CharField(max_length=56)),
                ('invoice_number', models.CharField(max_length=56)),
                ('invoice_date', models.DateField()),
                ('supplier_name', models.CharField(blank=True, max_length=256, null=True)),
                ('supplier_city', models.CharField(blank=True, max_length=256, null=True)),
                ('supplier_country', models.CharField(blank=True, max_length=256, null=True)),
                ('vat', models.FloatField()),
                ('total_excluding_tax', models.FloatField()),
                ('total_including_tax', models.FloatField()),
                ('due_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.CharField(max_length=56)),
                ('description', models.CharField(max_length=512)),
                ('quantity', models.FloatField()),
                ('unit_price', models.FloatField()),
                ('amount', models.FloatField()),
            ],
        ),
    ]
