from .email_sender import EmailSender

class MockEmailSender(EmailSender):

    def send(self, recipient: str, subject: str, body: str):
        print(f"[MOCK] 이메일 전송: To={recipient}, Subject={subject}, Body={body}")
        return {"status": "success", "method": "Mock"}
