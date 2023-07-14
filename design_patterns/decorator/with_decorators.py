from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, replace

from design_patterns.constants import NON_VEGAN_INGREDIENTS


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
CAPPUCCINO = Coffee(name="Cappuccino", price=2.0, ingredients=["Coffee", "Milk"], is_vegan=False)


@dataclass
class BaseCoffeeDecorator(ABC):
    coffee: Coffee

    @property
    @abstractmethod
    def extra_cost(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def extra_name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def extra_ingredients(self) -> list[str]:
        raise NotImplementedError

    def __call__(self) -> Coffee:
        name = f"{self.coffee.name} + {self.extra_name}"
        price = self.coffee.price + self.extra_cost
        ingredients = self.coffee.ingredients + self.extra_ingredients
        is_vegan = self.coffee.is_vegan and not any(
            ingredient in NON_VEGAN_INGREDIENTS for ingredient in self.extra_ingredients
        )
        return replace(self.coffee, name=name, price=price, ingredients=ingredients, is_vegan=is_vegan)


class MilkDecorator(BaseCoffeeDecorator):
    extra_name = "Milk"
    extra_cost = 0.2
    extra_ingredients = ["Milk"]


class VanillaDecorator(BaseCoffeeDecorator):
    extra_name = "Vanilla"
    extra_cost = 0.3
    extra_ingredients = ["Vanilla"]


if __name__ == "__main__":
    coffee_with_milk = MilkDecorator(SIMPLE_COFFEE)()
    coffee_with_milk_and_vanilla = VanillaDecorator(MilkDecorator(SIMPLE_COFFEE)())()
    orders = [
        SIMPLE_COFFEE.order(amount=1),
        coffee_with_milk.order(amount=3),
        coffee_with_milk_and_vanilla.order(amount=2),
    ]

    for order in orders:
        print(order)
