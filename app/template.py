from pathlib import Path


def render_template(template_path, variables):
    """
    Load an email template and replace its placeholders
    with values supplied in the variables dictionary.

    Example:
        "Hello {name}" + {"name": "Angelo"}
        becomes:
        "Hello Angelo"
    """

    template_path = Path(template_path)

    # Make sure the requested template actually exists.
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    # Read the template as UTF-8 so normal characters are supported.
    template = template_path.read_text(encoding="utf-8")

    try:
        # Replace placeholders such as {name} and {event}.
        return template.format(**variables)

    except KeyError as error:
        # Give a clearer error if the template references
        # a variable that wasn't supplied.
        missing_variable = error.args[0]
        raise ValueError(
            f"Missing template variable: {missing_variable}"
        ) from error