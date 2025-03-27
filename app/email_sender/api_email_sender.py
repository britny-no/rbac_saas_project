import requests
from .email_sender import EmailSender

class APIEmailSender(EmailSender):
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def send(self, recipient: str, subject: str, body: str):
        payload = {
            "to": recipient,
            "subject": subject,
            "body": body,
            "api_key": self.api_key
        }
        response = requests.post(self.api_url, json=payload)
        response.raise_for_status()

        return {"status": "success", "method": "API"}
