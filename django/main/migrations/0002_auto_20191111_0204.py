# Generated by Django 2.2.7 on 2019-11-11 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='not_read',
            field=models.PositiveIntegerField(default=1),
        ),
    ]