from django.db import models


# Placeholder GRN models — implement fields as needed later
class GoodsReceivedNote(models.Model):
    no = models.CharField(max_length=64)
    date = models.DateField()
    linked_po = models.CharField(max_length=64, blank=True, null=True)
    received_by = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"GRN {self.no}"
