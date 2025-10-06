from ..repositories import ProductRepository
from ..schemas import CartItemDTO, ProductDTO


class CartService:
    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository
        self._cart_items: list[CartItemDTO] = []

    def add_item(self, product_id: int, quantity: int) -> CartItemDTO:
        """Add a product to the cart."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        product = self._product_repository.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product with id {product_id} not found")

        product_dto = ProductDTO.from_model(product)

        for item in self._cart_items:
            if item.product.product_id == product_id:
                item.quantity += quantity
                return item

        cart_item = CartItemDTO(product=product_dto, quantity=quantity)
        self._cart_items.append(cart_item)
        return cart_item

    def remove_item(self, product_id: int) -> None:
        """Remove a product from the cart."""
        self._cart_items = [
            item for item in self._cart_items
            if item.product.product_id != product_id
        ]

    def update_quantity(self, product_id: int, quantity: int) -> CartItemDTO:
        """Update the quantity of a product in the cart."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        for item in self._cart_items:
            if item.product.product_id == product_id:
                item.quantity = quantity
                return item

        raise ValueError(f"Product with id {product_id} not in cart")

    def get_items(self) -> list[CartItemDTO]:
        """Get all items in the cart."""
        return self._cart_items.copy()

    def get_total(self) -> float:
        """Calculate the total price of all items in the cart."""
        return sum(item.product.price * item.quantity for item in self._cart_items)

    def clear(self) -> None:
        """Clear all items from the cart."""
        self._cart_items.clear()

    def is_empty(self) -> bool:
        """Check if the cart is empty."""
        return len(self._cart_items) == 0
