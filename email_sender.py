# -*- coding: utf-8 -*-
import smtplib
from email import MIMEMultipart
from email import MIMEText
from email import MIMEBase
from email import encoders
import os


class EmailSender(object):

    def __init__(self, img_folder, subject, body):
        self.email_from = 'contacto@fundaciontelefonica.com'
        self.email_pwd = ''

        self.email_subject = subject
        self.body = body

        self.img_folder = img_folder

    def compose_message(self, email_to, file_name):
        # Basic e-mail
        msg = MIMEMultipart.MIMEMultipart()
        msg['from'] = self.email_from
        msg['to'] = email_to
        msg['Subject'] = self.email_subject
        msg.attach(MIMEText.MIMEText(self.body, 'plain'))

        # Image attachment
        file_path = self.img_folder + file_name
        if os.path.isfile(file_path):
            attachment = open(file_path, 'rb')
            part = MIMEBase.MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename= %s' % file_name)
            msg.attach(part)

            # Message as string
            text = msg.as_string()
        else:
            text = None
        return text

    def server_login(self):
        # Login Email Server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.email_from, self.email_pwd)
        return server

    def send_email(self, email_to, file_name):
        # Compose message
        email_msg = self.compose_message(email_to, file_name)
        if email_msg is not None:
            # Get server
            server = self.server_login()
            # Send e-mail
            try:
                server.sendmail(self.email_from, email_to, email_msg)
                print('E-mail sent to address: ' + email_to + ' with attached file' + file_name)
            except smtplib.SMTPRecipientsRefused:
                print('Not a valid address!')
            # Close server
            server.quit()
        else:
            print('I have not found any png available with the name: ' + file_name)
            print('Sorry, not possible to send e-mail without attachment.')
