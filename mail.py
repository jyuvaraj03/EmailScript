import smtplib
import config
import csv
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from collections import namedtuple

def send_mails():
    try:
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo()
        server_ssl.login(config.sender_email,config.sender_password)
        messages = generate_emails()
        for message in messages:
            try:
                server_ssl.send_message(message)
                print('Successfully sent the mail to {}', message['To'])
            except:
                print('Failed to send mail to {}', message['To'])
        server_ssl.close()
    except:
        print('Failed to send mails ')

def generate_emails():
    messages = []
    EmailReceipient = namedtuple('EmailReceipient', 'email, attachment_name')
    for receipient in map(EmailReceipient._make, csv.reader(open(config.csv_file_name, 'r'))):
        print(receipient.email, receipient.attachment_name)
        message = EmailMessage()
        message['Subject'] = config.subject
        message['From'] = config.sender_email
        message.set_content(config.body)
        message.make_mixed()
        message['To'] = receipient.email

        with open('certificates/{}.pdf'.format(receipient.attachment_name), 'rb') as f:
            attachment = MIMEApplication(f.read(),_subtype="pdf")
            attachment.add_header('Content-Disposition','attachment',filename=config.attachment_name)
            message.attach(attachment)

        messages.append(message)

    return messages

send_mails()
