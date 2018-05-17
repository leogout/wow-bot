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
        'holy': holy_power_count(screen),
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

    if eq((r, g, b), (190, 0, 0), bias=10):
        return 'enemy'


def holy_power_count(img):
    hp_count = 0
    for hp_pos in HOLY_POWER_POS:
        r, g, b, *a = img.getpixel(hp_pos)
        if sup((r, g, b), (100, 100, 100)):
            hp_count += 1

    return hp_count
