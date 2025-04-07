def czy_pierwsza(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def liczby_pierwsze_w_zakresie(zakres_dolny, zakres_gorny):
    liczby_pierwsze = []
    for liczba in range(zakres_dolny, zakres_gorny + 1):
        if czy_pierwsza(liczba):
            liczby_pierwsze.append(liczba)
    return liczby_pierwsze


def main():
    print("Znajdowanie liczb pierwszych w zadanym zakresie")

    while True:
        try:
            zakres_dolny = int(input("Podaj początek zakresu: "))
            zakres_gorny = int(input("Podaj koniec zakresu: "))
            if zakres_dolny > zakres_gorny:
                print("Błąd, początek musi być większy niż koniec")
                continue
            break
        except ValueError:
            print("Błąd, tylko liczby całkowite")

    pierwsze = liczby_pierwsze_w_zakresie(zakres_dolny, zakres_gorny)

    print(f"\nLiczby pierwsze w zakresie {zakres_dolny}-{zakres_gorny}:")
    if not pierwsze:
        print("Brak liczb pierwszych w podanym zakresie")
    else:
        for i in range(0, len(pierwsze), 10):
            print(", ".join(map(str, pierwsze[i:i + 10])))


if __name__ == "__main__":
    main()