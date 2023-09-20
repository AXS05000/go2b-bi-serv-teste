from decimal import ROUND_DOWN, Decimal


def truncate_number(number, decimals=0):
    """
    Truncates a number to 'decimals' decimal places without rounding.
    """
    factor = 10.0 ** decimals
    return Decimal(int(number * factor)) / factor