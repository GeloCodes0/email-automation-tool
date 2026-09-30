import logging
from pathlib import Path


# Create the logs directory if it does not already exist.
LOG_DIRECTORY = Path("logs")
LOG_DIRECTORY.mkdir(exist_ok=True)

# Store application activity in an email_automation.log file.
LOG_FILE = LOG_DIRECTORY / "email_automation.log"

# Configure the application logger.
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Create a named logger for the application.
logger = logging.getLogger("email_automation")