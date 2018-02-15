import threading
from django.core.mail import EmailMultiAlternatives


class EmailThread(threading.Thread):

    def __init__(self, subject, html_content,
                 recipient_list, document=None, filename=None):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.document = document
        self.filename = filename
        threading.Thread.__init__(self)

    def run(self):

        msg = EmailMultiAlternatives(self.subject, self.html_content, None,
                                     self.recipient_list)
        msg.attach_alternative(self.html_content, 'text/html')

        if self.document:
            msg.attach(self.filename, self.document, 'application/pdf')
        msg.send()


def send_html_mail(subject, html_content, recipient_list):
    EmailThread(subject, html_content, recipient_list).start()


def send_attach_mail(subject, html_content,
                     recipient_list, document, filename):
    EmailThread(subject, html_content, recipient_list,
                document, filename).start()
