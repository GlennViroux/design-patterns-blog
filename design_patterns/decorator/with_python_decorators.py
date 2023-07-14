from __future__ import annotations
from dataclasses import dataclass, replace
from functools import wraps
from typing import Callable

from design_patterns.decorator.with_decorators import Coffee

SIMPLE_COFFEE = Coffee(name="Simple Coffee", price=1.0, ingredients=["Coffee"], is_vegan=True)


def milk_decorator(func: Callable[[], Coffee]) -> Callable[[], Coffee]:
    @wraps(func)
    def wrapper() -> Coffee:
        coffee = func()
        return replace(coffee, name=f"{coffee.name} + Milk", price=coffee.price + 0.2)

    return wrapper


def vanilla_decorator(func: Callable[[], Coffee]) -> Callable[[], Coffee]:
    @wraps(func)
    def wrapper() -> Coffee:
        coffee = func()
        return replace(coffee, name=f"{coffee.name} + Vanilla", price=coffee.price + 0.3)

    return wrapper


@milk_decorator
def make_coffee_with_milk():
    return SIMPLE_COFFEE


@vanilla_decorator
@milk_decorator
def make_coffee_with_milk_and_vanilla():
    return SIMPLE_COFFEE


if __name__ == "__main__":
    orders = [
        make_coffee_with_milk().order(amount=3),
        make_coffee_with_milk_and_vanilla().order(amount=2),
    ]
    for order in orders:
        print(order)
