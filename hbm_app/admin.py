from django.contrib import admin
from . import models


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("customer", "store", "article", "date", "sold_units", "sold_amount", "loss_units", "loss_amount")
    list_filter = ("date", "customer__name")
    search_fields = ("customer__name", "store", "article", "date",)
    date_hierarchy = 'date'

class AhDayTransactionAdmin(admin.ModelAdmin):
    list_display = ("article", "date", "type_transaction", "estimation_units", "sold_units",)
    list_filter = ("article", )
    date_hierarchy = 'date'

class AhWeekTransactionAdmin(admin.ModelAdmin):
    list_display = ("article", "year", "week", "type_transaction", "actual_number_of_units", "actual_revenue", "actual_gross_profit", "actual_loss", "store_count", "rotation")
    list_filter = ("article", "year", "week")

class AhPeriodTransactionAdmin(admin.ModelAdmin):
    list_display = ("year", "week", "day", "date", "nasa_number", "type_transaction", "value",)
    list_filter = ("year", "week", "day", "type_transaction")
    date_hierarchy = 'date'

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("customer", "date", "completed")
    list_filter = ("completed", "customer__name")
    date_hierarchy = 'date'

class ArticleAdmin(admin.ModelAdmin):
    list_display = ("customer", "article_number", "article_name", "article_type", "event")
    search_fields = ("article_number", "article_name",)
    list_filter = ("customer", "article_type", "event")

class ReceiverEmailAdmin(admin.ModelAdmin):
    list_display = ("email", "receive_sync_successull_email", "receive_sync_unsuccessull_email", "receive_missing_schedule_email")
    list_filter = ("email", "receive_sync_successull_email", "receive_sync_unsuccessull_email", "receive_missing_schedule_email")
    search_fields = ("email",)

class AgreflorAdmin(admin.ModelAdmin):
    list_display = ("store_number", "store_name", "product_category", "gtin_number", "units", "turnover", "start_date", "end_date")
    list_filter = ("store_name", "product_category",)
    search_fields = ("gtin_number", "store_name", "store_number",)
    date_hierarchy = 'start_date'

class AntennaAdmin(admin.ModelAdmin):
    list_display = ("resource_name",  "date_worked", "year", "week", "invoice_number", "invoice_date", "invoice_quantity", "invoice_type", "rate", "allowace_rate", "invoice_amount", "vat", "resource_number")
    list_filter = ("invoice_type",)
    search_fields = ("invoice_number", "resource_name")
    date_hierarchy = 'date_worked'

class WematransAdmin(admin.ModelAdmin):
    list_display = ("week",  "date", "loading_address", "file", "quantity", "unloading_address", "vat_code", "unit_price", "amount", "invoice_number")
    list_filter = ("loading_address","unloading_address")
    search_fields = ("loading_address", "vat_code", "invoice_number", "unloading_address", "file")
    date_hierarchy = 'date'

class CustomerReceiverEmailAdmin(admin.ModelAdmin):
    list_display = ("customer",  "name", "email_address", "interval", "active",)
    list_filter = ("customer", "active", "interval")
    search_fields = ("customer__name", "name", "email_address")

class DatedEventAdmin(admin.ModelAdmin):
    list_display = ("event",  "date",)
    search_fields = ("event__name",)
    date_hierarchy = 'date'

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("name" ,"customer", "read")

admin.site.register(models.Customer)
admin.site.register(models.Transaction, TransactionAdmin)
admin.site.register(models.ErrorLog)
admin.site.register(models.ActionLog)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Schedule, ScheduleAdmin)
admin.site.register(models.AhDayTransaction, AhDayTransactionAdmin)
admin.site.register(models.AhWeekTransaction, AhWeekTransactionAdmin)
admin.site.register(models.AhPeriodTransaction, AhPeriodTransactionAdmin)
admin.site.register(models.ReceiverEmail, ReceiverEmailAdmin)
admin.site.register(models.CustomCommand)
admin.site.register(models.Agreflor, AgreflorAdmin)
admin.site.register(models.Antenna, AntennaAdmin)
admin.site.register(models.CustomerReceiverEmail, CustomerReceiverEmailAdmin)
admin.site.register(models.Wematrans, WematransAdmin)
admin.site.register(models.ArticleType)
admin.site.register(models.Event)
admin.site.register(models.DatedEvent, DatedEventAdmin)
admin.site.register(models.Attachment, AttachmentAdmin)

admin.site.site_url = '/api/custom_commands'
admin.site.site_title = 'HBM Administration'
admin.site.site_header = 'HBM Administration'

