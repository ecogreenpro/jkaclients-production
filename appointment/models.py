import random

from django.contrib.auth.models import User
from django.db import models

from service.models import Service


# Create your models here.
def generate_ref_no():
    number = random.randint(1000000, 9999999)
    return "Ref-{}".format(number)


class Appointments(models.Model):
    APPOINTMENTS_CHOICE = [
        ('Queue', 'Queue'),
        ('Completes', 'Completes'),
        ('Denied', 'Denied'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Username')
    reference_no = models.CharField(default=generate_ref_no, max_length=10, verbose_name='Reference No')
    appointments = models.CharField(max_length=20, choices=APPOINTMENTS_CHOICE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Service")
    note = models.TextField(verbose_name="Note")
    appointment_date = models.DateTimeField(verbose_name='Appointment Date')

    def __str__(self):
        return self.reference_no


def generate_c_no():
    number = random.randint(10000, 99999)
    return "C-{}".format(number)


class OurClients(models.Model):
    APPOINTMENTS_CHOICE = [
        ('Queue', 'Queue'),
        ('Completes', 'Completes'),
        ('Denied', 'Denied'),
    ]
    name = models.CharField(max_length=200, verbose_name='Name')
    email = models.EmailField(verbose_name='Email')
    clients_no = models.CharField(default=generate_c_no, max_length=10, verbose_name='Reference No')
    service = models.ManyToManyField(Service, verbose_name="Service")
    appointments_status = models.CharField(max_length=10, choices=APPOINTMENTS_CHOICE)
    schedule_call = models.DateTimeField(verbose_name='Schedule Call', blank=True, null=True)
    note = models.TextField(verbose_name="Note")
    visit_date = models.DateTimeField(verbose_name='Office Visit Date', blank=True, null=True)

    def __str__(self):
        return self.clients_no


class GoogleCredSettings(models.Model):
    cred_file = models.FileField(blank=True, upload_to="googleauth", verbose_name="Cred File")
    drive_cred_file = models.FileField(blank=True, upload_to="googleauth", verbose_name="Drive Cred File")
