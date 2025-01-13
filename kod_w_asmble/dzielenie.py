def dzielenie(a, b):
    if b == 0:
        return 0

    save_power = 0
    old_b = b


    while True:
        power = 1

        while b < a: #b - a < 0
            b = b + b
            power = power + power
        if b == a:
            return power + save_power
        power = power // 2
        b = b // 2
        save_power += power
        a = a - b
        b = old_b
        if b > a:
            return save_power