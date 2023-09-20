from decimal import ROUND_DOWN, Decimal


def truncate_decimal(dec, places):
    factor = Decimal('10') ** places
    truncated = dec * factor
    truncated = int(truncated)  # Aqui removemos as casas decimais
    return truncated / factor
