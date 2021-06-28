from dataclasses import dataclass

import pytest as pytest


@dataclass
class Fruit:
    name: str


@pytest.fixture
def my_fave_fruit():
    return Fruit("banana")


@pytest.fixture
def fruit_basket(my_fave_fruit):
    return [Fruit("apple"), Fruit("pear"), my_fave_fruit]


def test_my_fruit_in_basket(my_fave_fruit, fruit_basket):
    assert my_fave_fruit in fruit_basket

