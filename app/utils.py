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


def generate_equipment(character_class: str) -> dict:
    if character_class == 'Fighter':
        armor = random_choice(['Chainmail', 'Plate'])
        weapon1_options = ['Longsword + Shield', 'Mace + Shield', 'Halberd', 'Two-handed Sword']
        weapon1 = random_choice(weapon1_options)

        if armor == 'Plate' or (armor == 'Chainmail' and 'Shield' in weapon1):
            defend = 'Armored'
        else:
            defend = 'Heavy'

        if weapon1 in ['Longsword + Shield', 'Mace + Shield']:
            attack1 = 'Heavy'
        else:
            attack1 = 'Armored'

        weapon2_options = ['Shortbow', 'Longbow', 'Crossbow']
        weapon2 = random_choice(weapon2_options)

        if weapon2 == 'Shortbow':
            attack2 = 'Light'
        elif weapon2 == 'Longbow':
            attack2 = 'Heavy'
        else:
            attack2 = 'Armored'

        return {
            'armor': armor,
            'weapon1': weapon1,
            'weapon2': weapon2,
            'attack1': attack1,
            'defend': defend,
            'attack2': attack2
        }

    elif character_class == 'Thief':
        armor = 'Leather'
        weapon1_options = ['Dagger + Buckler', '2 Daggers', 'Shortsword', 'Shortsword + Buckler']
        weapon1 = random_choice(weapon1_options)

        if 'Buckler' in weapon1:
            defend = 'Heavy'
        else:
            defend = 'Light'

        if 'Dagger' in weapon1:
            attack1 = 'Light'
        else:
            attack1 = 'Heavy'

        weapon2_options = ['Shortbow', 'Sling']
        weapon2 = random_choice(weapon2_options)
        attack2 = 'Light'

        return {
            'armor': armor,
            'weapon1': weapon1,
            'weapon2': weapon2,
            'attack1': attack1,
            'defend': defend,
            'attack2': attack2
        }

    else:
        armor = None
        weapon1 = random_choice(['Dagger', 'Staff'])
        attack1 = 'Light'

        return {
            'armor': armor,
            'weapon1': weapon1,
            'weapon2': None,
            'attack1': attack1,
            'defend': 'Light',
            'attack2': None
        }
