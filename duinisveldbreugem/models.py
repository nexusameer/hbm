from django.db import models

# Create your models here.
class Invoice(models.Model):
    customer_number = models.CharField(max_length=56)
    invoice_number = models.CharField(max_length=56)
    invoice_date = models.DateField()
    supplier_name = models.CharField(max_length=256, null=True, blank=True)
    supplier_city = models.CharField(max_length=256, null=True, blank=True)
    supplier_country = models.CharField(max_length=256, null=True, blank=True)
    vat = models.FloatField()
    total_excluding_tax = models.FloatField()
    total_including_tax = models.FloatField()
    due_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return str(f'{self.invoice_number} - {self.customer_number}')
    

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    item_id = models.CharField(max_length=56)
    description = models.CharField(max_length=512)
    quantity = models.FloatField()
    unit_price = models.FloatField()
    amount = models.FloatField()