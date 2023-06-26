import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from appointment.models import GoogleCredSettings


@login_required(login_url='/')
def my_appointment(request):
    credential = GoogleCredSettings.objects.filter().first()
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credential.cred_file.path,
        ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    )
    client = gspread.authorize(credentials)
    sheet = client.open('JK Associates Appointments (Responses)').sheet1
    data = sheet.get_all_values()

    modified_data = []
    for row in data:
        print(row[2], '---------Email---------')
        if row[2] == request.user.email:
            modified_data.append(row)

    print(modified_data, '------------------')

    return render(request, 'appointment/my_appointment.html', {'data': modified_data})


@login_required(login_url='/')
def book_a_appointment(request):
    return render(request, 'appointment/booked_appointment.html')
