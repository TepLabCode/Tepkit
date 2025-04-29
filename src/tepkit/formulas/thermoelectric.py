"""
This module contains the formulas related to **thermoelectric** properties.
"""


def z(s, sigma, kappa):
    R"""
    Get thermoelectric materials :math:`z` value.

    ========== =========== ===========================
    Argument   Unit        Explanation
    ========== =========== ===========================
    **Input**  —           —
    ``s``      V/K         Seebeck Coefficient
    ``sigma``  S/m         Electrical Conductivity
    ``kappa``  W·m⁻¹·K⁻¹   Thermal Conductivity (Total)
    **Output** —           —
    ``z``      1/k         z value
    ========== =========== ===========================

    Formula
    =======
    .. math:: z = \frac {S^2 \sigma} {\kappa}

    """

    return s * s * sigma / kappa


def zt(s, sigma, kappa, t):
    R"""
    Get thermoelectric materials :math:`zT` value (Thermoelectric Materials Figure of merit).

    ========== =========== ========================================
    Argument   Unit        Explanation
    ========== =========== ========================================
    **Input**  —           —
    ``s``      V/K         Seebeck Coefficient
    ``sigma``  S/m         Electrical Conductivity
    ``kappa``  W·m⁻¹·K⁻¹   Thermal Conductivity (Total)
    ``t``      K           Absolute Temperature
    **Output** —           —
    ``zT``     1           Thermoelectric Materials Figure of merit
    ========== =========== ========================================

    Formula
    =======
    .. math:: zT = \frac {S^2 \sigma} {\kappa} \cdot T
    """
    return z(s, sigma, kappa) * t
