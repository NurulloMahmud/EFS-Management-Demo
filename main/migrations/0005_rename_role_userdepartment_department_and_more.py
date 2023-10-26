# Generated by Django 4.2.5 on 2023-10-26 10:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_department_alter_statuschange_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdepartment',
            old_name='role',
            new_name='department',
        ),
        migrations.AlterField(
            model_name='statuschange',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 26, 10, 1, 30, 917513, tzinfo=datetime.timezone.utc)),
        ),
    ]