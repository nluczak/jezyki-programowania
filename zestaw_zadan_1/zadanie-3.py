def bezpieczna_pozycja(n, k=2):
    pozycja = 0
    for i in range(2, n + 1):
        pozycja = (pozycja + k) % i
    return pozycja + 1

n = int(input("Podaj liczbę żołnierzy: "))
k = 2
print(f"Bezpieczna pozycja: {bezpieczna_pozycja(n, k)}")