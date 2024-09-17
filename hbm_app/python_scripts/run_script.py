import os
import traceback
from datetime import datetime
from django.utils import timezone
from hbm_app.models import ActionLog, ErrorLog, Customer

import hbm_app.python_scripts.vomar as vomar
import hbm_app.python_scripts.albert_heijn_day as ah_day
import hbm_app.email_handler.email_action_log as email_log
import hbm_app.email_handler.email_uncomplete_schedule as uncomplete_schedule
import hbm_app.python_scripts.albert_heijn_week as ah_week
import hbm_app.python_scripts.agreflor as agreflor
import hbm_app.python_scripts.antenna as antenna
import hbm_app.python_scripts.albert_heijn_period as ah_period
import hbm_app.python_scripts.wematrans as wematrans
import hbm_app.python_scripts.duinisveldbreugem as duinisveldbreugem
import hbm_app.python_scripts.floriway as floriway


def check_customer_data(action):
    # all_customers = Customer.objects.all()
    all_customers = Customer.objects.filter(name="Floriway")  
    email_attachment_list = []
    for customer in all_customers:
        result = None
        if customer.name == "Vomar":
            result = vomar.read_input(customer, action)
        elif customer.name == "Albert Heijn (Dag)":
            result, email_attachment_list = ah_day.read_input(customer, action)
        elif customer.name == "Albert Heijn (Week)":
            result = ah_week.read_input(customer, action, email_attachment_list)
        elif customer.name == "Albert Heijn (Period)":
            result = ah_period.read_input(customer, action)
        elif customer.name == "Agreflor":
            result = agreflor.read_input(customer, action)
        elif customer.name == "Antenna":
            result = antenna.read_input(customer, action)
        elif customer.name == "Wematrans":
            result = wematrans.read_input(customer, action)
        elif customer.name == "DuinisveldBreugem":
            result = duinisveldbreugem.read_input(customer, action)
        elif customer.name == "Floriway":
            result = floriway.read_input(customer, action)
        
        output.append({'customer': customer.name, 'result': result})


def check_uncomplete_schedules(action):
    all_customers = Customer.objects.all()
    uncomplete_schedule.uncomplete_schedule(all_customers, action)


def handle_error(action):
    error = traceback.format_exc()
    print(error)
    if not action.test:
        ErrorLog.objects.create(action=action, timestamp=datetime.now(tz=timezone.get_current_timezone()), error=error)
        email_log.send_sync_log(action, error)  
    else:
        print('Test, so no email send.')


def new_action(function_name, test, post_to_database):
    return ActionLog.objects.create(action=function_name, test=test, start_date=datetime.now(tz=timezone.get_current_timezone()), post_to_database=post_to_database)


def action_completed(action):
    action.completed = True
    action.end_date = datetime.now(tz=timezone.get_current_timezone())
    action.save()


def run_function(function_name):
    # Init output as global variable. 
    global output
    output = []
    action = new_action(function_name, test=bool(os.getenv('TEST')), post_to_database=True)
    try: 
        eval(function_name + "(action)")
        action_completed(action)
        if not action.test:
            email_log.send_sync_log(action, output=output)
        else:
            print('Success!')
            print('Test, so no email send.')
            print(output)
    except Exception as e: 
        print(f'\n\n ERROR: \n {output}')
        handle_error(action)
    