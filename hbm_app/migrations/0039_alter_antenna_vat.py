# Generated by Django 3.2.8 on 2022-12-12 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hbm_app', '0038_antenna'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antenna',
            name='vat',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
