# Python Email Automation Tool

A Python-based email automation tool that reads recipients from a CSV file, generates personalised HTML emails from templates, and sends them through an SMTP server.

The project supports both **live email delivery** and a **dry-run mode** for safely testing the workflow without sending emails.

## Features

* Load recipients from a CSV file
* Personalise emails using template variables
* Generate HTML email content
* Send emails through SMTP
* Secure SMTP connections using STARTTLS
* SMTP authentication using environment variables
* Retry failed email deliveries
* Dry-run mode for safe testing
* Application logging
* Automated tests using pytest
* Clear delivery summary showing successful and failed recipients

## Technologies

* Python 3
* `smtplib`
* `email.message`
* `python-dotenv`
* `pytest`
* SMTP / STARTTLS
* CSV

## Project Structure

```text
06-email-automation-tool/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── email_sender.py
│   ├── template.py
│   ├── recipients.py
│   └── logger.py
│
├── templates/
│   └── welcome.html
│
├── data/
│   └── recipients.csv
│
├── logs/
│
├── tests/
│   ├── __init__.py
│   ├── test_email_sender.py
│   ├── test_recipients.py
│   └── test_template.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## How It Works

The application follows this workflow:

```text
CSV recipients
      │
      ▼
Load recipient data
      │
      ▼
Load HTML template
      │
      ▼
Personalise template
      │
      ▼
Build email message
      │
      ▼
Connect to SMTP server
      │
      ▼
STARTTLS encryption
      │
      ▼
SMTP authentication
      │
      ▼
Send email
      │
      ▼
Log result and display summary
```

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd 06-email-automation-tool
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure SMTP credentials

Create a `.env` file in the project root.

Example:

```text
SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USERNAME=your-smtp-login
SMTP_PASSWORD=your-smtp-key
```

The `.env` file is intentionally excluded from Git using `.gitignore`.

**Never commit SMTP credentials, API keys, passwords, or other secrets to the repository.**

## Recipient Data

Recipients are loaded from:

```text
data/recipients.csv
```

The CSV must contain:

```csv
name,email
Angelo,angelo@example.com
John,john@example.com
Sarah,sarah@example.com
```

## Email Templates

HTML templates are stored in:

```text
templates/
```

Template variables use Python-style placeholders.

For example:

```html
<h2>Hello {name}!</h2>
<p>Welcome to {event}.</p>
```

The application replaces these placeholders with recipient-specific values before sending.

## Running the Application

### Dry-run mode

Dry-run mode prepares the emails without sending them.

```powershell
python -m app.main --dry-run
```

This is useful for safely testing recipient loading, template rendering, and email preparation.

### Live mode

To send emails through the configured SMTP server:

```powershell
python -m app.main
```

The application displays a summary after processing all recipients.

Example:

```text
--------------------------------
Email automation summary
--------------------------------
Total recipients: 3
Successful: 3
Failed: 0
--------------------------------
```

## Retry Handling

The application retries failed email deliveries to handle temporary SMTP failures.

The default retry limit is three attempts.

A custom retry limit can be specified:

```powershell
python -m app.main --retries 5
```

## Testing

The project uses `pytest` for automated testing.

Run the complete test suite with:

```powershell
pytest
```

Current test coverage includes:

* Email message construction
* SMTP connection and STARTTLS usage
* SMTP authentication
* Email sending
* Retry behaviour
* Retry limits
* CSV recipient loading
* HTML template rendering
* Missing template variables

The current test suite contains **8 automated tests**.

## SMTP Testing

The application was tested using a real SMTP service with:

* SMTP server: Brevo
* Port: 587
* Encryption: STARTTLS

A real email was successfully delivered during testing.

The SMTP credentials are stored locally in `.env` and are not included in the repository.

## Security Considerations

The project demonstrates several basic security practices:

* SMTP credentials are stored in environment variables rather than source code.
* `.env` is excluded from version control.
* SMTP communication uses STARTTLS encryption.
* SMTP authentication is required before sending.
* Test recipient data uses non-production example addresses.
* Automated tests mock SMTP connections instead of sending real emails.

For production use, additional controls would be appropriate, such as secure secret management, rate limiting, stronger validation, monitoring, and protection against email abuse.

## What This Project Demonstrates

This project demonstrates practical Python development and automation skills including:

* Python application structure
* File and CSV processing
* HTML templating
* SMTP communication
* TLS-secured network communication
* Environment-based configuration
* Error handling
* Retry mechanisms
* Logging
* Command-line arguments
* Automated testing
* Separation of application components

## Future Improvements

Possible future improvements include:

* Support for multiple email templates
* HTML and plain-text template pairs
* Attachment support
* Email scheduling
* Rate limiting
* More detailed delivery reporting
* Configuration through a dedicated settings file
* Additional input validation
* Structured logging
