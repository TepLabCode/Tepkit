"""
This module contains constants for the different types of tensor indices used in Tepkit.
"""

# Order 0
EMPTY_INDEX = ["-"]
# Order 1
VECTOR2D_INDICES = ["x", "y"]
VECTOR3D_INDICES = ["x", "y", "z"]
# Order 2
TENSOR2D_ORDER2_INDICES = ["xx", "xy",
                           "yx", "yy"]  # fmt: skip
TENSOR3D_ORDER2_INDICES = ["xx", "xy", "xz",
                           "yx", "yy", "yz",
                           "zx", "zy", "zz"]  # fmt: skip
# Order 3
TENSOR3D_ORDER3_INDICES = ["xxx", "xxy", "xxz", "xyx", "xyy", "xyz", "xzx", "xzy", "xzz",
                           "yxx", "yxy", "yxz", "yyx", "yyy", "yyz", "yzx", "yzy", "yzz",
                           "zxx", "zxy", "zxz", "zyx", "zyy", "zyz", "zzx", "zzy", "zzz"]  # fmt: skip

# Voigt Notation
VOIGT_NOTATION_2X2 = ["xx", "yy", "xy"]
VOIGT_NOTATION_3X3 = ["xx", "yy", "zz", "yz", "xz", "xy"]

# Aliases
V3D_INDICES = VECTOR3D_INDICES
T3D_INDICES = TENSOR3D_ORDER2_INDICES
