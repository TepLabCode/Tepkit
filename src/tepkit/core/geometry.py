from dataclasses import dataclass

import numpy as np

from tepkit.utils.typing_tools import Self


@dataclass
class Point2D:
    x: float
    y: float

    def __iter__(self):
        return iter((self.x, self.y))

    def __add__(self, p2: Self) -> Self:
        return Point2D(
            x=self.x + p2.x,
            y=self.y + p2.y,
        )

    def __sub__(self, p2: Self) -> Self:
        return Point2D(
            x=self.x - p2.x,
            y=self.y - p2.y,
        )

    def __pos__(self) -> Self:
        return self

    def __neg__(self) -> Self:
        return Point2D(
            x=-self.x,
            y=-self.y,
        )

    def __truediv__(self, divisor: float) -> Self:
        return Point2D(
            x=self.x / divisor,
            y=self.y / divisor,
        )


@dataclass
class Line2D:
    A: float
    B: float
    C: float

    @property
    def k(self):
        if self.B == 0:
            return float("inf")
        else:
            return -self.A / self.B

    @property
    def a(self):
        return -self.C / self.A

    @property
    def b(self):
        return -self.C / self.B

    @classmethod
    def from_pp(cls, p1: Point2D, p2: Point2D) -> Self:
        return cls(
            A=p2.y - p1.y,
            B=p1.x - p2.x,
            C=p2.x * p1.y - p1.x * p2.y,
        )

    @classmethod
    def from_pk(cls, p: Point2D, k: float) -> Self:
        return cls(
            A=k,
            B=-1,
            C=p.y - k * p.x,
        )


def perpendicular_bisector(p1: Point2D, p2: Point2D) -> Line2D:
    """
    返回两点的中垂线
    """
    if p1.y == p2.y:
        line = Line2D(
            A=1,
            B=0,
            C=-(p1.x + p2.x) / 2,
        )
    else:
        l12 = Line2D.from_pp(p1, p2)
        line = Line2D.from_pk(
            p=(p1 + p2) / 2,
            k=-1 / l12.k,
        )
    return line


def intersection_point(l1: Line2D, l2: Line2D, decimal=15) -> Point2D | None:
    """
    返回两线的交点
    """
    m = l1.A * l2.B - l2.A * l1.B
    if m == 0:
        return None
    else:
        return Point2D(
            x=round((l2.C * l1.B - l1.C * l2.B) / m, decimal),
            y=round((l1.C * l2.A - l2.C * l1.A) / m, decimal),
        )


mid_line = perpendicular_bisector
cross_point = intersection_point


def rotate_matrix_2d(degree, to_3d=False):
    from math import cos, sin, pi

    r = (degree * pi) / 180
    if not to_3d:
        matrix = [
            [cos(r), -sin(r)],
            [sin(r), cos(r)],
        ]
    else:
        matrix = [
            [cos(r), -sin(r), 0],
            [sin(r), cos(r), 0],
            [0, 0, 1],
        ]
    return np.array(matrix).round(15)
