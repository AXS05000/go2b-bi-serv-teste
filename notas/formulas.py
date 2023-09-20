from decimal import ROUND_DOWN, Decimal


def truncate_number(number, decimals=0):
    """
    Truncates a number to 'decimals' decimal places without rounding.
    """
    factor = Decimal('10') ** decimals  # Aqui o 10 é convertido para Decimal
    return (number * factor).to_integral_value() / factor
