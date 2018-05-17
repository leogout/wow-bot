import pyautogui
import time
from PIL import ImageGrab


def get_rgb_at(x, y):
    img = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))
    return img.getpixel((0, 0))

while 1:
    g = get_rgb_at(1890, 950)[1]
    while g < 180 or g > 230:
        pyautogui.typewrite('-')
        time.sleep(0.5)
        g = get_rgb_at(1890, 950)[1]

    time.sleep(1)
