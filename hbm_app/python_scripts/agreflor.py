import datetime
import pandas
import os
import re
from hbm_app.python_scripts.schedules import complete_schedule
import pandas as pd
from hbm_app.models import AhWeekTransaction
import hbm_app.email_handler.extract_email_inbox as extract_email_inbox
from hbm_app.models import Agreflor

class ExcelDataParser:
    def __init__(self, customer, extracted_file):        
        self.df = pd.read_excel(extracted_file, sheet_name=customer.tab_name, header=None)
        self.customer = customer
        self.year = ''
        self.week = ''

    def date_from_weeknumber(self):
            day_number = 1 # Interval is 7, only each monday it's checked if the file was sent. .
            # Set and return datetime object. Used G and V to correspond to ISO 8601 date values
            return datetime.datetime.strptime(f'{self.year}-{self.week}-{day_number}', "%G-%V-%u")

    def get_week_from_file_name(self, attachment):
        return attachment[attachment.lower().rfind('wk')+2 : attachment.lower().rfind('yr')]

    def get_year_from_file_name(self, attachment):
        return attachment[attachment.lower().rfind('yr')+2 : attachment.lower().rfind('.')]

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
            try: # When attachment isn't found,
                pandas.read_excel(attachment, sheet_name=customer.tab_name)
            except ValueError:
                continue
            self = ExcelDataParser(customer, attachment)

            file_dict = self.df.to_dict(orient='records')

            # Get start and end date from heading
            heading = file_dict[0].get(0).lower()
            start_date = list(heading.split(" "))[list(heading.split(" ")).index('from')+1]
            start_date = datetime.datetime.strptime(start_date, '%Y%m%d')
            end_date = list(heading.split(" "))[list(heading.split(" ")).index('to')+1]
            end_date = datetime.datetime.strptime(end_date, '%Y%m%d')
            self.year = self.get_year_from_file_name(attachment)
            self.week = self.get_week_from_file_name(attachment)
            file_date = self.date_from_weeknumber()

            if not file_date in schedule_date:
                schedule_date.append(file_date)
                complete_schedule(file_date.date(), customer, action, schedule_range=[start_date, end_date])

            # Getting category from attachment name 
            category = 'Bloemen' if 'bloemen' in attachment.lower() else 'Planten'
            for row in file_dict[2:]:
                data = {
                    'store_number': row[0],
                    'store_name': row[1].strip(),
                    'gtin_number': row[2],
                    'units': row[3],
                    'turnover': row[4],
                    'start_date': start_date,
                    'end_date': end_date,
                    'product_category': category
                }
                obj, created = Agreflor.objects.update_or_create(
                    start_date = data['start_date'],
                    end_date = data['end_date'],
                    store_number = data['store_number'],
                    gtin_number = data['gtin_number'],
                    defaults = data
                )
                if created:
                    result['records_created'] += 1
                else:
                    result['records_updated_or_skipped'] += 1

        # When email attachment has been handled, move it to archive. 
        extract_email_inbox.move_email_to_archive(action, email['email'])

    return result
