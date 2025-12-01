from django.contrib import admin
from .models import RequestPayment


@admin.register(RequestPayment)
class RequestPaymentAdmin(admin.ModelAdmin):
    list_display = ('no', 'date', 'payee', 'amount', 'created_at')
