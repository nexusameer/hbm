import os
import codecs
import hbm_app.email_handler.email_server as email_server
from string import Template
from hbm_app.models import ReceiverEmail

def send_sync_log(action, error=False, output=[]):
    sender_email = email_server.init_email_server()
    query_params = {}
    if action.completed:
        query_params['receive_sync_successull_email'] = True
        result = { 'result': 'Succesvol', 'color': '#2eb85c' }
    else:
        query_params['receive_sync_unsuccessull_email'] = True
        result = { 'result': 'Onsuccesvol', 'color': '#e84a3e' }
    receiver_emails = ReceiverEmail.objects.filter(**query_params).values_list('email', flat=True)
    if not receiver_emails:
        email_server.close_server()
        return
    emails = [ 
        { 
            'receivers': list(receiver_emails),
            'subject': f'Status: {result.get("result")} - Synchronisatie log overzicht',
            'preview': 'Hier is een overzicht van de logs van afgelopen run.',
            'template': 'email_sync_log'
        },
    ]

    output_html = ""
    for x in output:
        output_html = output_html + f"<b> {x['customer']}: </b><br>Result: {x['result']}<br>"
        
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with codecs.open(dir_path+'/email_templates/default_template.html', 'r') as email_template_file:
        email_template = str(email_template_file.read())

    for item in emails:
        # Open email template
        with codecs.open(dir_path+'/email_templates/' + item.get('template') + '.html', 'r') as email_text_raw:
            email_text_raw = str(email_text_raw.read())

        email_text = Template(email_text_raw).substitute(action=action.action, start_date=action.start_date, end_date=action.end_date, test=action.test, post_to_database=action.post_to_database, **result, error=error, output=output_html)

        message = Template(email_template).substitute(preview=item['preview'], email_text=email_text)
        
        msg = email_server.msg_generator(sender_email, item['receivers'], item['subject'], message, files=item.get('files'), cc=item.get('cc_email'), bcc=item.get('bcc_email'))
        receivers = item.get('receivers')
        if item.get('cc_email'):
            receivers.extend(item.get('cc_email'))
        if item.get('bcc_email'):
            receivers.extend(item.get('bcc_email'))
        email_server.send_email(sender_email, receivers, msg, email_text)

    email_server.close_server()
