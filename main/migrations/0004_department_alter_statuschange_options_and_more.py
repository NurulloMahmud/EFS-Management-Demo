# Generated by Django 4.2.5 on 2023-10-26 09:55

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_alter_statuschange_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterModelOptions(
            name='statuschange',
            options={'ordering': ('-date', 'efs')},
        ),
        migrations.AlterField(
            model_name='statuschange',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 26, 9, 55, 39, 20494, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='UserDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.department')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
