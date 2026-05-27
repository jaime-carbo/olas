import numpy as np
import time


def get_function_box(x, height=5, extra=""):
    line = [" " for e in x]
    box: np.ndarray = np.array([line for e in range(height)])

    if extra != "":
        middle_row = height // 2
        middle_column = len(x) // 2
        box[middle_row][middle_column - len(extra) // 2: middle_column - len(extra) // 2 + len(extra)] = list(extra)
    return box

def print_function(x, y, height=5, extra=""):
    box = get_function_box(x, height, extra = extra)
    minimum = np.min(y)
    maximum = np.max(y)
    for pos, e in enumerate(y):
        relative_pos = (e - minimum) / (maximum - minimum)
        line_pos = int((1 - relative_pos) * (height - 1))
        box[line_pos][pos] = pick_symbol(pos, x, y)

    return "\n".join(["".join(e) for e in box])

def get_function_array(x, y, height= 5):
    box = get_function_box(x, height)
    minimum = np.min(y)
    maximum = np.max(y)
    for pos, e in enumerate(y):
        relative_pos = (e - minimum) / (maximum - minimum)
        line_pos = int((1 - relative_pos) * (height - 1))
        box[line_pos][pos] = pick_symbol(pos, x, y)
    return box

def pick_symbol(pos, x, y, tolerance=1e-1):
    if pos == 0 or pos == len(x)-1:
        return "-"
    step = x[1] - x[0]
    diff = (y[pos+1] - y[pos-1]) / (2 * step)
    if diff > tolerance:
        return "/"
    elif diff < -tolerance:
        return "\\"
    else:        return "-"


# print('hola')

# x = np.linspace(0, 10, 121)
# print(x)

# print(np.cos(x))

# for i in range(1000):
#     print_function(x, np.sin(np.cos(x + i * 0.1) + x), height=10)
#     time.sleep(0.01)