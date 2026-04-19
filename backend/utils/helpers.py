"""
Shared utility functions.
"""


def format_indian_currency(value: float) -> str:
    """Format a number in Indian currency notation (Crores, Lakhs)."""
    if value >= 10_000_000:
        return f"₹ {value / 10_000_000:.2f} Cr"
    elif value >= 100_000:
        return f"₹ {value / 100_000:.2f} Lakhs"
    return f"₹ {value:,.0f}"


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))
