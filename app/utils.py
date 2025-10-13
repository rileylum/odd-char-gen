import random


def roll_dice(num_dice: int, num_sides: int) -> list[int]:
    return [random.randint(1, num_sides) for _ in range(num_dice)]


def random_int(min_val: int, max_val: int) -> int:
    return random.randint(min_val, max_val)


def random_choice(items: list) -> any:
    return random.choice(items)
