from unittest.mock import right


def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero is not allowed.")

    quotient = 0
    power = 1
    original_b = b
    copy_b = b

    # Podwajamy b i power aż b > a
    while b < a:
        b = b + b  # Mnożenie przez 2 za pomocą dodawania
        power = power + power  # Mnożenie przez 2 za pomocą dodawania

    if b == a:
        return power

    while b > a:
        b = b - original_b
        power = power - 1


    return power


# Przykład użycia
print(divide(45, 5))
