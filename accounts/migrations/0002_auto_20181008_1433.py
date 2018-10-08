# Generated by Django 2.1.2 on 2018-10-08 09:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=datetime.datetime(2018, 10, 8, 9, 3, 35, 13726, tzinfo=utc), max_length=25, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='admin',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='staff',
            field=models.BooleanField(default=True),
        ),
    ]