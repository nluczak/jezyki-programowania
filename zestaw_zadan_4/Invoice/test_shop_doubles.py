import unittest
from unittest.mock import Mock, call
from Shop import Shop
from Invoice import Invoice
from Warehouse import OutOfStore


class DummyInvoiceRepository:
    pass


class StubWarehouse:
    def get_product_info(self, name):
        return {"price": 10, "quantity": 100}

    def remove_product(self, name, qty):
        pass


class FakeInvoiceRepository:
    def __init__(self):
        self._data = []
        self._number = 1

    def get_next_number(self):
        num = self._number
        self._number += 1
        return num

    def add(self, invoice):
        self._data.append(invoice)

    def delete(self, invoice):
        self._data.remove(invoice)

    def find_by_number(self, number):
        return next((i for i in self._data if i.number == number), None)


class SpyWarehouse:
    def __init__(self):
        self.calls = []
        self.products = {"woda": {"price": 3, "quantity": 10}}

    def get_product_info(self, name):
        return self.products[name]

    def remove_product(self, name, qty):
        self.calls.append(("remove", name, qty))
        self.products[name]["quantity"] -= qty

    def add_product(self, name, price, quantity):
        if name in self.products:
            self.products[name]["quantity"] += quantity
        else:
            self.products[name] = {"price": price, "quantity": quantity}

    def add_back(self, name, qty):
        self.calls.append(("add_back", name, qty))
        self.products[name]["quantity"] += qty


class ShopTestDoubles(unittest.TestCase):
    def test_dummy_repository_not_used(self):
        dummy_repo = DummyInvoiceRepository()
        stub_warehouse = StubWarehouse()
        shop = Shop(repository=dummy_repo, warehouse=stub_warehouse)

    def test_stub_returns_static_data(self):
        repo = FakeInvoiceRepository()
        stub_warehouse = StubWarehouse()
        shop = Shop(repository=repo, warehouse=stub_warehouse)

        invoice = shop.buy("Jan", [("kawa", 2)])
        self.assertEqual(len(invoice.items), 1)
        self.assertEqual(invoice.items[0][2], 10)  # cena ze stub-a

    def test_fake_repository_behaves_like_real(self):
        repo = FakeInvoiceRepository()
        warehouse = StubWarehouse()
        shop = Shop(repository=repo, warehouse=warehouse)

        invoice = shop.buy("Anna", [("herbata", 1)])
        found = repo.find_by_number(invoice.number)
        self.assertEqual(found.customer, "Anna")

    def test_spy_records_inventory_operations(self):
        spy_warehouse = SpyWarehouse()
        repo = FakeInvoiceRepository()
        shop = Shop(repository=repo, warehouse=spy_warehouse)

        shop.buy("Jan", [("woda", 3)])
        self.assertIn(("remove", "woda", 3), spy_warehouse.calls)

    def test_mock_verifies_method_calls_and_params(self):
        mock_repo = Mock()
        mock_repo.get_next_number.return_value = 1
        mock_warehouse = Mock()
        mock_warehouse.get_product_info.return_value = {"price": 4.5, "quantity": 10}

        shop = Shop(repository=mock_repo, warehouse=mock_warehouse)
        shop.buy("Zosia", [("sok", 2)])

        mock_repo.add.assert_called_once()
        mock_repo.get_next_number.assert_called_once()
        mock_warehouse.get_product_info.assert_called_with("sok")
        mock_warehouse.remove_product.assert_called_with("sok", 2)


if __name__ == "__main__":
    unittest.main()
