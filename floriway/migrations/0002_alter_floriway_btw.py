# Generated by Django 3.2.8 on 2024-03-15 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('floriway', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floriway',
            name='btw',
            field=models.CharField(max_length=128),
        ),
    ]
