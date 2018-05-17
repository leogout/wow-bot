def compare_list(a, b, comp):
    for i in range(0, len(a)):
        if not comp(a[i], b[i]):
            return False

    return True


def eq(a, b, bias=0):
    return compare_list(a, b, lambda x, y: y - bias < x < y + bias)


def inf(a, b):
    return compare_list(a, b, lambda x, y: x < y)


def sup(a, b):
    return compare_list(a, b, lambda x, y: x > y)


def is_red(r, g, b):
    return r > 150 and g < 50 and b < 50


def is_green(r, g, b):
    return r < 50 and g > 150 and b < 50


def is_blue(r, g, b):
    return r < 50 and g < 50 and b > 150


def is_black(r, g, b):
    return r <= g <= b <= 10


def is_white(r, g, b):
    return r >= g >= b >= 230
