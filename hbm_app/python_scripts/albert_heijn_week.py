import datetime
import pandas
import os
import re
from hbm_app.python_scripts.schedules import complete_schedule
import pandas as pd
from hbm_app.models import AhWeekTransaction, Article
import hbm_app.email_handler.extract_email_inbox as extract_email_inbox

class ExcelDataParser:
    def __init__(self, customer, extracted_file):        
        self.df = pd.read_excel(extracted_file, sheet_name=customer.tab_name)
        self.customer = customer
        self.columns = []
        self.year = ''
        self.week = ''

    def get_cell_column_from_coordinates(self, cell_name):
        # Split cell coordinates between column and header
        cell_coordinates = re.split('(\d+)', cell_name)[0:2]
        # Only first two values are taken, column and row, as the third value is an empty string.
        # Excel-style column name to number, e.g., A = 1, Z = 26, AA = 27, AAA = 703.

        n = 0
        for c in cell_coordinates[0]:
            n = n * 26 + 1 + ord(c) - ord('A')
        return n - 1  # -1 as A should be 0, B should be 1, etc.

    def get_cell_row_from_coordinates(self, cell_name):
        cell_coordinates = re.split('(\d+)', cell_name)[0:2]
        row = int(cell_coordinates[1]) - 2
        return row

    def get_cell_value_from_coordinates(self, cell_name):
        column = self.get_cell_column_from_coordinates(cell_name)
        row = self.get_cell_row_from_coordinates(cell_name)
        return self.df.iloc[row, column]

    def define_location_other_columns(self):
        columns = {}
        # Make an dictionary with the columns indices, based on the name of the column, so the code will still work when the columns shift position. 
        for index, value in enumerate(self.df.iloc[self.customer.row_headers - 2]):
            if isinstance(value, (str, int)):
                value = value.strip()
                if value == self.customer.column_article:
                    columns['article'] = index
                elif value == self.customer.column_transaction_type:
                    columns['type_transaction'] = index
                elif value == self.customer.column_number_of_units:
                    if index == self.get_cell_column_from_coordinates(self.customer.cell_forecast_number_of_units):
                        columns['forecast_number_of_units'] = index
                    if index == self.get_cell_column_from_coordinates(self.customer.cell_actual_number_of_units):
                        columns['actual_number_of_units'] = index
                elif value == self.customer.column_purchase_price:
                    columns['forecast_purchase_price'] = index
                elif value == self.customer.column_sale_price:
                    columns['forecast_sale_price'] = index
                elif value == self.customer.column_revenue:
                    if index == self.get_cell_column_from_coordinates(self.customer.cell_forecast_revenue):
                        columns['forecast_revenue'] = index
                    if index == self.get_cell_column_from_coordinates(self.customer.cell_actual_revenue):
                        columns['actual_revenue'] = index
                elif value == self.customer.column_gross_profit:
                    columns['actual_gross_profit'] = index
                elif value == self.customer.column_loss:
                    columns['actual_loss'] = index
                elif index == self.get_cell_column_from_coordinates(self.customer.column_store_count):
                    columns['store_count'] = index
                elif index == self.get_cell_column_from_coordinates(self.customer.column_rotation):
                    columns['rotation'] = index
        self.columns = columns

    def get_cell_data(self):
        for index, row in self.df.iloc[self.customer.row_headers - 1:].iterrows():
            row = row.fillna('None')
            result = {}
            for idx, column in enumerate(self.columns):
                if (isinstance(row[self.columns[column]], str) or isinstance(row[self.columns[column]],
                                                                             float) or isinstance(
                    row[self.columns[column]], int)) and (row[self.columns[column]] != 'None'):
                    result[column] = row[self.columns[column]]
            if bool(result) and 'article' in result.keys():
                self.get_output(result)
                self.check_article(row)

    def check_article(self, row):
        if not Article.objects.filter(article_number=row[self.columns.get('article')], customer=self.customer).exists():
            Article.objects.create(
                article_number = row[self.columns.get('article')],
                article_name = row[self.columns.get('article') + 1],
                customer = self.customer
            )
            self.result['articles_created'] += 1

    def get_output(self, data_instance):
        data_instance['week'] = self.week
        data_instance['year'] = self.year
        obj, status = AhWeekTransaction.objects.update_or_create(
            year=data_instance['year'], 
            week=data_instance['week'], 
            type_transaction=data_instance['type_transaction'], 
            article=data_instance['article'], 
            defaults=data_instance
        )
        if status:
            self.result['records_created'] += 1
        else:
            self.result['records_updated_or_skipped'] += 1

    def date_from_weeknumber(self):
        day_number = 1 # Interval is 7, only each monday it's checked if the file was sent. .
        # Set and return datetime object. Used G and V to correspond to ISO 8601 date values
        return datetime.datetime.strptime(f'{self.year}-{self.week}-{day_number}', "%G-%V-%u")

def read_input(customer, action, email_attachment_list):
    # Initialize schedule date
    schedule_date = []
    # Initialize result
    result = {
        'records_created': 0,
        'records_updated_or_skipped': 0,
        'articles_created': 0
    }
    for email in email_attachment_list: 
        for attachment in email['attachments']:
            try: # When attachment isn't found, 
                pandas.read_excel(attachment, sheet_name=customer.tab_name)
            except ValueError:
                continue
            self = ExcelDataParser(customer, attachment)
            self.year = self.get_cell_value_from_coordinates(self.customer.cell_year)
            self.week = self.get_cell_value_from_coordinates(self.customer.cell_week)
            file_date = self.date_from_weeknumber()
            # If there is a new date, the schedule should be updated to True as completed. 
            if not file_date in schedule_date:
                schedule_date.append(file_date)
                complete_schedule(file_date.date(), customer, action)
            self.result = result
            self.define_location_other_columns()
            self.get_cell_data()

            result = self.result

    return result
