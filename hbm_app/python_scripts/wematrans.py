import datetime
import pandas
import os
from hbm_app.python_scripts.schedules import complete_schedule
import hbm_app.email_handler.extract_email_inbox as extract_email_inbox
from hbm_app.models import Wematrans

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
            file_dict = self.df.to_dict(orient='records')
            for row in file_dict:
                if pandas.isnull(row.get('Datum')):
                    continue
                data = {
                    'week': row.get('Week'),
                    'date': datetime.datetime.strptime(row.get('Datum'), "%d-%m-%Y") if isinstance(row.get('Datum'), str) else row.get('Datum'),
                    'loading_address': row.get('Laadadres'),
                    'file': row.get('Dossier'),
                    'quantity': None if pandas.isnull(row.get('Aantal')) else row.get('Aantal'),
                    'description': row.get('Eenheid'), 
                    'unloading_address': row.get('Losadres'),
                    'vat_code': row.get('BTW'),
                    'unit_price': row.get('Prijs p/e'),
                    'amount': row.get('Bedrag'),
                    'file_reference': row.get('Dossier referentie'),
                    'invoice_number': row.get('FactuurNr'),
                }

                obj, created = Wematrans.objects.update_or_create(
                    invoice_number = data['invoice_number'],
                    file = data['file'],
                    file_reference = data['file_reference'],
                    description = data['description'],
                    defaults = data
                )    
                print(f"{data['invoice_number']} - {data['date']} - {data['description']} ")

                file_date = data['date']
                end_date = file_date

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
