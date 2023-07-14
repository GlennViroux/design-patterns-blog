from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from more_itertools import flatten

from design_patterns.chain_of_responsability.chain_of_responsability_coffee import MaximumPriceHandler, VeganHandler
from design_patterns.decorator.with_decorators import VanillaDecorator, MilkDecorator


@dataclass
class Coffee:
    name: str
    price: float
    ingredients: list[str]
    is_vegan: bool


class CoffeeOrderComponentBase(ABC):
    @property
    @abstractmethod
    def total_price(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def all_ingredients(self) -> list[str]:
        raise NotImplementedError

    @property
    @abstractmethod
    def is_vegan(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def order_lines(self) -> list[str]:
        raise NotImplementedError


@dataclass
class CoffeeOrder(CoffeeOrderComponentBase):
    base_coffee: Coffee
    amount: int

    @property
    def total_price(self) -> float:
        return self.amount * self.base_coffee.price

    @property
    def all_ingredients(self) -> list[str]:
        return self.base_coffee.ingredients

    @property
    def is_vegan(self) -> bool:
        return self.base_coffee.is_vegan

    @property
    def order_lines(self) -> list[str]:
        if self.amount == 1:
            return [f"Ordered 1 '{self.base_coffee.name}' for the price of {self.total_price}€"]
        return [
            f"Ordered {self.amount} times a '{self.base_coffee.name}' for the total price of {self.total_price:.2f}€"
        ]


@dataclass
class CompositeCoffeeOrder(CoffeeOrderComponentBase):
    children: list[CoffeeOrderComponentBase] = field(default_factory=list)

    @property
    def total_price(self) -> float:
        return sum(child.total_price for child in self.children)

    @property
    def all_ingredients(self) -> list[str]:
        return list(set(flatten([child.all_ingredients for child in self.children])))

    @property
    def is_vegan(self) -> bool:
        return all(child.is_vegan for child in self.children) or not len(self.children)

    @property
    def order_lines(self) -> list[str]:
        return list(flatten([child.order_lines for child in self.children]))


SIMPLE_COFFEE = Coffee(name="Simple Coffee", price=1.0, ingredients=["Coffee"], is_vegan=True)
CAPPUCCINO = Coffee(name="Cappuccino", price=2.0, ingredients=["Coffee", "Milk"], is_vegan=False)


if __name__ == "__main__":
    handlers = MaximumPriceHandler(VeganHandler())
    coffee_with_milk_and_vanilla = VanillaDecorator(MilkDecorator(SIMPLE_COFFEE)())()

    order = CompositeCoffeeOrder(
        children=[
            CoffeeOrder(amount=2, base_coffee=handlers(CAPPUCCINO)),
            CoffeeOrder(amount=1, base_coffee=handlers(coffee_with_milk_and_vanilla)),
            CompositeCoffeeOrder(
                children=[CoffeeOrder(amount=3, base_coffee=handlers(VanillaDecorator(CAPPUCCINO)()))]
            ),
        ]
    )

    for order_line in order.order_lines:
        print(order_line)

    print("-" * 40)
    print(f"The total price of the order is {order.total_price:.2f}€")
    print(f"These are all the ingredients included in this order: {', '.join(order.all_ingredients)}")
    print(f"This order is {'' if order.is_vegan else 'not'} vegan")