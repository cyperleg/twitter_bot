from typing import Iterable
import numpy as np
import scipy.interpolate as si
from numpy import ndarray
from random import randint


class Automate:
    def __init__(self):
        pass

    @classmethod
    def get_curve_points(cls) -> tuple[ndarray | Iterable, ndarray | Iterable]:
        # Curve base:
        points = list()
        for i in range(randint(0, 10)):
            points.append([randint(0, 10), randint(0, 10)])
        points = np.array(points)

        x = points[:, 0]
        y = points[:, 1]

        t = range(len(points))
        ipl_t = np.linspace(0.0, len(points) - 1, 100)

        x_tup = si.splrep(t, x, k=3)
        y_tup = si.splrep(t, y, k=3)

        x_list = list(x_tup)
        xl = x.tolist()
        x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

        y_list = list(y_tup)
        yl = y.tolist()
        y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

        x_i = si.splev(ipl_t, x_list)  # x interpolate values
        y_i = si.splev(ipl_t, y_list)  # y interpolate values

        return x_i, y_i
