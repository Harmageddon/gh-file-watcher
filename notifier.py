from email.mime.text import MIMEText
from subprocess import Popen, PIPE
import os.path


class Notifier:
    def __init__(self, mail_address):
        self.messages = []
        self.mail_address = mail_address

    def append(self, message, title=''):
        self.messages.append({'title': title, 'body': message})

    def send_notifications(self, title):
        for msg in self.messages:
            mail = MIMEText(msg['body'])
            mail['To'] = self.mail_address

            if msg['title'] != '':
                mail['Subject'] = msg['title']
            else:
                mail['Subject'] = title

            if os.path.exists('/usr/sbin/sendmail'):
                p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE, universal_newlines=True)
                p.communicate(mail.as_string())
            else:
                print('Sendmail is not installed. Mail that would have been sent:')
                print(mail.as_string())

    @staticmethod
    def notify_pr(file, pr):
        return '*{}* has been {} in the following pull request:\n' \
               '  {} by {}\n' \
               '  {:d} additions, {:d} deletions\n' \
               '  {}\n' \
            .format(file['filename'], file['status'], pr['title'], pr['user']['login'], file['additions'],
                    file['deletions'], pr['html_url'])
