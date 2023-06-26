from django.contrib import admin

from account.models import Invoice, Payment


# Register your models here.
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'invoice_id',
        'contract',
        'due_date',
        'due_amount',
    ]
    search_fields = ['invoice_id']


admin.site.register(Invoice, InvoiceAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'invoice',
        'payment_reference',
        'amount',
        'payment_status'
    ]
    search_fields = ['payment_id']


admin.site.register(Payment, PaymentAdmin)
