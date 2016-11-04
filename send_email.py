__author__ = 'marcos'
import smtplib
from email.mime.text import MIMEText


class SendEmail:
    def __init__(self):
        pass

    @staticmethod
    def send_email(message_file_name, sender, recipients, subject=None, replaces=None):
        message_file = open(message_file_name, 'rb')
        message = message_file.read()
        message_file.close()

        if subject is None:
            subject = '(no subject)'

        for recipient_i in range(len(recipients)):
            recipient = recipients[recipient_i]
            content = MIMEText(message)
            content['Subject'] = subject
            content['From'] = recipient
            content['To'] = sender

            s = smtplib.SMTP('smtphost.fit.edu')
            s.sendmail(sender, [recipient], content.as_string())
            s.quit()
    """
    execfile("send_email.py")
    SendEmail.send_email("hello.txt", "no-reply@fit.edu", ["moliveirajun2013@my.fit.edu", "syncmaxtor@gmail.com"])
    """