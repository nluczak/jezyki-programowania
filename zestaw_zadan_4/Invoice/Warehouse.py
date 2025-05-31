class OutOfStore(Exception):
    pass


class Warehouse:
    def __init__(self):
        self._products = {}

    def add_product(self, name, price, quantity):
        if name in self._products:
            self._products[name]['quantity'] += quantity
        else:
            self._products[name] = {'price': price, 'quantity': quantity}

    def remove_product(self, name, quantity):
        if name not in self._products or self._products[name]['quantity'] < quantity:
            raise OutOfStore(f"Product '{name}' is out of store or insufficient.")
        self._products[name]['quantity'] -= quantity

    def get_product_info(self, name):
        return self._products.get(name, None)

    def get_all_products(self):
        return self._products.copy()

    def list_products(self):
        return list(self.__products.keys())
