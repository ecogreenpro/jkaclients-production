import tempfile
from itertools import count

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template

from jkaclients import settings
from service.forms import FileUploadForm, ServiceUpdateForm
from service.google_drive import upload_to_google_drive
from service.models import Service, MyService, Contract, MyDocuments


@login_required(login_url='/')
def my_service(request):
    if request.method == 'POST':
        service_form = ServiceUpdateForm(request.POST, request=request)
        if service_form.is_valid():
            service_form.save()
            service = service_form.cleaned_data['service']
            my_service_description = service_form.cleaned_data['my_service_description']
            messages.info(request, 'Service added Successfully')
            current_site = get_current_site(request)
            mail_context = {
                'user': request.user,
                'domain': current_site.domain,
                'service': service,
                'notes': my_service_description,
            }
            # Mail to Admin
            admin_subject = f'There has a new service request from {request.user.profile.client_id} - {request.user.get_full_name()}'
            admin_content = f'There has a new service request from {request.user.profile.client_id}'
            from_email = 'JK Associates <noreply@jkassociates.com.bd>'
            admin_to_email = [settings.EMAIL_ADMIN_USER]
            admin_templates = get_template('emails/service_consultant.html').render(mail_context)
            admin_mail = EmailMultiAlternatives(admin_subject, admin_content, from_email, admin_to_email)
            admin_mail.attach_alternative(admin_templates, 'text/html')
            admin_mail.send()

            # Mail to Clients

            subject = f'{request.user.get_full_name()}, you request for a service'
            content = f'{request.user.get_full_name()}, you request for a service'
            from_email = 'JK Associates <noreply@jkassociates.com.bd>'
            to_email = [request.user.email]
            templates = get_template('emails/service_clients.html').render(mail_context)
            mail = EmailMultiAlternatives(subject, content, from_email, to_email)
            mail.attach_alternative(templates, 'text/html')
            mail.send()
        return redirect('service:my-service')
    else:
        my_services = MyService.objects.filter(user=request.user)
        service_form = ServiceUpdateForm(request=request)
        context = {
            'my_services': my_services,
            'service_form': service_form,
        }
        return render(request, 'service/my_services.html', context)


@login_required(login_url='/')
def contract(request):
    my_contracts = Contract.objects.filter(user=request.user)

    context = {
        'my_contracts': my_contracts
    }
    return render(request, 'service/contracts.html', context)


@login_required(login_url='/')
def my_documents(request):
    form = FileUploadForm()
    my_contracts = Contract.objects.filter(user=request.user)

    context = {
        'my_contracts': my_contracts,
        'form': form,
    }
    return render(request, 'service/my_documents.html', context)


def upload_file(request, contract_id):
    if request.method == 'POST':
        this_contract = Contract.objects.get(contract_id=contract_id)
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file_name = request.POST.get('file_name')
            file_note = request.POST.get('note')
            uploaded_file = request.FILES['file']
            file_path = tempfile.mkstemp()[1]
            print(file_path, '---------------file--------------')
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            file_name = uploaded_file.name
            google_drive_link = upload_to_google_drive(file_path, file_name)
            my_documents = MyDocuments()
            my_documents.user = request.user
            my_documents.contract = this_contract
            my_documents.file_name = upload_file_name
            my_documents.file_url = google_drive_link
            my_documents.description = file_note
            my_documents.save()
            messages.success(request, 'File Upload successfully')
            return redirect('service:my_document')
