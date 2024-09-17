from hbm_app.models import Customer, Schedule
import datetime

def create_schedule():
    all_customers = Customer.objects.all()
    for customer in all_customers:
        query_params = {}
        if customer.interval == 1:
            query_params['date'] = datetime.date.today()
        else:
            query_params['date__gt'] = datetime.date.today() - datetime.timedelta(customer.interval)
        schedule_found = Schedule.objects.filter(customer=customer, **query_params)
        if not schedule_found:
            Schedule.objects.create(customer=customer, date=datetime.date.today(), completed=False)


def complete_schedule(schedule_date, customer, action, schedule_range=[]):
    if action.post_to_database:
        if schedule_range:
            schedule = Schedule.objects.filter(customer=customer, date__range=schedule_range, completed=False).update(completed=True)
            return
        schedule = Schedule.objects.filter(customer=customer, date=schedule_date, completed=False)
        if bool(schedule):
            schedule[0].completed = True
            schedule[0].save()
