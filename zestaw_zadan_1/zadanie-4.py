def porownaj_daty(data1, data2):
    if data1['rok'] != data2['rok']:
        return data1['rok'] > data2['rok']
    if data1['miesiac'] != data2['miesiac']:
        return data1['miesiac'] > data2['miesiac']
    return data1['dzien'] > data2['dzien']

def sortowanie_dat(lista_dat):
    for i in range(1, len(lista_dat)):
        biezaca_data = lista_dat[i]
        j = i - 1
        while j >= 0 and porownaj_daty(lista_dat[j], biezaca_data):
            lista_dat[j + 1] = lista_dat[j]
            j -= 1
        lista_dat[j + 1] = biezaca_data
    return lista_dat

def main():
    print("Program do sortowania dat")
    while True:
        try:
            liczba_dat = int(input("\nIle dat chcesz wprowadzić? "))
            if liczba_dat > 0:
                break
            print("Proszę podać liczbę większą od 0!")
        except ValueError:
            print("To nie jest poprawna liczba!")

    lista_dat = []
    for i in range(liczba_dat):
        print(f"\nData {i + 1}:")
        while True:
            try:
                dzien = int(input("Dzień (1-31): "))
                if 1 <= dzien <= 31:
                    break
                print("Dzień musi być między 1 a 31!")
            except ValueError:
                print("Proszę podać liczbę!")

        while True:
            try:
                miesiac = int(input("Miesiąc (1-12): "))
                if 1 <= miesiac <= 12:
                    break
                print("Miesiąc musi być między 1 a 12!")
            except ValueError:
                print("Proszę podać liczbę!")

        while True:
            try:
                rok = int(input("Rok: "))
                if rok > 0:
                    break
                print("Rok musi być dodatni!")
            except ValueError:
                print("Proszę podać liczbę!")

        lista_dat.append({'dzien': dzien, 'miesiac': miesiac, 'rok': rok})

    posortowane_daty = sortowanie_dat(lista_dat.copy())

    print("\nPosortowane daty:")
    for data in posortowane_daty:
        print(f"{data['dzien']:02d}-{data['miesiac']:02d}-{data['rok']}")

if __name__ == "__main__":
    main()