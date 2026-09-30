from app.template import render_template


def test_render_template(tmp_path):
    """
    Test that template placeholders are replaced
    with the correct variable values.
    """

    # Create a temporary HTML template for the test.
    template_file = tmp_path / "welcome.html"

    template_file.write_text(
        "<h2>Hello {name}!</h2><p>Welcome to {event}.</p>",
        encoding="utf-8"
    )

    # Provide the values that should replace the placeholders.
    variables = {
        "name": "Angelo",
        "event": "GeloCodes"
    }

    # Render the template using the function we're testing.
    result = render_template(template_file, variables)

    # Check that the placeholders were replaced correctly.
    assert "Hello Angelo!" in result
    assert "Welcome to GeloCodes." in result


def test_missing_template_variable(tmp_path):
    """
    Test that a clear error is raised when a template
    requires a variable that wasn't provided.
    """

    # Create a template that requires a name.
    template_file = tmp_path / "welcome.html"

    template_file.write_text(
        "<h2>Hello {name}!</h2>",
        encoding="utf-8"
    )

    # Don't provide the required 'name' variable.
    variables = {}

    # Verify that the function raises the expected error.
    try:
        render_template(template_file, variables)
        assert False, "Expected ValueError was not raised"

    except ValueError as error:
        assert "Missing template variable: name" in str(error)