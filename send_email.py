#!/usr/bin/python2.7
import sys
import time
import re
import smtplib
import pandas as pd
from email.mime.text import MIMEText


class SendEmail:
    def __init__(self):
        pass

    @staticmethod
    def send_email(message_file_name, sender, recipients, subject=None, replaces=None,
                   delay=2, batch_size=50, smtp_host='smtphost.fit.edu'):
        message_file = open(message_file_name, 'rb')
        message = message_file.read()
        message_file.close()
        if subject is None:
            subject = '(no subject)'
        for recipient_i in range(0, len(recipients)):
            message_i = message
            if replaces is not None:
                for replace in replaces:
                    message_i = re.sub(re.escape(replace[0]), replace[1][recipient_i], message_i)
            recipient = recipients[recipient_i]
            content = MIMEText(message_i)
            content['From'] = sender
            content['To'] = recipient
            content['Subject'] = subject
            mail_man = smtplib.SMTP(smtp_host)
            print "Sending to (%d/%d): %s" % (recipient_i, len(recipients), recipient)
            mail_man.sendmail(mail_man, [recipient], content.as_string())
            mail_man.quit()
            if (recipient_i + 1) % batch_size == 0:
                print " waiting %d seconds " % delay
                time.sleep(delay)
    """
    execfile("send_email.py")
    SendEmail.send_email("CFP.txt", "admin@fit.edu", ["email1@host.com", "email2@host.com"], subject="Call for papers", batch_size=1)
    """

    @staticmethod
    def construct_email_and_send(
            message_file_name, recipients_file_name, sender, replaces=None, **kargs):
        recipients_data = pd.read_csv(recipients_file_name)
        recipients = list(recipients_data['email'])
        if replaces is not None:
            replaces_names = [c for c in recipients_data.columns if c != "email"]
            replaces = zip(replaces_names, [list(recipients_data[replace_name]) for replace_name in replaces_names])
        SendEmail.send_email(message_file_name, sender, recipients, replaces=replaces, **kargs)
    """
    execfile("send_email.py")
    SendEmail.construct_email_and_send("CFP.txt", "full_emaillist.csv", "no-reply@fit.edu", subject="Call for papers")
    """

if __name__ == '__main__':
    if len(sys.argv[1:]) < 6:
        print 'Usage:\n\t$ send_email.py message.txt recipient.csv sender@email.com "subject" delay batch_size'
        print " 'message.txt' might contain variables with the same name of the columns in 'recipient.csv', so" \
              "  it will be replaced by the respective values."
    else:
        message_file_name_, recipients_file_name_, sender_, subject_, delay_, batch_size_ = sys.argv[1:]
        delay_, batch_size_ = int(delay_), int(batch_size_)
        print "We are going to send some e-mails now..."
        print " from: '%s' " % sender_
        print " to: '%s' " % recipients_file_name_
        print " subject: '%s' " % subject_
        print " message file: '%s' " % message_file_name_
        print "using a delay of %d seconds between batches of %d" % (delay_, batch_size_)
        SendEmail.construct_email_and_send(
            message_file_name_, recipients_file_name_, sender_, subject=subject_, delay=delay_, batch_size=batch_size_)


