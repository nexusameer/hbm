from django.contrib import admin
from . import models

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "customer_number", "invoice_date", "due_date", "total_excluding_tax", "vat", "total_including_tax")
    list_filter = ("invoice_date",)
    search_fields = ("customer_number", "invoice_number", "invoice_date", "due_date",)
    date_hierarchy = 'invoice_date'

class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ("item_id", "invoice", "description", "quantity", "unit_price", "amount",)
    list_filter = ("invoice__invoice_number", "invoice__customer_number", "unit_price", "amount",)
    search_fields = ("description", "unit_price", "quantity", "amount",)


admin.site.register(models.Invoice, InvoiceAdmin)
admin.site.register(models.InvoiceItem, InvoiceItemAdmin)