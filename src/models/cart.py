from .product import Product


class ShoppingCart:
    def __init__(self):
        self.items: list[CartItem] = []

    def add_item(self, product: Product, quantity: int):
        self.items.append(CartItem(product, quantity))


class CartItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
