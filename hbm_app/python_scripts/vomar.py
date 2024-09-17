import pandas
import os    
import datetime
from django.utils import timezone
import hbm_app.python_scripts.hbm_api as hbm_api
from hbm_app.models import Transaction, Article
from hbm_app.python_scripts.schedules import complete_schedule
import hbm_app.email_handler.extract_email_inbox as extract_email_inbox

def read_input(customer, action):
    
    # Extract files from the emails in the inbox. 
    email_attachment_list = extract_email_inbox.read_inbox(action, customer.email, customer_name=customer.name)

    # Initialize result
    result = {
        'records_created': 0,
        'records_skipped': 0
    }

    for email in email_attachment_list: 
        for attachment in email['attachments']:

            # Open tab 'Lijst' from Excel file and load into Pandas dataframe
            excel_data_df = pandas.read_excel(attachment, sheet_name='Lijst')

            # Define the row where the columns start. Number gets substracted by 2 as the count starts at 0 vs 1, and the first row is the header row. 
            column_row = excel_data_df.iloc[customer.row_headers - 2]

            # Make an dictionary with the columns indices, based on the name of the column, so the code will still work when the columns shift position. 
            columns = {}
            for idx, value in enumerate(column_row):
                if value == customer.column_date:
                    columns['date'] = idx
                elif value == customer.column_store:
                    columns['store'] = idx
                elif value == customer.column_article:
                    columns['article'] = idx
                elif value == customer.column_sold_units:
                    columns['sold_units'] = idx
                    columns['sold_amount'] = idx + 1
                elif value == customer.column_loss_units:
                    columns['loss_units'] = idx
                    columns['loss_amount'] = idx + 1  
                elif value == customer.column_margin:
                    columns['margin'] = idx

            # Initialize schedule date
            schedule_date = ""

            # Loop over rows.
            for index, row in excel_data_df.iloc[customer.row_headers:].iterrows():
                schedule_date, result = loop_excel_file(row, customer, columns, action, schedule_date, result)

        # When email attachment has been handled, move it to archive. 
        extract_email_inbox.move_email_to_archive(action, email['email'])

    return result


def loop_excel_file(row, customer, columns, action, schedule_date, result):
    # Check if there is a date in the transaction line, if there is a date, it isn't a total.
    if isinstance(row[columns['date']], datetime.date):
        # Check if transaction line already exists in database, in that case, it should not be uploaded anymore. 
        # Transaction exist if the date, store and article already exist in database. 
        
        # Localize date to make it timezone aware.
        check_date = timezone.get_current_timezone().localize(row[columns.get('date')])

        # If there is a new date, the schedule should be updated to True as completed. 
        if schedule_date != check_date.date():
            schedule_date = check_date.date()
            complete_schedule(schedule_date, customer, action)

        check_article(row, columns, customer)

        if not Transaction.objects.filter(article=row[columns.get('article')], store=row[columns.get('store')], date=check_date).exists():
            result = output(row, check_date, customer, columns, action, result)
        else:
            result['records_skipped'] += 1
    return schedule_date, result


def check_article(row, columns, customer):
    if not Article.objects.filter(article_number=row[columns.get('article')], customer=customer).exists():
        Article.objects.create(
            article_number = row[columns.get('article')],
            article_name = row[columns.get('article') + 1],
            customer = customer
        )

def output(data, check_date, customer, columns, action, result):
    # Replace NaN values with 0
    data = data.fillna(0)

    # Post to database
    if action.post_to_database:
        Transaction.objects.create(
            customer = customer,
            store = data[columns.get('store')],
            article = data[columns.get('article')],
            date = check_date,
            sold_units = data[columns.get('sold_units')],
            sold_amount = data[columns.get('sold_amount')],
            loss_units = data[columns.get('loss_units')],
            loss_amount = data[columns.get('loss_amount')],
            margin = data[columns.get('margin')]
        )   
        result['records_created'] += 1
    return result