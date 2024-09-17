from django.db import models
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

class ActionLog(models.Model):
    action = models.CharField(max_length=200)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    test = models.BooleanField(default=False)
    post_to_database = models.BooleanField(default=True)

    def __str__(self):
        return str(f'{self.action} {self.start_date} - Completed: {self.completed}')


class ErrorLog(models.Model):
    action = models.ForeignKey(ActionLog, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    error = models.TextField()

    def __str__(self):
        return str(self.error)


class Customer(models.Model):
    name = models.CharField(max_length=200)
    interval = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], help_text="Note: Enter number of days that represent the frequency of the schedule.")
    start_date = models.DateField(("Date"), default=datetime.date.today, help_text="Note: Enter start date from when the schedule should be created. Value is only taken into account during creation of the record. ")
    email = models.CharField(max_length=200, help_text="Note: Enter from what email address the emails are sent. ")
    tab_name = models.CharField(max_length=200, null=True, blank=True, help_text="Note: Fill in name of the Excel sheet")
    row_headers = models.IntegerField(null=True, blank=True, help_text="Enter row where the header is located.")
    column_article = models.CharField(max_length=200, null=True, blank=True, help_text="Describe column name for the article column, if any.")
    column_sold_units = models.CharField(max_length=200, null=True, blank=True, help_text="Describe column name for the units sold column, if any.")
    column_date = models.CharField(max_length=200, null=True, blank=True, help_text="VOMAR: Describe column name for the date column, if any.")
    column_store = models.CharField(max_length=200, null=True, blank=True, help_text="VOMAR: Describe column name for the store column, if any.")
    column_loss_units = models.CharField(max_length=200, null=True, blank=True, help_text="VOMAR: Describe column name for the lost units column, if any.")
    column_margin = models.CharField(max_length=200, null=True, blank=True, help_text="VOMAR: Describe column name for the margin column, if any.")
    row_days = models.PositiveIntegerField(validators=[MinValueValidator(1)], null=True, blank=True, help_text="AH Day: Enter row where the days are located.")
    days_list = models.CharField(max_length=200, default="Maandag, Dinsdag, Woensdag, Donderdag, Vrijdag, Zaterdag, Zondag", null=True, blank=True, help_text="AH Day: Enter the names of the days, seperated by comma.")
    column_transaction_type = models.CharField(max_length=200, null=True, blank=True, help_text="AH: Describe column name for the transaction type column, if any.")
    cell_year = models.CharField(max_length=200, null=True, blank=True, help_text="AH: Enter cell coordinate (e.g. A1) where the year is located, if any.")
    cell_week = models.CharField(max_length=200, null=True, blank=True, help_text="AH: Enter cell coordinate (e.g. A1) where the weeknumber is located, if any.")
    column_number_of_units = models.CharField(max_length=200, null=True, blank=True, help_text="AH Week: Describe column name for the number of units column, if any.")
    cell_forecast_number_of_units=models.CharField(max_length=200,null=True, blank=True, help_text="AH Week: Enter cell coordinate (e.g. A1) for number of unit column in the forcast, if any")
    cell_actual_number_of_units=models.CharField(max_length=200,null=True, blank=True, help_text="AH Week: Enter cell coordinate (e.g. A1) for number of unit column in Actual, if any")
    column_purchase_price = models.CharField(max_length=200, null=True, blank=True, help_text="AH Week: Describe column name for the purchase price column, if any.")
    column_sale_price = models.CharField(max_length=200, null=True, blank=True, help_text="AH Week: Describe column name for the sale price column, if any.")
    column_revenue = models.CharField(max_length=200, null=True, blank=True, help_text="AH Week: Describe column name for the revenue column, if any.")
    cell_forecast_revenue=models.CharField(max_length=200,null=True, blank=True,help_text="AH Week: Enter cell coordinate (e.g. A1) for the revenue column in the forcast, if any")
    cell_actual_revenue=models.CharField(max_length=200,null=True, blank=True,help_text="AH Week: Enter cell coordinate (e.g. A1) for the revenue column in the Actual, if any")
    column_gross_profit = models.CharField(max_length=200, null=True, blank=True, help_text="AH Week: Describe column name for the gross profit column, if any.")
    column_loss = models.CharField(max_length=200, null=True, blank=True, help_text="AH Week: Describe column name for the loss column, if any.")
    column_store_count = models.CharField(max_length=200, null=True, blank=True, help_text="AH Week: Describe column name for the store count column, if any.")
    column_rotation = models.CharField(max_length=200, null=True, blank=True, help_text="AH Week: Describe column name for the rotation column, if any.")


    def __str__(self):
        return str(f'{self.name} ({self.pk})')


class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    store = models.CharField(max_length=200)
    article = models.CharField(max_length=200)
    date = models.DateTimeField()
    sold_units = models.FloatField(null=True, blank=True)
    sold_amount = models.FloatField(null=True, blank=True)
    loss_units = models.FloatField(null=True, blank=True)
    loss_amount = models.FloatField(null=True, blank=True)
    margin = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(f'{self.customer} {self.store} {self.article} {self.date}')


