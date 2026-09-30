from unittest.mock import MagicMock, patch

from app.email_sender import build_email, send_email
from app.main import send_with_retry


def test_build_email():
    """
    Test that an email message is built with the
    correct headers and HTML content.
    """

    message = build_email(
        sender="sender@example.com",
        recipient="recipient@example.com",
        subject="Test Subject",
        html_body="<h1>Hello</h1>"
    )

    assert message["From"] == "sender@example.com"
    assert message["To"] == "recipient@example.com"
    assert message["Subject"] == "Test Subject"


@patch("app.email_sender.smtplib.SMTP")
def test_send_email(mock_smtp):
    """
    Test that the email is sent using SMTP with
    STARTTLS encryption and authentication.
    """

    # Create a fake SMTP server.
    mock_server = MagicMock()

    # Make the mocked SMTP connection behave like
    # the real context manager used by send_email().
    mock_smtp.return_value.__enter__.return_value = mock_server

    message = build_email(
        sender="sender@example.com",
        recipient="recipient@example.com",
        subject="Test Subject",
        html_body="<h1>Hello</h1>"
    )

    send_email(
        message=message,
        smtp_host="smtp.example.com",
        smtp_port=587,
        username="username",
        password="password"
    )

    # Confirm that the SMTP server was contacted
    # using the expected host and port.
    mock_smtp.assert_called_once_with(
        "smtp.example.com",
        587
    )

    # Confirm that the connection was upgraded
    # to encrypted TLS.
    mock_server.starttls.assert_called_once()

    # Confirm that authentication occurred.
    mock_server.login.assert_called_once_with(
        "username",
        "password"
    )

    # Confirm that the email was sent.
    mock_server.send_message.assert_called_once_with(
        message
    )


def test_send_with_retry_succeeds_after_failure():
    """
    Test that send_with_retry() retries after a failed
    attempt and succeeds when a later attempt works.
    """

    message = MagicMock()

    with patch(
        "app.main.send_email",
        side_effect=[
            Exception("Temporary SMTP failure"),
            None
        ]
    ) as mock_send:

        result = send_with_retry(
            message=message,
            recipient_email="recipient@example.com",
            smtp_host="smtp.example.com",
            smtp_port=587,
            username="username",
            password="password",
            max_retries=3
        )

    assert result is True
    assert mock_send.call_count == 2


def test_send_with_retry_fails_after_all_attempts():
    """
    Test that send_with_retry() reports failure when
    every retry attempt fails.
    """

    message = MagicMock()

    with patch(
        "app.main.send_email",
        side_effect=Exception("SMTP failure")
    ) as mock_send:

        result = send_with_retry(
            message=message,
            recipient_email="recipient@example.com",
            smtp_host="smtp.example.com",
            smtp_port=587,
            username="username",
            password="password",
            max_retries=3
        )

    assert result is False
    assert mock_send.call_count == 3


def test_send_with_retry_respects_retry_limit():
    """
    Test that send_with_retry() does not exceed the
    configured retry limit.
    """

    message = MagicMock()

    with patch(
        "app.main.send_email",
        side_effect=Exception("SMTP failure")
    ) as mock_send:

        result = send_with_retry(
            message=message,
            recipient_email="recipient@example.com",
            smtp_host="smtp.example.com",
            smtp_port=587,
            username="username",
            password="password",
            max_retries=2
        )

    assert result is False
    assert mock_send.call_count == 2