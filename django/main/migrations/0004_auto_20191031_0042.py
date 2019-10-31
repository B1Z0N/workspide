# Generated by Django 2.2.6 on 2019-10-30 22:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20191030_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='not_read',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ad',
            name='pub_dtime',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='pide',
            name='pub_dtime',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]