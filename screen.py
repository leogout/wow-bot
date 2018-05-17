from utils import *
from PIL import ImageGrab

SPELL_GAP = 56
SPELL_X = 763

SPELL_UP_KEYS = ['keypad 1', 'keypad 2']
SPELL_UP_Y = 919
SPELL_UP_COUNT = 2

SPELL_DOWN_KEYS = ['keypad 3', 'keypad 4', 'keypad 5', 'keypad 6']
SPELL_DOWN_Y = 976
SPELL_DOWN_COUNT = 4

HHP_X = 98
HHP_Y = 50
HHP_LENGTH = 108

EHP_X = 257
EHP_Y = 50
EHP_LENGTH = 108

ECAST_X = 280
ECAST_Y = 128

HOLY_POWER_POS = [(98, 88), (134, 88), (170, 88), (124, 98), (154, 98)]


def get_data():
    screen = ImageGrab.grab()

    return {
        'spells': spells(screen),
        'target': target_type(screen),
        'hhp': hero_hp(screen),
        'ehp': enemy_hp(screen),
        'ecast': enemy_cast(screen),
        'holy': holy_power_count(screen),
        'oor': incorrect_position(screen)
    }


def spells(img):
    status = {}
    for i in range(0, SPELL_UP_COUNT):
        r, g, b, *a = img.getpixel((SPELL_X + i * SPELL_GAP, SPELL_UP_Y))
        status['u{}'.format(i + 1)] = {
            'key': SPELL_UP_KEYS[i],
            'ready': sup((r, g, b), (100, 100, 100))
        }

    for i in range(0, SPELL_DOWN_COUNT):
        r, g, b, *a = img.getpixel((SPELL_X + i * SPELL_GAP, SPELL_DOWN_Y))
        status['d{}'.format(i + 1)] = {
            'key': SPELL_DOWN_KEYS[i],
            'ready': sup((r, g, b), (100, 100, 100))
        }

    return status


def target_type(img):
    r, g, b, *a = img.getpixel((252, 35))
    print(r, g, b)
    if eq((r, g, b), (0, 0, 190), bias=10):
        return 'ally'
    if eq((r, g, b), (0, 190, 0), bias=10):
        return 'pnj'
    if eq((r, g, b), (102, 101, 102), bias=10) or eq((r, g, b), (203, 200, 0), bias=10) or eq((r, g, b), (190, 190, 0), bias=10):
        return 'neutral'
    if eq((r, g, b), (190, 0, 0), bias=10):
        return 'enemy'
    return 'none'


def hero_hp(img):
    green = 0
    for x in range(0, HHP_LENGTH):
        r, g, b, *a = img.getpixel((HHP_X + x, HHP_Y))

        if r < 10 and g > 90 and b < 10:
            green += 1

    return green / HHP_LENGTH * 100


def enemy_hp(img):
    green = 0
    for x in range(0, EHP_LENGTH):
        r, g, b, *a = img.getpixel((EHP_X + x, EHP_Y))

        if r < 10 and g > 90 and b < 10:
            green += 1

    return green / EHP_LENGTH * 100


def enemy_cast(img):
    r, g, b, *a = img.getpixel((ECAST_X, ECAST_Y))

    return eq((r, g, b), (174, 121, 0), bias=5) or is_green(r, g, b)


def holy_power_count(img):
    hp_count = 0
    for hp_pos in HOLY_POWER_POS:
        r, g, b, *a = img.getpixel(hp_pos)
        if sup((r, g, b), (100, 100, 100)):
            hp_count += 1

    return hp_count


def incorrect_position(img):
    def detect_e(x):
        r1, g1, b1, *a1 = img.getpixel((x, 130))
        r2, g2, b2, *a2 = img.getpixel((x, 131))
        r3, g3, b3, *a3 = img.getpixel((x, 134))
        r4, g4, b4, *a4 = img.getpixel((x, 135))
        return is_red(r1, g1, b1) and is_black(r2, g2, b2) and is_red(r3, g3, b3) and is_black(r4, g4, b4)

    out_of_range = detect_e(956) and detect_e(1005) and detect_e(1015)
    cant_attack = detect_e(856) and detect_e(913) and detect_e(1021)
    wrong_direction = detect_e(840) and detect_e(881) and detect_e(961)
    target_not_in_front = detect_e(882) and detect_e(941) and detect_e(972)

    return out_of_range or cant_attack or wrong_direction or target_not_in_front

