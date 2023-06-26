import random

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django_countries.fields import CountryField


def generate_cid():
    number = random.randint(10000, 99999)
    return "JKC-{}{}".format(timezone.now().strftime("%y%m"), number)


def profile_image_upload(instance, filename):
    return "profile/%s/%s" % (instance.client_id, filename)


class Profile(models.Model):
    GENDER_CHOICE = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Username')
    client_id = models.CharField(default=generate_cid, unique=True, max_length=20, verbose_name='Client ID')
    company_name = models.CharField(max_length=200, verbose_name='Company Name', null=True, blank=True)
    image = models.FileField(upload_to=profile_image_upload, default='avatar.png', verbose_name='Image')
    date_of_birth = models.DateField(auto_now=False, verbose_name="Date of birth", null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, blank=True)
    phone = models.CharField(max_length=15, null=True, verbose_name="Phone", blank=True)
    address = models.TextField(null=True, verbose_name="Address", blank=True)
    district = models.CharField(max_length=200, null=True, verbose_name="District", blank=True)
    country = CountryField(blank_label='(Select Country)', null=True, verbose_name="Country")
    otp = models.CharField(max_length=6, blank=True, verbose_name='One Time Password')
    is_verify = models.BooleanField(verbose_name="Verified", default=False)
    is_company = models.BooleanField(verbose_name="Company", default=False)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    create_date = models.DateTimeField(auto_now=True, verbose_name='Create date')

    def __str__(self):
        return self.client_id + "_" + self.user.username

    def user_photo(self):
        return mark_safe('<img src="{}" width="50" height ="50" />'.format(self.image.url))

    user_photo.short_description = 'Image'
    user_photo.allow_tags = True


class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Client")
    name = models.CharField(max_length=200, verbose_name='Name', null=True)
    job_title = models.CharField(max_length=200, verbose_name='Job Title', null=True, blank=True)
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=15, verbose_name="Phone")
    whatsapp = models.CharField(max_length=20, verbose_name='WhatsApp', blank=True)
    create_date = models.DateTimeField(auto_now=True, verbose_name='Create Date')

    def __str__(self):
        return self.user.profile.client_id + "_" + self.name
