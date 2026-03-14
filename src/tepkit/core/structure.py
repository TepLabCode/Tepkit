import numpy as np

from tepkit.utils.typing_tools import NumpyArray3x3, NumpyArrayNx3


def abc_to_xyz(
    abc: NumpyArrayNx3[float],
    lattice: NumpyArray3x3[float],
) -> NumpyArrayNx3[float]:
    """
    Convert fractional coordinates to Cartesian coordinates.
    
    [zh-CN]
    将分数坐标转换为笛卡尔坐标。
    
    :param abc: Fractional coordinates.
    :param lattice: Lattice matrix.
    :return: Cartesian coordinates.
    
    Usage
    -----
    >>> xyz = abc_to_xyz(abc, lattice)
    >>> xyz = abc_to_xyz(np.column_stack((a, b, c)), b_lattice)
    >>> x, y, z = abc_to_xyz(abc, lattice).T
    >>> x, y, z = abc_to_xyz(np.column_stack((a, b, c)), b_lattice).T
    
    """
    abc = np.array(abc, dtype=float)
    xyz = np.dot(abc, lattice)
    return xyz


def xyz_to_abc(
    xyz: NumpyArrayNx3[float],
    lattice: NumpyArray3x3[float],
    decimal=15,
) -> NumpyArrayNx3[float]:
    """
    Convert Cartesian coordinates to fractional coordinates.
    
    [zh-CN]
    将笛卡尔坐标转换为分数坐标。
    
    :param xyz: Cartesian coordinates.
    :param lattice: Lattice matrix.
    :param decimal: Rounding precision.
    :return: Fractional coordinates.
    
    Usage
    -----
    >>> abc = xyz_to_abc(xyz, lattice)
    >>> abc = xyz_to_abc(np.column_stack((x, y, z)), lattice)
    >>> a, b, c = xyz_to_abc(xyz, lattice).T
    >>> a, b, c = xyz_to_abc(np.column_stack((x, y, z)), lattice).T
    
    """
    xyz = np.array(xyz, dtype=float)
    lattice_inv = np.linalg.inv(lattice)
    abc = np.dot(xyz, lattice_inv)
    return abc.round(decimal)
