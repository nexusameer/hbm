# Generated by Django 3.2.8 on 2021-10-22 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hbm_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('sold_units', models.FloatField(blank=True, null=True)),
                ('sold_amount', models.FloatField(blank=True, null=True)),
                ('loss_units', models.FloatField(blank=True, null=True)),
                ('loss_amount', models.FloatField(blank=True, null=True)),
                ('margin', models.FloatField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hbm_app.customer')),
            ],
        ),
    ]
