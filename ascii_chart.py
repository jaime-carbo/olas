from print_function import get_function_array
import numpy as np


def _apply_axes(curve, y, x_legend_values, x=None, cols_per_value=1, bar_cols=None, max_ticks=2, append_x_axis=False, force_min=None):
    height = curve.shape[0]
    y_min = min(y) if force_min is None else force_min
    y_max = max(y)
    biggest = f"{y_max:.2f}"
    smallest = f"{y_min:.2f}"
    legend_width = max(len(biggest), len(smallest))
    curve = curve.astype(f"<U{legend_width}")
    y_axis = np.full(height, "|")
    first_space = " " * legend_width
    y_legend = np.full(height, first_space, dtype=f"<U{legend_width}")
    y_legend[0] = y_legend[0][:-len(biggest)] + biggest
    if force_min is not None:
        y_legend[-1] = y_legend[-1][:-len(smallest)] + smallest
    curve = np.insert(curve, 0, y_axis, axis=1)
    curve = np.insert(curve, 0, y_legend, axis=1)

    n = len(y)
    data_cols = curve.shape[1] - 2

    if cols_per_value == 1:
        x_axis_content = ["-" if curve[-1][i + 2] == " " else "|" for i in range(data_cols)]
    else:
        row = ["-"] * data_cols
        for idx in bar_cols or []:
            if 0 <= idx < data_cols:
                row[idx] = "|"
        x_axis_content = row

    x_axis = [first_space] + ["∟"] + x_axis_content
    if not append_x_axis:
        x_axis[0] = x_axis[0][:-len(smallest)] + smallest
    x_axis[1] = "∟"

    if append_x_axis:
        x_axis_arr = np.array([x_axis], dtype=f"<U{legend_width}")
        curve = np.vstack([curve, x_axis_arr])
    else:
        curve[-1] = x_axis

    if x_legend_values:
        start = "↑" + str(x_legend_values[0])
        end = "↑" + str(x_legend_values[-1])
        mid = "↑" + str(x_legend_values[len(x_legend_values) // 2]) if max_ticks >= 3 and len(x_legend_values) > 2 else None
    elif x is not None:
        start = "↑" + f"{min(x):.2f}"
        end = "↑" + f"{max(x):.2f}"
        mid = "↑" + f"{(min(x) + max(x)) / 2:.2f}" if max_ticks >= 3 else None
    else:
        start = "↑0"
        end = f"↑{n}"
        mid = f"↑{n // 2}" if max_ticks >= 3 else None

    x_legend_width = max(len(start), len(end), len(mid) if mid else 0)
    min_legend_len = max(len(curve[-1]), x_legend_width + 1)
    x_legend = [first_space] + [start] + [" "] * (min_legend_len - 2)
    x_legend[-x_legend_width] = end
    if mid and max_ticks >= 3:
        mid_target = min_legend_len // 2
        x_legend[mid_target] = " " * max(0, x_legend_width - len(mid)) + mid
    pad_width = min_legend_len - len(curve[-1])
    if pad_width > 0:
        curve = np.pad(curve, ((0, 0), (0, pad_width)), constant_values=" ")
    curve = np.vstack((curve, x_legend))
    return "\n".join(["".join(e) for e in curve])


def create_chart(x, y, height=250, x_legend_values=[]):
    curve = get_function_array(x, y, height)
    return _apply_axes(curve, y, x_legend_values, x=x, max_ticks=2)


def create_bar_chart(y, height=10, x_legend_values=[], width=80, title=""):
    y = np.asarray(y, dtype=float)
    n = len(y)
    if n == 0 or height <= 0:
        return ""

    # Cap to most-recent bars that fit within width
    max_val = float(np.max(y)) if n > 0 else 0.0
    biggest = f"{max_val:.2f}" if max_val > 0 else "0.00"
    smallest = "0.00"
    legend_width = max(len(biggest), len(smallest))
    axis_overhead = legend_width + 2
    available = max(3, width - axis_overhead)
    bar_unit = 3
    max_bars = max(1, available // bar_unit + 1)
    if n > max_bars:
        y = y[-max_bars:]
        n = max_bars
        if x_legend_values:
            x_legend_values = x_legend_values[-max_bars:]

    maximum = max(max_val, 1e-9)

    # Total bar cols (2 per bar) + gaps (min 1 each)
    bare_cols = n * 2 + max(0, n - 1)
    if n > 1:
        extra = max(0, available - bare_cols)
        gap = 1 + extra // (n - 1)
    else:
        gap = 0
    total_cols = n * 2 + max(0, (n - 1) * gap)

    grid_width = max(total_cols, available)
    grid = np.full((height + 1, grid_width), " ", dtype="<U2")

    # Compute left-column index of each bar
    bar_cols = [i * (2 + gap) for i in range(n)]

    # Fill bars: baseline = 0, top relative to max; shift down 1 row for label space
    top_rows = (np.clip(1 - y / maximum, 0, 1) * (height - 1)).astype(int)
    for i in range(n):
        col = bar_cols[i]
        top = top_rows[i]
        # Value label directly above the bar cap
        label = f"{y[i]:.0f}"
        label_start = col + (2 - len(label)) // 2
        for j, ch in enumerate(label):
            if 0 <= label_start + j < grid_width:
                grid[top, label_start + j] = ch
        # Cap (row top+1) and body (top+2..height)
        grid[top + 1, col] = "▓"
        grid[top + 1, col + 1] = "▓"
        for r in range(top + 2, height + 1):
            grid[r, col] = "█"
            grid[r, col + 1] = "█"

    # Apply axes to bar grid only (force_min=0 for honest baseline)
    chart = _apply_axes(grid, y, x_legend_values, cols_per_value=2, bar_cols=bar_cols, max_ticks=3, append_x_axis=True, force_min=0.0)

    chart_lines = chart.split("\n")
    chart_width = max(len(line) for line in chart_lines)

    # Title row
    title_row = list(title.ljust(chart_width))

    return "\n".join(["".join(title_row)] + chart_lines)


def create_horizontal_bar_chart(labels, values, width=80, title="", unit="", display=None, subtitle="", maxes=None, label_width=None):
    n = len(labels)
    if n == 0:
        return ""

    if label_width is not None:
        label_field = label_width
    else:
        max_label = max(len(str(l)) for l in labels)
        label_field = max_label + 1
    if maxes is not None:
        denominators = [m if m > 0 else 1 for m in maxes]
    else:
        maximum = max(values) if max(values) > 0 else 1
        denominators = [maximum] * n

    # Layout: "label │ bar value unit"
    # label field = max_label + 1 space, separator "│ ", value field estimated
    if display is not None:
        value_strs = [str(d) for d in display]
    else:
        value_strs = [f"{v:.1f}{unit}" for v in values]
    max_value_len = max(len(v) for v in value_strs)
    sep = "│ "
    value_field = max_value_len + 1
    available_bar = max(1, width - label_field - len(sep) - value_field)

    lines = []
    title_line = title.ljust(width)
    lines.append(title_line)
    if subtitle:
        lines.append(subtitle.ljust(width))
    top_border = " " * label_field + "┌" + "─" * (available_bar + len(sep) - 2 + value_field) + "┐"
    lines.append(top_border)
    for i in range(n):
        label = str(labels[i]).ljust(label_field)
        bar_len = int((values[i] / denominators[i]) * available_bar)
        bar = "█" * bar_len + "░" * (available_bar - bar_len)
        val = value_strs[i].rjust(value_field)
        lines.append(f"{label}{sep}{bar} {val}")
    bottom_border = " " * label_field + "└" + "─" * (available_bar + len(sep) - 2 + value_field) + "┘"
    lines.append(bottom_border)

    return "\n".join(lines)


def create_timeline_chart(entries, width=80, title="", label_width=None):
    n = len(entries)
    if n == 0:
        return ""

    if label_width is not None:
        label_field = label_width
    else:
        max_label = max(len(f"{e['role']} @ {e['company']}") for e in entries)
        label_field = min(max_label + 1, width // 3)

    sep = "│ "
    date_width = max(len(f"{e['start']} - {e['end']}") for e in entries)
    available_bar = max(1, width - label_field - len(sep) - date_width - 1)
    max_years = max(e["years"] for e in entries) if entries else 1

    lines = []
    title_line = title.ljust(width)
    lines.append(title_line)
    top_border = " " * label_field + "┌" + "─" * (available_bar + len(sep) - 2 + date_width) + "┐"
    lines.append(top_border)
    for e in entries:
        label = f"{e['role']} @ {e['company']}"
        if len(label) > label_field - 1:
            label = label[:label_field - 2] + ".."
        label = label.ljust(label_field)
        bar_len = int((e["years"] / max_years) * available_bar)
        bar = "█" * bar_len + "░" * (available_bar - bar_len)
        date_str = f"{e['start']} - {e['end']}".rjust(date_width)
        lines.append(f"{label}{sep}{bar} {date_str}")
    bottom_border = " " * label_field + "└" + "─" * (available_bar + len(sep) - 2 + date_width) + "┘"

    return "\n".join(lines)


def create_tech_grid(entries, width=80, title=""):
    if not entries:
        return ""

    inner = width - 2
    bar = "│"

    lines = []
    if title:
        lines.append(title.ljust(width))

    for i, entry in enumerate(entries):
        header = f"{entry['role']} @ {entry['company']}"
        date = entry.get("date", "")
        header_line = header.ljust(inner - len(date)) + date
        lines.append(f"{bar}{header_line[:inner]}{bar}")
        for cat, techs in entry.get("techs", []):
            text = f"  {cat}: {techs}"
            if len(text) > inner:
                text = text[:inner - 1] + ".."
            lines.append(f"{bar}{text.ljust(inner)}{bar}")
        if i < len(entries) - 1:
            lines.append(f"├{'─' * inner}┤")

    lines.append(f"└{'─' * inner}┘")
    return "\n".join(lines)
