def mnozenie(a, b):
    wynik = 0
    while a != 0:
        if a % 2 == 1:
            wynik += b
        b += b
        a = a // 2
    return wynik

#print(mnozenie(-20, -58))
#print(-1//2)
# slowo = "amodda"
# for i in range(len(slowo)-1):
#     suma = ord(slowo[i]) + ord(slowo[i+1])
#     print(suma)

ksiazki = [
    "Władca Pierścieni: Drużyna Pierścienia",
    "Władca Pierścieni: Dwie Wieże",
    "Władca Pierścieni: Powrót Króla",
    "Hobbit, czyli tam i z powrotem",
    "Harry Potter i Kamień Filozoficzny",
    "Harry Potter i Komnata Tajemnic",
    "Harry Potter i Więzień Azkabanu",
    "Harry Potter i Czara Ognia",
    "Harry Potter i Zakon Feniksa",
    "Harry Potter i Książę Półkrwi",
    "Harry Potter i Insygnia Śmierci",
    "Gra o Tron",
    "Starcie Królów",
    "Nawałnica Mieczy",
    "Uczta dla Wron",
    "Taniec ze Smokami",
    "Zbrodnia i kara",
    "Anna Karenina",
    "Mistrz i Małgorzata",
    "Bracia Karamazow",
    "Idiota",
    "Lalka",
    "Quo Vadis",
    "Pan Tadeusz",
    "Chłopi",
    "Krzyżacy",
    "Przedwiośnie",
    "Duma i Uprzedzenie",
    "Emma",
    "Wichrowe Wzgórza"
]

ksiazki.sort()
for i in range(len(ksiazki)):
    print(f"{i} : {ksiazki[i]}")