class Schedule(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(f'{self.customer} {self.date} {self.completed}')


class AhDayTransaction(models.Model):
    article = models.CharField(max_length=200)
    date = models.DateTimeField()
    type_transaction = models.CharField(max_length=200, help_text="Defines whether the transaction is a regular or action.")
    estimation_units = models.IntegerField(null=True, blank=True, help_text="Prognose")
    sold_units = models.IntegerField(null=True, blank=True, help_text="Realisatie")

    def __str__(self):
        return str(f'{self.article} {self.date}')


class AhWeekTransaction(models.Model):
    week=models.IntegerField(help_text="Week")
    year=models.IntegerField(help_text="Jaar")
    article=models.IntegerField(help_text="Nasa#")
    type_transaction=models.CharField(max_length=200, help_text="Actie")
    forecast_number_of_units=models.IntegerField(null=True, blank=True, help_text="Prognose - Aantal CE")
    forecast_purchase_price=models.FloatField(null=True, blank=True, help_text="Prognose - Inkoopprijs")
    forecast_sale_price=models.FloatField(null=True, blank=True, help_text="Prognose - Verkoopprijs")
    forecast_revenue=models.DecimalField(null=True, blank=True, help_text="Prognose - Omzet", max_digits=10, decimal_places=3)
    actual_number_of_units=models.IntegerField(null=True, blank=True, help_text="Realisatie - Aantal CE")
    actual_revenue=models.DecimalField(null=True, blank=True, help_text="Realisatie - Omzet", max_digits=10, decimal_places=3)
    actual_gross_profit=models.DecimalField(null=True, blank=True, help_text="Realisatie - Brutowinst", max_digits=10, decimal_places=3)
    actual_loss=models.DecimalField(null=True, blank=True, help_text="Realisatie - Afboekingen", max_digits=10, decimal_places=3)
    store_count=models.DecimalField(null=True, blank=True, help_text="Aantal Filialen", max_digits=10, decimal_places=3)
    rotation=models.DecimalField(null=True, blank=True, help_text="Rotatie", max_digits=10, decimal_places=3)

    def __str__(self):
        return str(f'{self.article}')

class AhPeriodTransaction(models.Model):
    date = models.DateTimeField(help_text="Datum")
    week=models.CharField(max_length=20, help_text="Week")
    year=models.IntegerField(help_text="Jaar")
    day=models.CharField(max_length=20, help_text="Dag")
    nasa_number = models.IntegerField(help_text="NasaNr")
    type_transaction = models.CharField(max_length=200)
    value = models.FloatField(null=True, blank=True, help_text="Waarde")



class ReceiverEmail(models.Model):
    email = models.CharField(max_length=200)
    receive_sync_successull_email = models.BooleanField(default=False)
    receive_sync_unsuccessull_email = models.BooleanField(default=False)
    receive_missing_schedule_email = models.BooleanField(default=False)

    def __str__(self):
        return str(f'{self.email}')


class CustomCommand(models.Model):
    command = models.CharField(max_length=200)

    def __str__(self):
        return str(f'{self.command}')


class ArticleType(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return str(f'{self.name}')
    
class Event(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return str(f'{self.name}')

class DatedEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(f'{self.event} - {self.date}')


class Article(models.Model):
    article_number = models.CharField(max_length=50, unique=True)
    article_name = models.CharField(max_length=200, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    article_type = models.ForeignKey(ArticleType, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(DatedEvent, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(f'{self.article_number} - {self.article_name}')





class Agreflor(models.Model):
    store_number = models.IntegerField()
    store_name = models.CharField(max_length=200)
    gtin_number = models.IntegerField()
    units = models.IntegerField()
    turnover = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    product_category = models.CharField(max_length=50, choices=[('Bloemen', 'Bloemen'), ('Planten', 'Planten'),])


class Antenna(models.Model):
    registration_number_debtor = models.IntegerField()
    debtor_number = models.IntegerField()
    debtor_name = models.CharField(max_length=128)
    year = models.IntegerField()
    week = models.CharField(max_length=128)
    invoice_date = models.DateField()
    invoice_number = models.CharField(max_length=128)
    invoice_text = models.CharField(max_length=256)
    invoice_quantity = models.TimeField(null=True, blank=True)
    invoice_minutes = models.FloatField(null=True, blank=True)
    invoice_type = models.CharField(max_length=128)
    rate = models.FloatField(null=True, blank=True)
    type_hour = models.CharField(max_length=128, null=True, blank=True)
    allowace_rate = models.FloatField()
    invoice_amount = models.FloatField()
    vat = models.FloatField(null=True, blank=True)
    resource_number = models.IntegerField()
    resource_name = models.CharField(max_length=128)
    date_worked = models.DateField(null=True, blank=True)


class Wematrans(models.Model):
    week = models.IntegerField()
    date = models.DateField()
    loading_address = models.CharField(max_length=512)
    file = models.FloatField()
    quantity = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=512)
    unloading_address = models.CharField(max_length=512)
    vat_code = models.CharField(max_length=64)
    unit_price = models.FloatField()
    amount = models.FloatField()
    file_reference = models.CharField(max_length=256, null=True, blank=True)
    invoice_number = models.BigIntegerField()



class CustomerReceiverEmail(models.Model):

    DAILY = 'Daily'
    WEEKLY = 'Weekly'
    MONTHLY = 'Monthly'
    YEAR_IN_SCHOOL_CHOICES = [
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    email_address = models.EmailField(max_length=128)
    active = models.BooleanField(default=True)
    interval = models.CharField(max_length=128, choices=YEAR_IN_SCHOOL_CHOICES, default=DAILY)
    last_sent_email_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('customer', 'email_address',)


    
class Attachment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    read = models.BooleanField(default=True)
    file_path = models.CharField(max_length=1024)
    recieve_date = models.DateTimeField(null=True, blank=True)
    process_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.process_date:
            self.process_date = timezone.now()
        super().save(*args, **kwargs)
