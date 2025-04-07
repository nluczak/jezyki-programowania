def suma_dzielnikow(n):
    if n == 1:
        return 0
    suma = 1
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            suma += i
            drugi_dzielnik = n // i
            if drugi_dzielnik != i:
                suma += drugi_dzielnik
    return suma

def liczby_zaprzyjaznione(zakres_dolny, zakres_gorny):
    znalezione_pary = set()
    for a in range(zakres_dolny, zakres_gorny + 1):
        b = suma_dzielnikow(a)
        if b > a and suma_dzielnikow(b) == a:
            znalezione_pary.add((a, b))
    return znalezione_pary

if __name__ == "__main__":
    zakres_dolny = int(input("Podaj zakres dolny: "))
    zakres_gorny = int(input("Podaj zakres górny: "))

    pary = liczby_zaprzyjaznione(zakres_dolny, zakres_gorny)

    print(f"Liczby zaprzyjaźnione w zakresie {zakres_dolny}-{zakres_gorny}:")
    for para in sorted(pary):
        print(f"{para[0]} i {para[1]}")