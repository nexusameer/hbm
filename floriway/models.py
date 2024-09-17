from django.db import models

# Create your models here.
class Floriway(models.Model):
    week = models.FloatField()
    date = models.DateField()
    loading_address = models.CharField(max_length=512)
    file = models.FloatField()
    number = models.IntegerField(null=True, blank=True)
    unit = models.CharField(max_length=256, null=True, blank=True)
    unloading_address = models.CharField(max_length=512)
    btw = models.CharField(max_length=128)
    price = models.FloatField()
    amount = models.FloatField()
    file_reference = models.CharField(max_length=256, null=True, blank=True)
    invoice_number = models.FloatField()
    
    def __str__(self):
        return str(f'{self.invoice_number} - {self.loading_address}')
 