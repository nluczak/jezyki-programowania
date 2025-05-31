from Shop import Shop
from InvoiceRepository import InvoiceRepository
from Warehouse import Warehouse
from Invoice import Invoice
from Warehouse import OutOfStore


def print_invoice(invoice):
    print(f"\n🧾 Faktura nr {invoice.number} dla {invoice.customer}:")
    for name, qty, price in invoice.items:
        print(f"  - {name} x{qty} @ {price} zł")
    print("")


def save_invoice_to_file(invoice):
    filename = f"faktura_{invoice.number}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Faktura nr {invoice.number}\n")
        file.write(f"Klient: {invoice.customer}\n")
        file.write("Pozycje:\n")
        for name, qty, price in invoice.items:
            file.write(f" - {name} x{qty} @ {price} zł\n")
    print(f"📁 Zapisano fakturę do pliku: {filename}\n")


def interactive_add_products(warehouse):
    print("➕ Dodawanie produktów do magazynu (wpisz 'koniec' aby zakończyć)")
    while True:
        name = input("Nazwa produktu: ")
        if name.lower() == "koniec":
            break
        try:
            price = float(input("Cena: "))
            quantity = int(input("Ilość: "))
            warehouse.add_product(name, price, quantity)
        except ValueError:
            print("❗ Błąd: wpisz poprawne dane (liczby).")


def interactive_purchase(shop):
    print("\n🛒 Zakupy (wpisz 'koniec' jako nazwę, by zakończyć)")
    customer = input("Imię klienta: ")
    items = []
    while True:
        name = input("Nazwa produktu: ")
        if name.lower() == "koniec":
            break
        try:
            quantity = int(input("Ilość: "))
            items.append((name, quantity))
        except ValueError:
            print("❗ Błąd: ilość musi być liczbą całkowitą.")
    try:
        invoice = shop.buy(customer=customer, items_list=items)
        print_invoice(invoice)
        save_invoice_to_file(invoice)
    except OutOfStore as e:
        print(f"❌ Zakup nieudany: {e}")


def main():
    repository = InvoiceRepository()
    warehouse = Warehouse()
    shop = Shop(repository=repository, warehouse=warehouse)

    print("=== SYSTEM SKLEPU ===")

    interactive_add_products(warehouse)

    while True:
        interactive_purchase(shop)
        again = input("Czy chcesz zrobić kolejne zakupy? (tak/nie): ").strip().lower()
        if again != "tak":
            break

    print("\n📦 Końcowy stan magazynu:")
    for name in warehouse.list_products():
        info = warehouse.get_product_info(name)
        print(f"{name}: {info['quantity']} szt. @ {info['price']} zł")


if __name__ == "__main__":
    main()
