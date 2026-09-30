import smtplib
from email.message import EmailMessage


def build_email(sender, recipient, subject, html_body):
    """
    Build an email message containing both a plain-text
    version and an HTML version of the email.
    """

    message = EmailMessage()

    # Set the basic email headers.
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject

    # Plain-text fallback for email clients that cannot
    # display HTML.
    message.set_content(
        "This email contains HTML content. "
        "Please use an HTML-compatible email client."
    )

    # HTML version of the email.
    message.add_alternative(html_body, subtype="html")

    return message


def send_email(
    message,
    smtp_host,
    smtp_port,
    username,
    password
):
    """
    Send an email using SMTP with STARTTLS encryption.

    SMTP credentials are supplied to the function rather
    than being stored directly in the source code.
    """

    # Connect to the SMTP server without SSL initially.
    with smtplib.SMTP(smtp_host, smtp_port) as server:

        # Upgrade the connection to encrypted TLS.
        server.starttls()

        # Authenticate with the SMTP server.
        server.login(username, password)

        # Send the prepared email.
        server.send_message(message)