from django.contrib import admin

from appointment.models import Appointments, GoogleCredSettings, OurClients


# Register your models here.
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'appointments',
        'service',
        'note',
        'appointment_date'
    ]


admin.site.register(Appointments, AppointmentsAdmin)
admin.site.register(GoogleCredSettings)


class OurClientsAdmin(admin.ModelAdmin):
    list_display = [
        'clients_no',
        'name',
        'email',
        'schedule_call',
        'visit_date',
        'note'
    ]
    search_fields = ['clients_no', 'name', 'email']


admin.site.register(OurClients, OurClientsAdmin)
