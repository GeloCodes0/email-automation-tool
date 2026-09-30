import csv
from pathlib import Path


def load_recipients(file_path):
    """
    Load recipient information from a CSV file.

    Expected CSV columns:
    name,email
    """

    recipients = []

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Recipient file not found: {file_path}")

    with file_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # Make sure the CSV contains the required columns
        required_columns = {"name", "email"}

        if not required_columns.issubset(reader.fieldnames or set()):
            raise ValueError("CSV must contain 'name' and 'email' columns.")

        for row in reader:
            name = row["name"].strip()
            email = row["email"].strip()

            # Ignore incomplete rows
            if not name or not email:
                continue

            recipients.append({
                "name": name,
                "email": email
            })

    return recipients