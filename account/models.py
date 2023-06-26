import random

from django.contrib.auth.models import User
from django.db import models

from service.models import Contract


def generate_inv():
    number = random.randint(10000, 99999)
    return "INV-{}".format(number)


class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Username')
    invoice_id = models.CharField(default=generate_inv, unique=True, max_length=10, verbose_name='Invoice ID')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name="Contract",
                                 related_name='contract_invoice')
    bill_date = models.DateTimeField(verbose_name='Bill date')
    due_date = models.DateTimeField(verbose_name='Due date')
    payment_received_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                                  verbose_name='Payment Received Amount')
    due_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                     verbose_name='Due Amount')

    def __str__(self):
        return self.invoice_id


def generate_pay_id():
    number = random.randint(10000, 99999)
    return "JKA-{}".format(number)


class Payment(models.Model):
    PAYMENT_CHOICE = [
        ('Bkash', 'Bkash'),
        ('Nagad', 'Nagad'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Check', 'Check'),
        ('Others', 'Others')
    ]
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, verbose_name='Invoice', related_name='inv_payment')
    payment_id = models.CharField(default=generate_pay_id, unique=True, max_length=20, verbose_name='Payment ID')
    payment_date = models.DateTimeField(auto_now=True, verbose_name='Payment Date')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICE, verbose_name='Payment Method')
    payment_reference = models.CharField(max_length=100, verbose_name='Payment Reference')
    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                 verbose_name='Amount')
    payment_status = models.BooleanField(default=True, verbose_name='Payment Confirm')

    def __str__(self):
        return self.invoice.invoice_id + "_" + self.payment_method
