from django.contrib import admin
from .models import PurchaseOrder, POItem


class POItemInline(admin.TabularInline):
    model = POItem
    extra = 0


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('no', 'date', 'supplier', 'total')
    inlines = [POItemInline]
