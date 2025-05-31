import unittest
from unittest.mock import Mock
from InvoiceRepository import InvoiceRepository
from Shop import Shop
from Invoice import Invoice
from Warehouse import Warehouse, OutOfStore


class ShopWithWarehouseTests(unittest.TestCase):
    def setUp(self):
        self.repository = InvoiceRepository()
        self.warehouse = Warehouse()
        self.shop = Shop(repository=self.repository, warehouse=self.warehouse)

        self.warehouse.add_product("cukierki", price=2.0, quantity=10)
        self.warehouse.add_product("sok", price=4.5, quantity=5)

    def test_buy_removes_items_from_warehouse(self):
        self.shop.buy(customer="Anna", items_list=[("cukierki", 2)])
        product = self.warehouse.get_product_info("cukierki")
        self.assertEqual(product["quantity"], 8)

    def test_buy_raises_exception_when_out_of_stock(self):
        with self.assertRaises(OutOfStore):
            self.shop.buy(customer="Anna", items_list=[("sok", 10)])

    def test_returning_goods_adds_products_back_to_warehouse(self):
        invoice = self.shop.buy(customer="Anna", items_list=[("sok", 2)])
        self.shop.returning_goods(invoice)
        product = self.warehouse.get_product_info("sok")
        self.assertEqual(product["quantity"], 5)

    def test_partial_return_restores_only_some_products(self):
        invoice = self.shop.buy(customer="Anna", items_list=[("sok", 3)])
        self.shop.partial_return(invoice, [("sok", 1)])
        product = self.warehouse.get_product_info("sok")
        self.assertEqual(product["quantity"], 3)  # 5 - 3 + 1 = 3
        self.assertEqual(invoice.items[0][1], 2)  # pozostało 2 sztuki na fakturze


class ShopTests(unittest.TestCase):
    def test_while_buy_the_repository_add_should_be_called(self):
        spy_repository = Mock(InvoiceRepository)
        warehouse = Mock()
        warehouse.remove_product.return_value = None
        warehouse.get_product_info.return_value = {"price": 2.0, "quantity": 10}
        shop = Shop(repository=spy_repository, warehouse=warehouse)
        shop.buy(customer="Jan", items_list=[("cukierki", 1)])
        spy_repository.add.assert_called_once()

    def test_while_returning_goods_the_repository_returns_false_when_not_find(self):
        stub_repository = Mock(InvoiceRepository)
        warehouse = Mock()
        shop = Shop(repository=stub_repository, warehouse=warehouse)
        stub_repository.find_by_number.return_value = None
        invoice_mock = Mock(spec=Invoice)
        invoice_mock.number = 1
        result = shop.returning_goods(invoice_mock)
        self.assertEqual(result, False)

    def test_while_returning_goods_the_repository_delete_should_be_called_when_find(self):
        spy_repository = Mock(InvoiceRepository)
        warehouse = Mock()
        shop = Shop(repository=spy_repository, warehouse=warehouse)
        invoice = Invoice(1, "Jan", [("cukierki", 1, 2.0)])
        spy_repository.find_by_number.return_value = invoice
        shop.returning_goods(invoice)
        spy_repository.delete.assert_called_once()
