# Generated by Django 2.2.6 on 2019-10-15 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=10000)),
                ('salary', models.IntegerField()),
                ('currency', models.CharField(max_length=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('email', models.CharField(max_length=30)),
                ('pass_hash', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=10000)),
                ('salary', models.IntegerField(null=True)),
                ('currency', models.CharField(max_length=3, null=True)),
                ('experience_months', models.IntegerField(null=True)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.User')),
            ],
        ),
        migrations.CreateModel(
            name='Petproject',
            fields=[
                ('resume_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main.Resume')),
                ('title', models.CharField(max_length=30)),
                ('link', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Responsibilities',
            fields=[
                ('vacancy_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main.Vacancy')),
                ('text', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_id', models.IntegerField()),
                ('text', models.CharField(max_length=30)),
                ('ad_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='contenttypes.ContentType')),
            ],
        ),
        migrations.AddField(
            model_name='resume',
            name='uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.User'),
        ),
        migrations.CreateModel(
            name='Connector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_id', models.IntegerField()),
                ('ad_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='contenttypes.ContentType')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.User')),
            ],
        ),
    ]
