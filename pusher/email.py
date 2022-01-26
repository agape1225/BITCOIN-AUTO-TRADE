import smtplib
from email.mime.text import MIMEText


class Email:

    def __init__(self):
        self.s = smtplib.SMTP('smtp.gmail.com', 587)
        self.s.starttls()
        self.s.login("wapp.study@gmail.com", "wapp1234")

    def send_mail(self, text, to):
        self.msg = MIMEText(text)
        self.msg['Subject'] = 'title'
        self.s.sendmail("wapp.study@gmail.com", to, self.msg.as_string())
