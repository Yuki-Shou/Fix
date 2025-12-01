from django.db import models


class PurchaseRequisition(models.Model):
    no = models.CharField(max_length=64)
    date = models.DateField()
    requester = models.CharField(max_length=128, blank=True)
    dept = models.CharField(max_length=128, blank=True)
    date_needed = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True)
    requested_by = models.CharField(max_length=128, blank=True)
    checked_by = models.CharField(max_length=128, blank=True)
    recommend_approval = models.CharField(max_length=128, blank=True)
    approved_by = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PR {self.no}"


class PRItem(models.Model):
    pr = models.ForeignKey(PurchaseRequisition, related_name='items', on_delete=models.CASCADE)
    stk = models.CharField(max_length=64, blank=True)
    qty = models.FloatField(default=0)
    unit = models.CharField(max_length=64, blank=True)
    desc = models.TextField(blank=True)
    remark = models.TextField(blank=True)

    def __str__(self):
        return f"{self.desc} ({self.qty})"
