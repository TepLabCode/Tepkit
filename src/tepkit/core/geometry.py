"""
Provide simple 2D geometry helpers.

[zh-CN]
提供简单的二维几何辅助工具。
"""

from dataclasses import dataclass

import numpy as np

from tepkit.utils.typing_tools import Self


@dataclass
class Point2D:
    """
    Represent a point on a 2D plane.
    
    [zh-CN]
    表示二维平面中的一个点。
    
    """

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
    """
    Represent a line in ``Ax + By + C = 0`` form.
    
    [zh-CN]
    使用隐式方程 ``Ax + By + C = 0`` 表示一条直线。
    
    """

    A: float
    B: float
    C: float

    @property
    def k(self):
        if self.B == 0:
            return float("inf")
        return -self.A / self.B

    @property
    def a(self):
        return -self.C / self.A

    @property
    def b(self):
        return -self.C / self.B

    @classmethod
    def from_pp(cls, p1: Point2D, p2: Point2D) -> Self:
        """
        Build a line through two points.
        
        [zh-CN]
        由两个点构造一条直线。
        
        :param p1: Start point.
        :param p2: End point.
        :return: Line through both points.
        
        """
        return cls(
            A=p2.y - p1.y,
            B=p1.x - p2.x,
            C=p2.x * p1.y - p1.x * p2.y,
        )

    @classmethod
    def from_pk(cls, p: Point2D, k: float) -> Self:
        """
        Build a line from a point and slope.
        
        [zh-CN]
        由一个点和斜率构造一条直线。
        
        :param p: Point on the line.
        :param k: Line slope.
        :return: Line in point-slope form.
        
        """
        return cls(
            A=k,
            B=-1,
            C=p.y - k * p.x,
        )


def perpendicular_bisector(p1: Point2D, p2: Point2D) -> Line2D:
    """
    Return the perpendicular bisector of a segment.
    
    [zh-CN]
    返回两点连线的中垂线。
    
    :param p1: First endpoint.
    :param p2: Second endpoint.
    :return: Perpendicular bisector of ``p1`` and ``p2``.
    
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
    Return the intersection of two lines.
    
    [zh-CN]
    返回两条直线的交点。
    
    :param l1: First line.
    :param l2: Second line.
    :param decimal: Rounding precision.
    :return: Intersection point, or ``None`` if parallel.
    
    """
    m = l1.A * l2.B - l2.A * l1.B
    if m == 0:
        return None
    return Point2D(
        x=round((l2.C * l1.B - l1.C * l2.B) / m, decimal),
        y=round((l1.C * l2.A - l2.C * l1.A) / m, decimal),
    )


mid_line = perpendicular_bisector
cross_point = intersection_point


def rotate_matrix_2d(degree, to_3d=False):
    """
    Return a 2D rotation matrix.
    
    [zh-CN]
    返回二维旋转矩阵。
    
    :param degree: Rotation angle in degrees.
    :param to_3d: Expand to ``3 x 3`` when ``True``.
    :return: Rounded rotation matrix.
    
    """
    from math import cos, pi, sin

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
