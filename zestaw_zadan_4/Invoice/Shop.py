from abc import ABC
from Invoice import Invoice
from Warehouse import Warehouse, OutOfStore

class Shop(ABC):
    def __init__(self, repository=None, warehouse=None):
        self.__invoice_repository = repository
        self.__warehouse = warehouse

    def buy(self, customer, items_list):
        """
        items_list: list of tuples (product_name, quantity)
        """
        for name, qty in items_list:
            self.__warehouse.remove_product(name, qty)

        invoice_items = []
        for name, qty in items_list:
            product_info = self.__warehouse.get_product_info(name)
            price = product_info['price']
            invoice_items.append((name, qty, price))

        invoice = Invoice(
            number=self.invoice_repository.get_next_number(),
            customer=customer,
            items=invoice_items
        )
        self.invoice_repository.add(invoice)
        return invoice

    def returning_goods(self, invoice):
        if self.invoice_repository.find_by_number(invoice.number):
            self.invoice_repository.delete(invoice)
            for name, qty, _ in invoice.items:
                self.__warehouse.add_product(name, 0, qty)
            return True
        return False

    def partial_return(self, invoice, returned_items):
        """
        returned_items: list of tuples (product_name, quantity)
        """
        if not self.invoice_repository.find_by_number(invoice.number):
            return False

        new_items = []
        for name, qty, price in invoice.items:
            returned_qty = next((r_qty for r_name, r_qty in returned_items if r_name == name), 0)
            actual_qty = qty - returned_qty
            if actual_qty > 0:
                new_items.append((name, actual_qty, price))
            if returned_qty > 0:
                self.__warehouse.add_product(name, price, returned_qty)

        invoice.items = new_items
        self.invoice_repository.update(invoice)
        return True

    @property
    def invoice_repository(self):
        return self.__invoice_repository
