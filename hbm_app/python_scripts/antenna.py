import datetime
import pandas
import os
from hbm_app.python_scripts.schedules import complete_schedule
import hbm_app.email_handler.extract_email_inbox as extract_email_inbox
from hbm_app.models import Antenna

class ExcelDataParser:
    def __init__(self, customer, extracted_file, file_extension):  
        if file_extension == ".csv":
            self.df = pandas.read_csv(extracted_file, sep=";", dtype=str)#, engine='python', header=0 )  sep='delimiter' #header=None, sep='delimiter') #, header=None, sep='delimiter'
        elif file_extension == ".xlsx":
            self.df = pandas.read_excel(extracted_file, engine='openpyxl') 
        elif file_extension == ".xls":
            self.df = pandas.read_excel(extracted_file) 

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
            self = ExcelDataParser(customer, attachment, file_extension)
            self.df = self.df.dropna(subset=['Factuurnummer'])
            file_dict = self.df.to_dict(orient='records')
            for row in file_dict:
                if pandas.isnull(row.get('Datum gewerkt')):
                    row['Datum gewerkt'] = None
                data = {
                    'registration_number_debtor': row.get('Registratienummer relatie'),
                    'debtor_number': row.get('Debiteurennummer'),
                    'debtor_name': row.get('Naam relatie'),
                    'year': row.get('Declaratie jaar'),
                    'week': row.get('Declaratietijdvak'),
                    'invoice_date': datetime.datetime.strptime(row.get('Factuur datum'), "%d-%m-%Y") if isinstance(row.get('Factuur datum'), str) else row.get('Factuur datum'),
                    'invoice_number': row.get('Factuurnummer'),
                    'invoice_text': row.get('Factuur tekst'),
                    'invoice_quantity': row.get('Factuur aantal'),
                    'invoice_minutes': row.get('Factuur minuten'),
                    'invoice_type': row.get('Factuur soort'),
                    'rate': row.get('Tarief').replace(',', '.') if isinstance(row.get('Tarief'), str) else row.get('Tarief'),
                    'type_hour': row.get('Type uur'),
                    'allowace_rate': str(row.get('Tarief obv toeslagpercentage')).replace(',', '.'),
                    'invoice_amount': row.get('Factuurbedrag').replace(',', '.') if isinstance(row.get('Factuurbedrag'), str) else row.get('Factuurbedrag'),
                    'vat': None if row.get('Afwijkend BTW') == '' else row.get('Afwijkend BTW'),
                    'resource_number': row.get('Registratienummer persoon'),
                    'resource_name': row.get('Naam persoon'),
                    'date_worked': datetime.datetime.strptime(row.get('Datum gewerkt'), "%d-%m-%Y") if isinstance(row.get('Factuur datum'), str) else row.get('Datum gewerkt'),
                }

                if data['invoice_type'] == "GD":
                    obj, created = Antenna.objects.update_or_create(
                        invoice_number = data['invoice_number'],
                        week = data['week'],
                        resource_number = data['resource_number'],
                        invoice_amount = data['invoice_amount'],
                        defaults = data
                    )    
                else:
                    obj, created = Antenna.objects.update_or_create(
                        date_worked = data['date_worked'],
                        invoice_type = data['invoice_type'],
                        invoice_number = data['invoice_number'],
                        resource_number = data['resource_number'],
                        invoice_amount = data['invoice_amount'],
                        invoice_minutes = data['invoice_minutes'],
                        defaults = data
                    )
                print(f"{data['invoice_number']} - {data['date_worked']} - {data['resource_number']} ")

                file_date = data['invoice_date']
                end_date = file_date + datetime.timedelta(days=6)

                if not file_date in schedule_date:
                    schedule_date.append(file_date)
                    complete_schedule(file_date.date(), customer, action, schedule_range=[file_date, end_date])

                if created:
                    result['records_created'] += 1
                else:
                    result['records_updated_or_skipped'] += 1

        # When email attachment has been handled, move it to archive. 
        extract_email_inbox.move_email_to_archive(action, email['email'])

    return result
