#!/usr/bin/env python

'''Version 0.2

Usage: main dev|prod
'''

import os
import sys
import csv
import datetime
import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MessageMaker:
    '''Fetch the info you want to send, put it together, and send it'''
    def __init__(self, configuration):
        self._config = configuration
        self.date = str(datetime.datetime.now())

    def get_recipient_info(self):
        self.first = self._config.recipient_info['first']
        self.last = self._config.recipient_info['last']
        self.recipient_email_address = self._config.recipient_info['email_address']

    def get_subject_line(self):
        self.subject_line = str(datetime.datetime.now()) + " - EMailSender Message"

    def get_message_data(self):
        self.message_data = "Some info rendered as a string."

    def get_footer(self):
        self.footer = "Some post-message text."

    def make_message_text(self):
        self.message_text = self._config.plaintext_message.format(date = self.date,
                                                        first = self.first,
                                                        last = self.last,
                                                        message_text = self.message_data,
                                                        footer = self.footer)
    def make_message_html(self):
        self.message_html = self._config.html_message.format(date = self.date,
                                                    first = self.first,
                                                    last = self.last,
                                                    message_text = self.message_data,
                                                    footer = self.footer)
    def send_message(self):
        m = MIMEMultipartEmailBuilder(subject = self.subject_line,
                                from_addr = self._config.smtp_config['login_id'],
                                to_addr = self.recipient_email_address,
                                message_text = self.message_text,
                                message_html = self.message_html)
        s = EmailSender(self._config.smtp_config,
                         self._config.smtp_config['login_id'],
                         self.recipient_email_address,
                         m.message)
        s.send()

class MIMEMultipartEmailBuilder:
    '''Build a MIMEMultipart object with this class.

    All parts except 'from_addr' (string) are optional.

    Init builds a .message object for use in SMTPlib.

    Note: do not include BCC recipients in any addressing,
    put this list in the EmailSender class.'''
    def __init__(self,
        subject='None',
        from_addr='',
        to_addr=[],
        cc_addr=[],
        message_text='None',
        message_html='None',
        file_attach='None'):
        self.message = MIMEMultipart('alternative')
        if subject != 'None':
            self.message['Subject'] = subject
        self.message['From'] = from_addr
        if len(to_addr) > 1:
            self.message['To'] = ','.join(to_addr)
        else:
            self.message['To'] = to_addr[0]
        if len(cc_addr) > 1:
            self.message['CC'] = ','.join(cc_addr)
        elif len(cc_addr) == 1:
            self.message['CC'] = cc_addr[0]
        self.part1 = MIMEText(message_text, 'plain')
        self.message.attach(self.part1)
        if message_html != 'None':
            self.part2 = MIMEText(message_html, 'html')
            self.message.attach(self.part2)
        if file_attach != 'None':
            fp = open(file_attach)
            self.attachment = MIMEText(fp.read(), _subtype='text/csv')
            fp.close()
            self.attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_attach))
            self.message.attach(self.attachment)

class EmailSender:
    '''Send your email message using this class.

    'smtp_conf' dictionary with:
        'host', 'port', 'login_id', and 'passwd'.
    'sender' email address as string
    'recipients' list of email address
        Note: you can safely include BCC recipients in this list.
    'message' can be string, or a MIMEMultipart object
    '''
    def __init__(self, smtp_conf, sender, recipients, message):
        self.sender = sender
        self.recipients = recipients
        self.conf = smtp_conf
        self.msg = message
    def send(self):
        """'send' sends message"""
        with smtplib.SMTP(host=self.conf['host'],port=self.conf['port']) as s:
            s.starttls()
            s.login(self.conf['login_id'],self.conf['passwd'])
            s.sendmail(self.sender,
                       self.recipients,
                       str(self.msg))

def main():
    env = sys.argv[1] if len(sys.argv) >= 2 else 'prod'
    global config
    if env == 'dev':
        config = config.Development()
    elif env == 'prod':
        config = config.Production()
    else:
        raise ValueError('Invalid environment name')

    mm = MessageMaker(config)
    mm.get_recipient_info()
    mm.get_subject_line()
    mm.get_message_data()
    mm.get_footer()
    mm.make_message_text()
    mm.make_message_html()
    mm.send_message()

if __name__ == "__main__":
    main()
