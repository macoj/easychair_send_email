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
                   delay=2, batch_size=50, smtp_host='smtphost.fit.edu', dry_run=False):
        message_file = open(message_file_name, 'rb')
        message = message_file.read()
        message_file.close()
        if subject is None:
            subject = '(no subject)'
        for recipient_i in range(0, len(recipients)):
            recipient = recipients[recipient_i]
            print "Constructing e-mail to (%d/%d): %s" % (recipient_i, len(recipients), recipient)
            message_i = message
            if replaces is not None:
                for replace in replaces:
                    print " > replacing '%s' with '%s'" % (replace[0], replace[1][recipient_i])
                    message_i = re.sub(re.escape(replace[0]), replace[1][recipient_i], message_i)
            content = MIMEText(message_i)
            content['From'] = sender
            content['To'] = recipient
            content['Subject'] = subject
            print "Sending to (%d/%d): %s" % (recipient_i, len(recipients), recipient)
            if not dry_run:
                mail_man = smtplib.SMTP(smtp_host)
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
            replaces_names = [c for c in replaces if c != "email"]
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
        message_file_name, recipients_file_name, sender, subject, delay, batch_size = sys.argv[1:7]
        delay, batch_size = int(delay), int(batch_size)
        if len(sys.argv) > 7:
            replaces = sys.argv[7:]
        else:
            replaces = None
        print "We are going to send some e-mails now..."
        print " from: '%s' " % sender
        print " to: '%s' " % recipients_file_name
        print " subject: '%s' " % subject
        print " message file: '%s' " % message_file_name
        print " replacing: " + str(replaces)
        print "using a delay of %d seconds between batches of %d" % (delay, batch_size)

        SendEmail.construct_email_and_send(
            message_file_name, recipients_file_name, sender, subject=subject, delay=delay, batch_size=batch_size, replaces=replaces)

