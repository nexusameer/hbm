# Generated by Django 3.2.8 on 2023-10-26 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hbm_app', '0046_alter_ahperiodtransaction_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ahperiodtransaction',
            name='week',
            field=models.CharField(help_text='Week', max_length=20),
        ),
    ]
