import datetime
import pandas
import os
from hbm_app.python_scripts.schedules import complete_schedule
import hbm_app.email_handler.extract_email_inbox as extract_email_inbox
from hbm_app.models import AhPeriodTransaction
# from datetime import timedelta
class ExcelDataParser:
    def __init__(self, customer, extracted_file):        
        self.df = pandas.read_excel(extracted_file, sheet_name=customer.tab_name, header=None)
        self.customer = customer

    def get_netherlands_date(self, year, week, day):
        # Define a dictionary to map Dutch day abbreviations to English day names
        day_mapping = {"MA": "Monday", "DI": "Tuesday", "WO": "Wednesday", "DO": "Thursday", "VR": "Friday", "ZA": "Saturday", "ZO": "Sunday"}

        # Get the English day name from the Dutch abbreviation
        english_day = day_mapping.get(day, "")

        # Calculate the date of the first day of the week
        first_day_of_week = datetime.datetime.strptime(f'{year}-W{int(week[1:]) }-{english_day}', "%G-W%V-%A")

        # Add 1 day to get the actual date of the specified day
        netherlands_date = first_day_of_week

        return netherlands_date.date()

def read_input(customer, action):
    
    # Extract files from the emails in the inbox. 
    email_attachment_list = extract_email_inbox.read_inbox(action, customer.email, customer_name=customer.name)
    # Initialize schedule date
    schedule_date = []
    # Initialize result
    result = {
        'records_created': 0,
        'records_updated_or_skipped': 0,
    }
    for email in email_attachment_list: 
        for attachment in email['attachments']:
            filename, file_extension = os.path.splitext(attachment)
            if not file_extension in ['.csv', '.xlsx', '.xls']:  #
                continue
            self = ExcelDataParser(customer, attachment)
            file_dict = self.df.to_dict(orient='records')
            for row in file_dict[1:]:
                date = self.get_netherlands_date(row[1], row[2], row[3])
                data = {
                    'date': date,
                    'year': row[1],
                    'week': row[2],
                    'day': row[3],
                    'nasa_number': row[4],
                    'type_transaction': row[5],
                    'value': row[6],
                }

                obj, created = AhPeriodTransaction.objects.update_or_create(
                    date = data['date'],
                    year = data['year'],
                    week = data['week'],
                    day = data['day'],
                    nasa_number = data['nasa_number'],
                    type_transaction = data['type_transaction'],
                    defaults = data
                )    
                print(f"{data['date']} - {data['nasa_number']} - {data['type_transaction']} ")

                file_date = date

                if not file_date in schedule_date:
                    schedule_date.append(file_date)
                    complete_schedule(file_date, customer, action)

                if created:
                    result['records_created'] += 1
                else:
                    result['records_updated_or_skipped'] += 1

        # When email attachment has been handled, move it to archive. 
        extract_email_inbox.move_email_to_archive(action, email['email'])
    return result
