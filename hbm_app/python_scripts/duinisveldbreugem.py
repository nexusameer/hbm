import datetime
from django.utils import timezone
import hbm_app.python_scripts.hbm_api as hbm_api
from hbm_app.python_scripts.schedules import complete_schedule
import hbm_app.email_handler.extract_email_inbox_using_graph_api as extract_email_inbox
from duinisveldbreugem.models import Invoice, InvoiceItem
import xml.etree.ElementTree as ET

class InvoiceXMLReader:
    def __init__(self, file_path):
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()
        self.namespaces = {
            'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
            'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'
        }

    def get_invoice_id(self):
        return self.root.findtext('.//cbc:ID', namespaces=self.namespaces, default=None)

    def get_issue_date(self):
        return self.root.findtext('.//cbc:IssueDate', namespaces=self.namespaces, default=None)

    def get_due_date(self):
        return self.root.findtext('.//cbc:DueDate', namespaces=self.namespaces, default=None)

    def get_buyer_reference(self):
        return self.root.findtext('.//cbc:BuyerReference', namespaces=self.namespaces, default=None)

    def get_supplier_name(self):
        return self.root.findtext('.//cac:PartyName/cbc:Name', namespaces=self.namespaces, default=None)

    def get_supplier_city(self):
        return self.root.findtext('.//cac:PostalAddress/cbc:CityName', namespaces=self.namespaces, default=None)

    def get_supplier_country(self):
        return self.root.findtext('.//cac:PostalAddress/cac:Country/cbc:IdentificationCode',
                                  namespaces=self.namespaces, default=None)
    def get_vat(self):
        return self.root.findtext('.//cac:TaxTotal/cbc:TaxAmount',
                                  namespaces=self.namespaces, default=None)
    def get_total_excl_vat(self):
        return self.root.findtext('.//cac:LegalMonetaryTotal/cbc:TaxExclusiveAmount',
                                  namespaces=self.namespaces, default=None)
    def get_total_incl_vat(self):
        return self.root.findtext('.//cac:LegalMonetaryTotal/cbc:TaxInclusiveAmount',
                                  namespaces=self.namespaces, default=None)

    def get_invoice_lines(self):
        invoice_lines = []
        for line_element in self.root.findall('.//cac:InvoiceLine', namespaces=self.namespaces):
            line_id = line_element.findtext('cbc:ID', namespaces=self.namespaces, default=None)
            description = line_element.findtext('.//cbc:Description', namespaces=self.namespaces, default=None)
            amount_per_unit = line_element.findtext('.//cbc:PriceAmount', namespaces=self.namespaces, default=None)
            quantity = line_element.findtext('.//cbc:InvoicedQuantity', namespaces=self.namespaces, default=None)
            amount = line_element.findtext('.//cbc:LineExtensionAmount', namespaces=self.namespaces, default=None)
            invoice_lines.append({'LineID': line_id, 'Description': description, 'Amount': amount, 'AmountPerUnit': amount_per_unit, 'Quantity': quantity})
        return invoice_lines


def read_input(customer, action):
    
    # Extract files from the emails in the inbox. 
    email_attachment_list = extract_email_inbox.read_inbox(action, customer.email, customer_name=customer.name)
    # Initialize result
    result = {
        'invoices_created': 0,
        'invoices_updated_or_skipped': 0,
        'invoice_items_created': 0,
        'invoice_items_updated_or_skipped': 0,
    }
    archive_folder_id = extract_email_inbox.get_archive_folder_id()
    for email in email_attachment_list: 
        for attachment in email['attachments']:
            xml_reader = InvoiceXMLReader(attachment)
            
            # Accessing data using class methods
            invoice_number = xml_reader.get_invoice_id()
            invoice_date = xml_reader.get_issue_date()
            due_date = xml_reader.get_due_date()
            customer_number = xml_reader.get_buyer_reference()
            customer_number = customer_number.split(' - ')[0]
            supplier_name = xml_reader.get_supplier_name()
            supplier_city = xml_reader.get_supplier_city()
            supplier_country = xml_reader.get_supplier_country()
            invoice_lines = xml_reader.get_invoice_lines()
            vat = xml_reader.get_vat()
            total_excl_vat = xml_reader.get_total_excl_vat()
            total_incl_vat = xml_reader.get_total_incl_vat()

            invoice_data = {
                'customer_number': customer_number,
                'invoice_number': invoice_number,
                'invoice_date': invoice_date,
                'supplier_name': supplier_name,
                'supplier_city': supplier_city,
                'supplier_country': supplier_country,
                'vat': vat,
                'total_excluding_tax': total_excl_vat,
                'total_including_tax': total_incl_vat,
                'due_date': due_date,
            }

            invoice_obj, created = Invoice.objects.update_or_create(
                invoice_number=invoice_number,
                defaults=invoice_data
            )

            if created:
                result['invoices_created'] += 1
            else:
                result['invoices_updated_or_skipped'] += 1

            for line in invoice_lines:
                invoice_item_data = {
                    'invoice': invoice_obj,
                    'item_id': line['LineID'],
                    'description': line['Description'],
                    'quantity': line['Quantity'],
                    'unit_price': line['AmountPerUnit'],
                    'amount': line['Amount'],
                }
                invoice_item_obj, created = InvoiceItem.objects.update_or_create(
                    invoice=invoice_obj,
                    item_id=invoice_item_data['item_id'],
                    defaults=invoice_item_data
                )

                if created:
                    result['invoice_items_created'] += 1
                else:
                    result['invoice_items_updated_or_skipped'] += 1
        extract_email_inbox.move_email_to_archive(action, email['email']['id'], archive_folder_id)

    return result