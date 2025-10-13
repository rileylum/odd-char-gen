import random


def roll_dice(num_dice: int, num_sides: int) -> list[int]:
    return [random.randint(1, num_sides) for _ in range(num_dice)]


def random_int(min_val: int, max_val: int) -> int:
    return random.randint(min_val, max_val)


def random_choice(items: list) -> any:
    return random.choice(items)


def roll_stat() -> int:
    return random.randint(1, 6) + 7


def calculate_modifier(stat: int) -> int:
    if stat >= 13:
        return 1
    elif stat <= 8:
        return -1
    else:
        return 0


def generate_six_stats() -> dict[str, dict[str, int]]:
    stats = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
    result = {}
    for stat in stats:
        score = roll_stat()
        result[stat] = {
            'score': score,
            'modifier': calculate_modifier(score)
        }
    return result
