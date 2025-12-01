"""Add linked_pr (FK to PR) to PurchaseOrder and del_date to POItem

Generated manually to persist the front-end fields used by PO form.
"""
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_orders', '0001_initial'),
        ('purchase_requisitions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='linked_pr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='linked_pos', to='purchase_requisitions.purchaserequisition'),
        ),
        migrations.AddField(
            model_name='poitem',
            name='del_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
