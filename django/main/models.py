from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


##################################################
# Custom user management models
##################################################


class UserManager(BaseUserManager):

    def create_user(self, email, password=None,
        first_name=None, last_name=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='email address',
        max_length=50,
        unique=True,
    )
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)  # a superuser
    # notice the absence of a "Password field", that's built in.

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True


##################################################
# Workflow models
##################################################


CURRENCY_CHOICES = [
    ('uah', 'uah'),
    ('usd', 'usd'),
    ('eur', 'eur'),
]


AD_CHOICES = [
    ('resume', 'resume'),
    ('vacancy', 'vacancy')
]


def print_ad_info(self):
    sal = ''
    if self.salary and self.currency:
        sal = ', ' + str(self.salary) + ' ' + self.currency
    exp = ', ' + str(self.experience_months) + ' months' if self.experience_months else ''
    return self.ad_type + ': ' + self.title + sal + exp


class Ad(models.Model):
    uid = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # use User specified in settings file
        on_delete=models.CASCADE
        )
    ad_type = models.CharField(max_length=7, choices=AD_CHOICES, default='resume')
    title = models.CharField(max_length=30)
    text = models.TextField(null=True, blank=True)
    salary = models.PositiveIntegerField(null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, null=True, blank=True, default='usd')
    experience_months = models.PositiveIntegerField(null=True, blank=True)

    __str__ = print_ad_info


class Skill(models.Model):
    ad_id = models.ForeignKey(Ad, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.text


class PetProject(models.Model):
    resume_id = models.ForeignKey(Ad, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)
    link = models.CharField(max_length=50)

    def __str__(self):
        return self.text


class Responsibility(models.Model):
    vacancy_id = models.ForeignKey(Ad, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.text
