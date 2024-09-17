from django.contrib import admin
from . import models
# Register your models here.

class FloriwayAdmin(admin.ModelAdmin):
    list_display = ("week", "date", "loading_address", "file", "number", "unit", "unloading_address", "btw", "price", "amount", "invoice_number")
    list_filter = ("week", "date", "loading_address", "unloading_address", "invoice_number")
    search_fields = ("loading_address", "file", "invoice_number", "unloading_address", "file_reference")
    date_hierarchy = 'date'



admin.site.register(models.Floriway, FloriwayAdmin)