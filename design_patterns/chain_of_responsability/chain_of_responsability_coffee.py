from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

from design_patterns.constants import NON_VEGAN_INGREDIENTS
from design_patterns.decorator.with_decorators import Coffee, MilkDecorator, VanillaDecorator


SIMPLE_COFFEE = Coffee(name="Simple Coffee", price=1.0, ingredients=["Coffee"], is_vegan=True)
CAPPUCCINO = Coffee(name="Cappuccino", price=2.0, ingredients=["Coffee", "Milk"], is_vegan=True)
EXPENSIVE_CAPPUCCINO = Coffee(name="Cappuccino", price=12.0, ingredients=["Coffee", "Milk"], is_vegan=False)


@dataclass
class BaseHandler(ABC):
    next_handler: BaseHandler | None = None

    @abstractmethod
    def __call__(self, coffee: Coffee) -> Coffee:
        raise NotImplementedError


@dataclass
class MaximumPriceHandler(BaseHandler):
    def __call__(self, coffee: Coffee) -> Coffee:
        if coffee.price > 10.0:
            raise RuntimeError(f"{coffee.name} costs more than €10?!")

        return coffee if self.next_handler is None else self.next_handler(coffee)


@dataclass
class VeganHandler(BaseHandler):
    def __call__(self, coffee: Coffee) -> Coffee:
        if coffee.is_vegan and any(ingredient in NON_VEGAN_INGREDIENTS for ingredient in coffee.ingredients):
            raise RuntimeError(f"Coffee {coffee.name} is said to be vegan but contains non-vegan ingredients")

        if not coffee.is_vegan and all(ingredient not in NON_VEGAN_INGREDIENTS for ingredient in coffee.ingredients):
            raise RuntimeError(f"Coffee {coffee.name} is not not labelled as vegan when it should be")

        return coffee if self.next_handler is None else self.next_handler(coffee)


if __name__ == "__main__":
    handlers = MaximumPriceHandler(VeganHandler())
    coffee_milk_and_vanilla = handlers(VanillaDecorator(MilkDecorator(SIMPLE_COFFEE)())())
    print(coffee_milk_and_vanilla.order(amount=3))

    try:
        cappuccino = handlers(CAPPUCCINO)
    except RuntimeError as err:
        print(str(err))

    try:
        cappuccino = handlers(EXPENSIVE_CAPPUCCINO)
    except RuntimeError as err:
        print(str(err))
