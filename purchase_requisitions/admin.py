from django.contrib import admin
from .models import PurchaseRequisition, PRItem


class PRItemInline(admin.TabularInline):
    model = PRItem
    extra = 0


@admin.register(PurchaseRequisition)
class PurchaseRequisitionAdmin(admin.ModelAdmin):
    list_display = ('no', 'date', 'requester')
    inlines = [PRItemInline]
