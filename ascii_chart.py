from print_function import get_function_array
import numpy as np
import time

def create_chart(x, y, height=250, x_legend_values=[]):
    curve = get_function_array(x, y, height)
    # el grid perfecto
    biggest = f"{max(y):.2f}"
    smallest = f"{min(y):.2f}"
    legend_width = max(len(biggest), len(smallest))
    curve = curve.astype(f"<U{legend_width}")
    y_axis = np.full(height, "|")
    # n barras verticales
    first_space = " "*legend_width
    y_legend = np.full(height, first_space, dtype=f"<U{legend_width}"); y_legend[0] = y_legend[0][:-len(biggest)] + biggest
    # n objetos en la leyenda de longitud del objeto mas largo
    curve = np.insert(curve, 0, y_axis, axis=1)
    curve = np.insert(curve, 0, y_legend, axis=1)
    # n_filas * (n_columnas + 2) el elemento 0 es el ancho, y el 1 la barra vertical
    x_axis =  [first_space] + ["∟"] + ["-" if curve[-1][i+2]==" " else "|" for i in range(len(curve[-1])-2)]
    x_axis[0] = x_axis[0][:-len(smallest)] + smallest; x_axis[1]="∟"
    curve[-1] = x_axis
    if not x_legend_values:
        start = "↑"+f"{min(x):.2f}"
        end = "↑"+f"{max(x):.2f}"
    else:
        start = "↑"+x_legend_values[0]
        end = "↑"+x_legend_values[1]
    x_legend_width = max(len(start), len(end))
    x_legend = [first_space]+[start]+[" "]*(len(curve[-1])-2)
    x_legend[-x_legend_width] = end
    curve = np.vstack((curve, x_legend)) 
    return "\n".join(["".join(e) for e in curve])

