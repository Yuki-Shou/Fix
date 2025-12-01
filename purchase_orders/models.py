from django.db import models


class PurchaseOrder(models.Model):
    no = models.CharField(max_length=64)
    date = models.DateField()
    # Optional link to a Purchase Requisition (PR)
    linked_pr = models.ForeignKey(
        'purchase_requisitions.PurchaseRequisition',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='linked_pos'
    )
    dept = models.CharField(max_length=128, blank=True)
    supplier = models.CharField(max_length=256, blank=True)
    tin = models.CharField(max_length=64, blank=True)
    address = models.TextField(blank=True)
    contact_person = models.CharField(max_length=128, blank=True)
    contact_number = models.CharField(max_length=64, blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    prepared_by = models.CharField(max_length=128, blank=True)
    checked_by = models.CharField(max_length=128, blank=True)
    approved_by = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PO {self.no}"


class POItem(models.Model):
    po = models.ForeignKey(PurchaseOrder, related_name='items', on_delete=models.CASCADE)
    qty = models.FloatField(default=0)
    unit = models.CharField(max_length=64, blank=True)
    description = models.TextField(blank=True)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # Optional delivery / date expected for this item
    del_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.description} ({self.qty})"
