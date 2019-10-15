from django.db import models


class Connector(models.Model):
    id = models.IntegerField(primary_key=True)
    uid = models.IntegerField()
    ad_t = models.CharField(max_length=7)
    ad_id = models.IntegerField()

    class Meta:
        db_table = 'Connector'


class Petproject(models.Model):
    id = models.ForeignKey('Resume', models.DO_NOTHING,
                           db_column='id', primary_key=True)
    resume_id = models.IntegerField()
    title = models.CharField(max_length=30)
    link = models.CharField(max_length=30)

    class Meta:
        db_table = 'PetProject'


class Responsibilities(models.Model):
    id = models.IntegerField(primary_key=True)
    vacancy_id = models.IntegerField()
    responsibility = models.CharField(max_length=30)

    class Meta:
        db_table = 'Responsibilities'


class Resume(models.Model):
    id = models.IntegerField(primary_key=True)
    uid = models.IntegerField()
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=10000)
    salary = models.IntegerField(blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        db_table = 'Resume'


class Skills(models.Model):
    id = models.IntegerField(primary_key=True)
    ad_t = models.CharField(max_length=7)
    ad_id = models.IntegerField()
    skill = models.CharField(max_length=30)

    class Meta:
        db_table = 'Skills'


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=30)
    pass_hash = models.CharField(max_length=50)

    class Meta:
        db_table = 'User'


class Vacancy(models.Model):
    id = models.IntegerField(primary_key=True)
    uid = models.IntegerField()
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=10000)
    salary = models.IntegerField(blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Vacancy'
