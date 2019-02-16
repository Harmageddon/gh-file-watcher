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
    def indent_subsequent(string):
        padding = '  '
        return padding.join(string.splitlines(True))

    @staticmethod
    def notify_pr(file, pr):
        return '*{}* has been {} in the following pull request:\n' \
               '  {} by {}\n' \
               '  {:d} additions, {:d} deletions\n' \
               '  {}\n' \
            .format(file['filename'], file['status'], pr['title'], pr['user']['login'], file['additions'],
                    file['deletions'], pr['html_url'])

    @staticmethod
    def notify_commit(file, commit):
        return '*{}* has been changed in the following commit:\n' \
               '  Author: {}. Committer: {}.\n\n' \
               '  {}\n\n' \
               '  {}\n' \
            .format(file, commit['author']['login'], commit['committer']['login'],
                    Notifier.indent_subsequent(commit['commit']['message']), commit['html_url'])

    @staticmethod
    def error(message):
        return 'An API request failed. Consider using authentication for your requests. ' \
               'Refer to the manual for more information.\n' \
               'Error message:\n\n' \
               '{}\n'\
            .format(message)
