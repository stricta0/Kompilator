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
            print(a-b)
            return power + save_power
        power = power // 2
        b = b // 2
        save_power += power
        a = a - b
        b = old_b
        if b > a:
            print(a)
            return save_power

def mod(a, b):
    if a < b:
        return a
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

            return a-b
        power = power // 2
        b = b // 2
        save_power += power
        a = a - b
        b = old_b
        if b > a:
            return a

for i in range(1000):
    for j in range(1, 1000):
        if i % j != mod(i, j):
            print(f"zle i:{i}, j:{j}, i%j:{i%j}, mod(i,j):{mod(i,j)}")
