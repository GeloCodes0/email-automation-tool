from app.recipients import load_recipients


def test_load_recipients(tmp_path):
    """
    Test that recipients are correctly loaded from a CSV file.
    """

    # Create a temporary CSV file for the test.
    csv_file = tmp_path / "recipients.csv"

    csv_file.write_text(
        "name,email\n"
        "Angelo,angelo@example.com\n"
        "John,john@example.com\n",
        encoding="utf-8"
    )

    # Load the recipients using the function we're testing.
    recipients = load_recipients(csv_file)

    # Verify that both recipients were loaded correctly.
    assert len(recipients) == 2

    assert recipients[0]["name"] == "Angelo"
    assert recipients[0]["email"] == "angelo@example.com"

    assert recipients[1]["name"] == "John"
    assert recipients[1]["email"] == "john@example.com"