from bot.colors import eq, sup

SPELL_GAP = 56
SPELL_X = 763

SPELL_UP_KEYS = ['keypad 1', 'keypad 2']
SPELL_UP_Y = 919
SPELL_UP_COUNT = 2

SPELL_DOWN_KEYS = ['keypad 3', 'keypad 4', 'keypad 5', 'keypad 6']
SPELL_DOWN_Y = 976
SPELL_DOWN_COUNT = 4


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

    if eq((r, g, b), (102, 101, 102), bias=10)\
            or eq((r, g, b), (203, 200, 0), bias=10)\
            or eq((r, g, b), (190, 190, 0), bias=10):
        return 'neutral'
    if eq((r, g, b), (190, 0, 0), bias=10):
        return 'enemy'

