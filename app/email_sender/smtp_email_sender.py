import smtplib
from email.mime.text import MIMEText
from .email_sender import EmailSender

class SMTPEmailSender(EmailSender):

    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send(self, recipient: str, subject: str, body: str):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.username
        msg["To"] = recipient

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, recipient, msg.as_string())

        return {"status": "success", "method": "SMTP"}
