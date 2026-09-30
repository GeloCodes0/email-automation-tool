import argparse
import os

from dotenv import load_dotenv

from app.email_sender import build_email, send_email
from app.logger import logger
from app.recipients import load_recipients
from app.template import render_template


# Load environment variables from the .env file.
load_dotenv()


# Get the main project directory.
from pathlib import Path

BASE_DIRECTORY = Path(__file__).resolve().parent.parent

# Define the locations of the recipient CSV and HTML template.
RECIPIENTS_FILE = BASE_DIRECTORY / "data" / "recipients.csv"
TEMPLATE_FILE = BASE_DIRECTORY / "templates" / "welcome.html"


# Number of times the application will attempt to send
# an email before marking it as failed.
MAX_RETRIES = 3


def parse_arguments():
    """
    Parse command-line arguments used to control the application.
    """

    parser = argparse.ArgumentParser(
        description="Python email automation tool."
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build and preview emails without sending them."
    )

    parser.add_argument(
        "--retries",
        type=int,
        default=MAX_RETRIES,
        help=f"Number of send attempts per email (default: {MAX_RETRIES})."
    )

    return parser.parse_args()


def send_with_retry(
    message,
    recipient_email,
    smtp_host,
    smtp_port,
    username,
    password,
    max_retries
):
    """
    Attempt to send an email multiple times if an SMTP error occurs.

    Returns True if the email was successfully sent.

    Returns False if all attempts fail.
    """

    for attempt in range(1, max_retries + 1):

        try:
            # Attempt to send the email.
            send_email(
                message=message,
                smtp_host=smtp_host,
                smtp_port=smtp_port,
                username=username,
                password=password
            )

            # If no exception occurred, the email was sent.
            logger.info(
                "Email sent successfully to %s on attempt %d.",
                recipient_email,
                attempt
            )

            return True

        except Exception as error:

            # Record the failed attempt.
            logger.warning(
                "Attempt %d/%d failed for %s: %s",
                attempt,
                max_retries,
                recipient_email,
                error
            )

            print(
                f"Attempt {attempt}/{max_retries} failed for "
                f"{recipient_email}: {error}"
            )

    # All attempts failed.
    logger.error(
        "All %d attempts failed for %s.",
        max_retries,
        recipient_email
    )

    return False


def main():
    """
    Run the complete email automation workflow.

    The application:
    1. Parses command-line arguments.
    2. Loads SMTP configuration when required.
    3. Loads recipients from the CSV file.
    4. Personalises the HTML template.
    5. Builds each email.
    6. Sends emails with retry handling.
    7. Supports safe dry-run execution.
    8. Displays a delivery summary.
    """

    # Read command-line arguments.
    args = parse_arguments()

    # Prevent invalid retry values.
    if args.retries < 1:
        raise ValueError(
            "The number of retries must be at least 1."
        )

    # Record that the application has started.
    logger.info("Starting email automation.")

    # Display the current execution mode.
    if args.dry_run:

        logger.info("Running in DRY-RUN mode.")

        print(
            "Running in DRY-RUN mode. "
            "No emails will be sent."
        )

    else:

        logger.info("Running in LIVE mode.")

        print(
            "Running in LIVE mode. "
            "Emails will be sent."
        )

    # Load recipient information from the CSV file.
    recipients = load_recipients(RECIPIENTS_FILE)

    logger.info(
        "Loaded %d recipients.",
        len(recipients)
    )

    print(
        f"Loaded {len(recipients)} recipients."
    )

    print()

    # Initialise delivery counters.
    successful = 0
    failed = 0

    # SMTP configuration is only required for live sending.
    if not args.dry_run:

        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(
            os.getenv("SMTP_PORT", "465")
        )
        smtp_username = os.getenv("SMTP_USERNAME")
        smtp_password = os.getenv("SMTP_PASSWORD")

        # Make sure all required SMTP settings exist.
        if not all(
            [
                smtp_host,
                smtp_username,
                smtp_password
            ]
        ):
            raise ValueError(
                "Missing SMTP configuration. "
                "Check your .env file."
            )

    else:

        # Dummy values are used during dry-run mode.
        smtp_host = None
        smtp_port = None
        smtp_username = "automation@example.com"
        smtp_password = None

    # Process each recipient individually.
    for recipient in recipients:

        try:

            # Personalise the HTML template.
            html_body = render_template(
                TEMPLATE_FILE,
                {
                    "name": recipient["name"],
                    "event": "GeloCodes Community Event"
                }
            )

            # Build the email message.
            message = build_email(
                sender=smtp_username,
                recipient=recipient["email"],
                subject="Welcome!",
                html_body=html_body
            )

            # Handle dry-run mode.
            if args.dry_run:

                logger.info(
                    "DRY-RUN: Email prepared for %s.",
                    recipient["email"]
                )

                print(
                    f"[DRY-RUN] Email prepared for "
                    f"{recipient['email']}"
                )

                print(
                    f"Subject: {message['Subject']}"
                )

                print(
                    f"Personalised name: "
                    f"{recipient['name']}"
                )

                print()

                # A successfully prepared email counts as
                # successful in dry-run mode.
                successful += 1

            else:

                # Attempt to send the email with retry handling.
                was_sent = send_with_retry(
                    message=message,
                    recipient_email=recipient["email"],
                    smtp_host=smtp_host,
                    smtp_port=smtp_port,
                    username=smtp_username,
                    password=smtp_password,
                    max_retries=args.retries
                )

                if was_sent:

                    successful += 1

                    print(
                        f"Email sent successfully to "
                        f"{recipient['email']}"
                    )

                    print()

                else:

                    failed += 1

                    print(
                        f"Failed to send email to "
                        f"{recipient['email']} "
                        f"after {args.retries} attempts."
                    )

                    print()

        except Exception as error:

            # Handle unexpected errors such as template or
            # recipient processing problems.
            failed += 1

            logger.error(
                "Failed to process %s: %s",
                recipient["email"],
                error
            )

            print(
                f"Failed to process "
                f"{recipient['email']}: {error}"
            )

            print()

    # Display the final delivery summary.
    print("--------------------------------")
    print("Email automation summary")
    print("--------------------------------")
    print(f"Total recipients: {len(recipients)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print("--------------------------------")

    # Record the final results in the log.
    logger.info(
        "Email automation completed. "
        "Total=%d Successful=%d Failed=%d",
        len(recipients),
        successful,
        failed
    )


# Run the application when this file is executed directly.
if __name__ == "__main__":
    main()