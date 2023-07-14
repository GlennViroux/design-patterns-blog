from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Coffee:
    name: str
    price: float
    ingredients: list[str]
    is_vegan: bool

    def order(self, amount: int) -> str:
        if amount == 1:
            return f"Ordered 1 '{self.name}' for the price of {self.price}€"
        return f"Ordered {amount} times a '{self.name}' for the total price of {self.price * amount:.2f}€"


SIMPLE_COFFEE = Coffee(name="Simple Coffee", price=1.0, ingredients=["Coffee"], is_vegan=True)
SIMPLE_COFFEE_WITH_MILK = Coffee(name="Simple Coffee + Milk", price=1.2, ingredients=["Coffee", "Milk"], is_vegan=False)
SIMPLE_COFFEE_WITH_VANILLA = Coffee(name="Simple Coffee + Vanilla", price=1.3, ingredients=["Coffee", "Vanilla"], is_vegan=True)
SIMPLE_COFFEE_WITH_MILK_AND_VANILLA = Coffee(name="Simple Coffee + Milk + Vanilla", price=1.5, ingredients=["Coffee", "Milk", "Vanilla"], is_vegan=False)


if __name__ == "__main__":
    orders = [
        SIMPLE_COFFEE.order(amount=1),
        SIMPLE_COFFEE_WITH_MILK.order(amount=3),
        SIMPLE_COFFEE_WITH_MILK_AND_VANILLA.order(amount=2),
    ]
    for order in orders:
        print(order)
