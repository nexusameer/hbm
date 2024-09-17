import datetime
import pandas
import os
import re
from django.utils import timezone
from hbm_app.models import AhDayTransaction
from hbm_app.python_scripts.schedules import complete_schedule
import hbm_app.email_handler.extract_email_inbox as extract_email_inbox


def read_input(customer, action):
    # Defines in what column the days are, also calculates the date based on the year, weeknumber and day. 
    def define_location_day_columns_and_date(df, customer, days_list):
        def date_from_weeknumber(day_list, day, weeknumber, year):
            day = day.lower() # Convert to lower case to prevent differences in capitalization.
            day_number = day_list.index(day) +1 # Increment with one as Monday is index 0, but day 1, etc.
            # Set and return datetime object. Used G and V to correspond to ISO 8601 date values
            return datetime.datetime.strptime(f'{year}-{weeknumber}-{day_number}', "%G-%V-%u") 
        
        # Init lists
        day_columns = []
        dates = []

        # Get Year and Weeknumber based on the customer. 
        year = get_cell_value_from_coordinates(df, customer.cell_year)
        weeknumber = get_cell_value_from_coordinates(df, customer.cell_week)
        
        for index, day in enumerate(df.iloc[customer.row_days-2]):
            if isinstance(day, str) and day.lower() in days_list:
                day_columns.append(index)
                dates.append(date_from_weeknumber(days_list, day, weeknumber, year))
        return day_columns, dates

    def define_location_other_columns(df, customer):
        columns = {}
        # Make an dictionary with the columns indices, based on the name of the column, so the code will still work when the columns shift position. 
        for index, value in enumerate(df.iloc[customer.row_headers-2]):
            if value == customer.column_article:
                columns['article'] = index
            elif value == customer.column_transaction_type:
                columns['column_transaction_type'] = index
        return columns


    # Initialize result
    result = {
        'records_created': 0,
        'records_updated_or_skipped': 0
    }

    # Takes the days, and converts it into a list by splitin on the comma. Also converts to lower case.     
    days_list = [x.strip().lower() for x in customer.days_list.split(',')]

    # Extract files from the emails in the inbox. 
    email_attachment_list = extract_email_inbox.read_inbox(action, customer.email, customer_name=customer.name)
    for email in email_attachment_list: 
        allow_move = False
        for attachment in email['attachments']:
            # Open tab from Excel file and load into Pandas dataframe. If Excel sheet cannot be opened because it doesn't exist, loop will continue
            try:
                df = pandas.read_excel(attachment, sheet_name=customer.tab_name)
            except ValueError:
                continue

            # Define in what columns the data is. 
            day_columns, dates = define_location_day_columns_and_date(df, customer, days_list)
            columns = define_location_other_columns(df, customer)

            result = loop_excel_file(df, customer, day_columns, columns, dates, action, result)
            allow_move = True
        # When email has been handled, move it to archive. 
        if allow_move:
            extract_email_inbox.move_email_to_archive(action, email['email'])
    
    return result, email_attachment_list


def get_cell_value_from_coordinates(df, variable):
    def excel_column_name_to_number(name):
        #Excel-style column name to number, e.g., A = 1, Z = 26, AA = 27, AAA = 703.
        n = 0
        for c in name:
            n = n * 26 + 1 + ord(c) - ord('A')
        return n -1 # -1 as A should be 0, B should be 1, etc. 

    # Split cell coordinates between column and header 
    cell_coordinates = re.split('(\d+)', variable)[0:2] # Only first two values are taken, column and row, as the third value is an empty string. 

    # Convert column to number (e.g. A=0, D=3, etc.)
    column = excel_column_name_to_number(cell_coordinates[0])
    # -2 on row, as first row has ID 0, second row has ID 1, etc. andthe other row is the header. 
    row = int(cell_coordinates[1])-2
    return df.iloc[row, column]


def loop_excel_file(df, customer, day_columns, columns, dates, action, result):
    # Initialize schedule date
    schedule_date = []

    for index, row in df.iloc[customer.row_headers-1:].iterrows():
        # Check if there is an article number in the transaction line, if there is an article number, then it is a transaction.
        if isinstance(row[columns['article']], (str, int)):
            for idx, day_column in enumerate(day_columns):
                # Check if there is data in the column of the day. If no data is there, it can be skipped. It checks both the forecast (P) as well as the actual (R, which is always one next to P), as if one of them is empty, the other one doesn't have to be empty. 
                if row[day_column] > 0 or row[day_column+1] > 0:

                    # Localize date to make it timezone aware.
                    transaction_date = timezone.get_current_timezone().localize(dates[idx])

                    # If there is a new date, the schedule should be updated to True as completed. 
                    if not transaction_date in schedule_date:
                        schedule_date.append(transaction_date)
                        complete_schedule(transaction_date.date(), customer, action)
                    result = output(row, day_column, columns, transaction_date, action, result)

    return result


def output(row, day_column, columns, transaction_date, action, result):
    # Replace NaN values with 0
    row = row.fillna(0)

    if action.post_to_database:
        # Check if transaction line exists. If it does exits, data should be updated. If it doesn't exit, new transaction line should be created. 
        transaction_line = AhDayTransaction.objects.filter(article=row[columns.get('article')], date=transaction_date)
        
        if transaction_line.exists():
            transaction_line = transaction_line[0] # Get first object from list (should only be one object per day per article number.)
            # Update only if the numbers changed 
            if transaction_line.estimation_units != round(row[day_column], 0) or transaction_line.sold_units != round(row[day_column+1], 0): 
                transaction_line.estimation_units = round(row[day_column], 0)
                transaction_line.sold_units = round(row[day_column+1], 0)
                transaction_line.save()
            result['records_updated_or_skipped'] += 1
        else: 
            # Article and Date combination doesn't exist yet. Create new transaction.
            AhDayTransaction.objects.create(
                article = row[columns['article']],
                date = transaction_date,
                type_transaction = row[columns['column_transaction_type']],
                estimation_units = round(row[day_column], 0),
                sold_units = round(row[day_column+1], 0),
            )
            result['records_created'] += 1
    return result