from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class User(models.Model):
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    email = models.CharField(max_length=30)
    pass_hash = models.CharField(max_length=50)


class Vacancy(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=10000)
    salary = models.IntegerField(null=True)
    currency = models.CharField(max_length=3, null=True)
    experience_months = models.IntegerField(null=True)


class Resume(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=10000)
    salary = models.IntegerField()
    currency = models.CharField(max_length=3, null=True)
    

class SkillsForVacancy(models.Model):
    vacancy_id = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)


class SkillsForResume(models.Model):
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)


class PetProject(models.Model):
    resume_id = models.OneToOneField(
        Resume,
        on_delete=models.CASCADE,
        primary_key=True
    )
    title = models.CharField(max_length=30)
    link = models.CharField(max_length=30)


class Responsibilities(models.Model):
    vacancy_id = models.OneToOneField(
        Vacancy,
        on_delete=models.CASCADE,
        primary_key=True
    )
    text = models.CharField(max_length=30)
