# Generated by Django 3.2.8 on 2022-01-18 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hbm_app', '0028_customcommands'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomCommands',
            new_name='CustomCommand',
        ),
    ]
