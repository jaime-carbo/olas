from print_function import get_function_array
import numpy as np


def _apply_axes(curve, y, x_legend_values, x=None):
    height = curve.shape[0]
    biggest = f"{max(y):.2f}"
    smallest = f"{min(y):.2f}"
    legend_width = max(len(biggest), len(smallest))
    curve = curve.astype(f"<U{legend_width}")
    y_axis = np.full(height, "|")
    first_space = " " * legend_width
    y_legend = np.full(height, first_space, dtype=f"<U{legend_width}")
    y_legend[0] = y_legend[0][:-len(biggest)] + biggest
    curve = np.insert(curve, 0, y_axis, axis=1)
    curve = np.insert(curve, 0, y_legend, axis=1)
    x_axis = [first_space] + ["∟"] + ["-" if curve[-1][i + 2] == " " else "|" for i in range(len(curve[-1]) - 2)]
    x_axis[0] = x_axis[0][:-len(smallest)] + smallest
    x_axis[1] = "∟"
    curve[-1] = x_axis
    if not x_legend_values:
        if x is not None:
            start = "↑" + f"{min(x):.2f}"
            end = "↑" + f"{max(x):.2f}"
        else:
            start = "↑0"
            end = f"↑{len(y)}"
    else:
        start = "↑" + x_legend_values[0]
        end = "↑" + x_legend_values[1]
    x_legend_width = max(len(start), len(end))
    min_legend_len = max(len(curve[-1]), x_legend_width + 1)
    x_legend = [first_space] + [start] + [" "] * (min_legend_len - 2)
    x_legend[-x_legend_width] = end
    pad_width = min_legend_len - len(curve[-1])
    if pad_width > 0:
        curve = np.pad(curve, ((0, 0), (0, pad_width)), constant_values=" ")
    curve = np.vstack((curve, x_legend))
    return "\n".join(["".join(e) for e in curve])


def create_chart(x, y, height=250, x_legend_values=[]):
    curve = get_function_array(x, y, height)
    return _apply_axes(curve, y, x_legend_values, x=x)


def create_bar_chart(y, height=10, x_legend_values=[]):
    y = np.asarray(y, dtype=float)
    n = len(y)
    if n == 0 or height <= 0:
        return ""
    width = n * 2 + max(0, n - 1)
    grid = np.full((height, width), " ", dtype="<U1")
    minimum = np.min(y)
    maximum = np.max(y)
    if maximum == minimum:
        top_rows = np.zeros(n, dtype=int)
    else:
        relative = (y - minimum) / (maximum - minimum)
        top_rows = (np.clip(1 - relative, 0, 1) * (height - 1)).astype(int)
    for i in range(n):
        col = i * 3
        top = top_rows[i]
        grid[top, col] = "░"
        grid[top, col + 1] = "░"
        for r in range(top + 1, height):
            grid[r, col] = "▓"
            grid[r, col + 1] = "▓"
    return _apply_axes(grid, y, x_legend_values)
