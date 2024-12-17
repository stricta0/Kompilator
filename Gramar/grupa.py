class GF1234577:
    MOD = 1234577

    def __init__(self, value):
        self.value = value % GF1234577.MOD  # Upewniamy się, że wartość jest w grupie modulo

    def get_value(self):
        return self.value
    def __repr__(self):
        return f"{self.value}"

    # Dodawanie
    def __add__(self, other):
        if isinstance(other, GF1234577):
            return GF1234577((self.value + other.value) % GF1234577.MOD)
        return NotImplemented

    # Odejmowanie
    def __sub__(self, other):
        if isinstance(other, GF1234577):
            return GF1234577((self.value - other.value) % GF1234577.MOD)
        return NotImplemented

    # Mnożenie
    def __mul__(self, other):
        if isinstance(other, GF1234577):
            return GF1234577((self.value * other.value) % GF1234577.MOD)
        return NotImplemented

    # Dzielenie (mnożenie przez odwrotność)
    def __truediv__(self, other):
        if isinstance(other, GF1234577):
            if other == GF1234577(0):
                raise ValueError(f"WE DONT DO DIVISION BY 0!")
            #odwrotność elementu w grupie
            inverse = other.inverse()
            return self * inverse
        return NotImplemented

    # Potęgowanie
    def __pow__(self, power, modulo=None):
        if isinstance(power, GF1234577):
            power = power.value
        if isinstance(power, int):
            return GF1234577(pow(self.value, power, GF1234577.MOD))
        return NotImplemented

    # Odwrotność elementu w grupie
    def inverse(self):
        return GF1234577(self._modinv(self.value, GF1234577.MOD))

    def _modinv(self, a, m):
        # Rozszerzony algorytm Euklidesa
        m0, x0, x1 = m, 0, 1
        if m == 1:
            return 0
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        if x1 < 0:
            x1 += m0
        return x1

    def __eq__(self, other):
        if isinstance(other, GF1234577):
            return self.value == other.value
        return False
