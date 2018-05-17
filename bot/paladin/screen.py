from bot.colors import sup
from bot.screen import spells, target_type

HOLY_POWER_POS = [(98, 88), (134, 88), (170, 88), (124, 98), (154, 98)]


def describe(screen):
    return {
        'holy': holy_power_count(screen),
        'spells': spells(screen),
        'target': target_type(screen),
    }


def holy_power_count(img):
    hp_count = 0
    for hp_pos in HOLY_POWER_POS:
        r, g, b, *a = img.getpixel(hp_pos)
        if sup((r, g, b), (100, 100, 100)):
            hp_count += 1

    return hp_count