# Generated by Django 3.2.8 on 2022-02-22 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hbm_app', '0031_merge_20220222_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='article_type',
            field=models.CharField(choices=[('Boeket', 'Boeket'), ('Mono', 'Mono'), ('Planten', 'Planten'), ('Geen type', 'Geen type')], default='Geen type', max_length=20),
        ),
    ]
