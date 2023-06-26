from django.contrib import admin

from service.models import Service, Contract, MyDocuments, MyService


class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'service_code',
        'service_name',
        'create_date',
        'is_active',
    ]
    search_fields = ['service_code']


admin.site.register(Service, ServiceAdmin)


class MyServiceAdmin(admin.ModelAdmin):
    list_display = [
        'my_service_id',
        'service',
        'my_service_fees',
        'my_service_start',
        'my_service_deadlines',
    ]
    search_fields = ['my_service_id']


admin.site.register(MyService, MyServiceAdmin)


class ContractAdmin(admin.ModelAdmin):
    list_display = [
        'contract_id',
        'user',
        'contract_title',
        'validates_date',
        'total_amount_of_contract'
    ]
    search_fields = ['contract_id']


admin.site.register(Contract, ContractAdmin)


class MyDocumentsAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'file_name',
        'description',
    ]


admin.site.register(MyDocuments, MyDocumentsAdmin)
