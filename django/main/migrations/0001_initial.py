# Generated by Django 2.2.6 on 2019-10-25 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_type', models.CharField(choices=[('res', 'resume'), ('vac', 'vacancy')], default='res', max_length=3)),
                ('title', models.CharField(max_length=30)),
                ('text', models.TextField()),
                ('salary', models.IntegerField(blank=True, null=True)),
                ('currency', models.CharField(blank=True, choices=[('uah', 'uah'), ('usd', 'usd'), ('eur', 'eur')], max_length=3, null=True)),
                ('experience_months', models.IntegerField(blank=True, null=True)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
                ('ad_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Ad')),
            ],
        ),
        migrations.CreateModel(
            name='Responsibility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
                ('vacancy_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Ad')),
            ],
        ),
        migrations.CreateModel(
            name='PetProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
                ('link', models.CharField(max_length=50)),
                ('resume_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Ad')),
            ],
        ),
    ]
