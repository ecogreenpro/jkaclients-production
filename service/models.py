import random

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def generate_scode():
    number = random.randint(1000, 9999)
    return "S-{}".format(number)


class Service(models.Model):
    service_code = models.CharField(default=generate_scode, unique=True, max_length=10, verbose_name='Service Code')
    service_name = models.CharField(max_length=200, verbose_name='Name')
    description = models.TextField(verbose_name='Description')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    create_date = models.DateField(auto_now_add=True, verbose_name='Create Date')
    update_date = models.DateField(auto_now=True, verbose_name='Update Date')

    def __str__(self):
        return self.service_code + "-" + self.service_name


def generate_sid():
    number = random.randint(1000, 9999)
    return "JKS-{}".format(number)


class MyService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Client")
    my_service_id = models.CharField(default=generate_sid, unique=True, max_length=20, verbose_name='Service id')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Service")
    my_service_fees = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Service Fees', blank=True,
                                          null=True)
    my_service_start = models.DateField(verbose_name='Service Start', blank=True, null=True)
    my_service_deadlines = models.DateField(verbose_name='Service Deadlines', blank=True, null=True)
    my_service_description = models.TextField(verbose_name="Description", blank=True)
    my_service_status = models.BooleanField(default=False, verbose_name='Completed')

    def __str__(self):
        return self.user.profile.client_id + "_" + self.service.service_name


def generate_con_id():
    number = random.randint(1000000, 9999999)
    return "CON-{}".format(number)


class Contract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Client")
    contract_id = models.CharField(default=generate_con_id, unique=True, max_length=20, verbose_name='Contract id')
    contract_title = models.CharField(max_length=500, verbose_name='Contract Title')
    contract_services = models.ManyToManyField(MyService, verbose_name="Contract Service")
    contract_date = models.DateField(auto_now_add=True, verbose_name='Contract Date')
    validates_date = models.DateField(auto_now_add=True, verbose_name='Validate Date')
    total_amount_of_contract = models.DecimalField(max_digits=10, decimal_places=2,
                                                   verbose_name='Total Amount of Contract')
    contract_status = models.BooleanField(default=False, verbose_name='Completed')

    def __str__(self):
        return self.contract_id + "_" + self.contract_title


def file_upload(instance, filename):
    return "profile/%s/%s/%s" % (instance.user.profile.client_id, instance.contract.contract_id, filename)


class MyDocuments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Client")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name="Contract", related_name='my_doc')
    file_name = models.CharField(max_length=500, verbose_name='File Name')
    file_url = models.CharField(max_length=1000, verbose_name='File')
    description = models.TextField(verbose_name="Description", blank=True)
    upload_date = models.DateField(auto_now_add=True, verbose_name='Upload Date')
    update_date = models.DateField(auto_now_add=True, verbose_name='Update Date')

    def __str__(self):
        return self.contract.contract_id + "_" + self.file_name
