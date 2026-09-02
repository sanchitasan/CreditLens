def format_currency(
    value: float,
) -> str:
    """Format a numeric value as Indian Rupees."""

    return f"₹{value:,.2f}"


def format_currency_integer(
    value: float,
) -> str:
    """Format currency without decimal places."""

    return f"₹{value:,.0f}"


def format_percentage(
    value: float,
) -> str:
    """Format a decimal probability as a percentage."""

    return f"{value * 100:.2f}%"