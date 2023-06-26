from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from account.models import Invoice, Payment
from service.models import Contract


@login_required(login_url='/')
def invoice(request):
    my_contracts = Contract.objects.filter(user=request.user)

    context = {
        'my_contracts': my_contracts
    }
    return render(request, 'accounts/invoice.html', context)


@login_required(login_url='/')
def payment(request):
    invoices = Invoice.objects.filter(user=request.user)

    context = {
        'invoices': invoices
    }
    return render(request, 'accounts/payment.html', context)
