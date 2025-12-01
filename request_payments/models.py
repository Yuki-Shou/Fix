from django.db import models


class RequestPayment(models.Model):
    no = models.CharField(max_length=64)
    date = models.DateField()
    payee = models.CharField(max_length=256, blank=True)
    tin = models.CharField(max_length=64, blank=True)
    action_required = models.CharField(max_length=64, blank=True, null=True)
    mode_of_payment = models.CharField(max_length=256, blank=True, null=True)
    payment_for = models.CharField(max_length=256, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remarks = models.TextField(blank=True)
    invoice = models.FileField(upload_to='invoices/', blank=True, null=True)
    requested_by = models.CharField(max_length=128, blank=True)
    checked_by = models.CharField(max_length=128, blank=True)
    recommend_approval = models.CharField(max_length=128, blank=True)
    approved_by = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RP {self.no}"
