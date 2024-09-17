from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from .models import Customer, Schedule, CustomerReceiverEmail
import logging
import datetime
from django.utils import timezone

log = logging.getLogger(__name__)

# Create schedule when customer gets created. 
@receiver(post_save, sender=Customer)
def create_schedules_for_customer(sender, instance, created, *args, **kwargs):
    if created:
        start_date = instance.start_date
        while True:
            if start_date <= datetime.date.today():
                Schedule.objects.create(customer=instance, date=start_date, completed=False)
                start_date += datetime.timedelta(days=instance.interval)
            else:
                break

@receiver(post_save, sender=CustomerReceiverEmail)
def set_last_email_sent_time_for_customer_specific_emails(sender, instance, created, *args, **kwargs):
    if created:
        days = 7 if instance.interval == 'Weekly' else 30 if instance.interval == 'Monthly' else 1
        instance.last_sent_email_time = timezone.now() - timezone.timedelta(days=days)
        instance.save()