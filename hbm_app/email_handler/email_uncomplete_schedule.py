import os
import codecs
import hbm_app.email_handler.email_server as email_server
from string import Template
from hbm_app.models import ReceiverEmail, Schedule, CustomerReceiverEmail
from django.utils import timezone
from django.db.models import Q

def uncomplete_schedule(all_customers, action):
    sender_email = email_server.init_email_server()
    schedule_result = ""
    for customer in all_customers:
        schedule_result_without_customer_name = ""
        schedules = Schedule.objects.filter(customer=customer, completed=False)
        if schedules:
            schedule_result = schedule_result + f"<h3> {customer.name} </h3> "
            for schedule in schedules: 
                dutch_day_names = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag", "Zaterdag", "Zondag"]
                day = dutch_day_names[schedule.date.weekday()]
                schedule_result = schedule_result + f"{schedule.date} ({day})<br>"
                schedule_result_without_customer_name = schedule_result_without_customer_name + f"{schedule.date} ({day})<br>"
            customer_specific_emails = CustomerReceiverEmail.objects.filter(customer=customer, active=True).values_list('email_address', flat=True)
            now = timezone.now().replace(minute=0, second=0) + timezone.timedelta(hours=1)
            daily_threshold = now - timezone.timedelta(days=1)
            weekly_threshold = now - timezone.timedelta(weeks=1)
            monthly_threshold = now - timezone.timedelta(days=30)
            result_list = customer_specific_emails.filter(
                Q(interval='Daily', last_sent_email_time__lte=daily_threshold) |
                Q(interval='Weekly', last_sent_email_time__lte=weekly_threshold) |
                Q(interval='Monthly', last_sent_email_time__lte=monthly_threshold)
            )
            if result_list and schedule_result_without_customer_name != "":
                send_emails_to_customers(customer.name, result_list, schedule_result_without_customer_name, sender_email)
                result_list.update(last_sent_email_time=timezone.now())



    if schedule_result == "":
        email_server.close_server()
        return
    receiver_emails = ReceiverEmail.objects.filter(receive_missing_schedule_email=True).values_list('email', flat=True)
    
    if not receiver_emails or schedule_result == "":
        email_server.close_server()
        return

    send_emails_to_admins(receiver_emails, schedule_result, sender_email)

    email_server.close_server()


def send_emails_to_admins(email_list, schedule_result, sender_email):

    emails = [ 
        { 
            'receivers': list(email_list),
            'subject': 'Overzicht niet aangeleverde dagen',
            'preview': 'Hier is een overzicht alle dagen die missen.',
            'template': 'email_uncomplete_schedule'
        },
    ]

    dir_path = os.path.dirname(os.path.realpath(__file__))
    with codecs.open(dir_path+'/email_templates/default_template.html', 'r') as email_template_file:
            email_template = str(email_template_file.read())

    for item in emails:
        # Open email template
        with codecs.open(dir_path+'/email_templates/' + item.get('template') + '.html', 'r') as email_text_raw:
            email_text_raw = str(email_text_raw.read())

        email_text = Template(email_text_raw).substitute(schedule_result=schedule_result)

        message = Template(email_template).substitute(preview=item['preview'], email_text=email_text)
        
        msg = email_server.msg_generator(sender_email, item['receivers'], item['subject'], message, files=item.get('files'), cc=item.get('cc_email'), bcc=item.get('bcc_email'))
        receivers = item.get('receivers')
        if item.get('cc_email'):
            receivers.extend(item.get('cc_email'))
        if item.get('bcc_email'):
            receivers.extend(item.get('bcc_email'))
        email_server.send_email(sender_email, receivers, msg, email_text)


def send_emails_to_customers(customer_name, email_list, schedule_result, sender_email):

    emails = [ 
        { 
            'receivers': list(email_list),
            'subject': 'We missen nog wat data',
            'preview': 'Hoorn Bloommasters - We missen nog wat data',
            'template': 'email_uncomplete_schedule_to_customer_emails'
        },
    ]

    dir_path = os.path.dirname(os.path.realpath(__file__))
    with codecs.open(dir_path+'/email_templates/default_template.html', 'r') as email_template_file:
            email_template = str(email_template_file.read())

    for item in emails:
        # Open email template
        with codecs.open(dir_path+'/email_templates/' + item.get('template') + '.html', 'r') as email_text_raw:
            email_text_raw = str(email_text_raw.read())

        email_text = Template(email_text_raw).substitute(schedule_result=schedule_result, customer_name=customer_name)

        message = Template(email_template).substitute(preview=item['preview'], email_text=email_text)
        
        msg = email_server.msg_generator(sender_email, item['receivers'], item['subject'], message, files=item.get('files'), cc=item.get('cc_email'), bcc=item.get('bcc_email'))
        receivers = item.get('receivers')
        if item.get('cc_email'):
            receivers.extend(item.get('cc_email'))
        if item.get('bcc_email'):
            receivers.extend(item.get('bcc_email'))
        email_server.send_email(sender_email, receivers, msg, email_text)