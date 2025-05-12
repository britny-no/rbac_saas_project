import pytest
from app.email_sender.mock_email_sender import MockEmailSender


class TestSend:
    @pytest.mark.description("이메일 전송 성공")
    def test_success(email_sender):
        # Given
        email_sender = MockEmailSender() 
        recipient = "test@example.com"
        subject = "Test Subject"
        body = "Test Body"

        # When
        result = email_sender.send(recipient, subject, body)

        # Then
        assert result["status"] == "success"
        assert result["method"] == "Mock"
