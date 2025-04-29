"""
This module contains the formulas related to **deformation potential** theory.
"""

from numpy import sqrt

# CODAtA Constants (https://docs.scipy.org/doc/scipy/reference/constants.html#references)
from scipy import constants

__all__ = (
    "carrier_mobility_3d_i",
    "carrier_mobility_2d_i",
    "carrier_mobility_2d_v",
    "relaxtion_time",
)

## 基本常数
# 基本电荷 e (1.602176634e-19, 'C', 0.0)
e = constants.value("elementary charge")
# 约化普朗克常数 (1.054571817e-34, 'J s', 0.0)
hbar = constants.value("reduced Planck constant")
# 玻尔兹曼常数 (1.380649e-23, 'J K^-1', 0.0)
k_b = constants.value("Boltzmann constant")
# 圆周率
pi = constants.pi

## 单位换算
eV_to_J = e
# 原子单位制质量换算/电子质量 (9.1093837015e-31, 'kg', 2.8e-40)
m0_to_kg = constants.value("atomic unit of mass")
# SI 前缀单位换算
m_to_cm = 100
s_to_fs = 10**15
GPa_to_Pa = 10**9


def carrier_mobility_3d_i(
    *,
    c_i, e1_i, m_i,
    t, method="dp_3d",
):  # fmt: skip
    R"""
    Get carrier mobility **component** :math:`\mu_i` by deformation potential theory for **bulk** materials.

    ========== =========== =====================
    Argument   Unit        Explanation
    ========== =========== =====================
    **Input**  —           —
    ``c``      GPa         Elastic constants
    ``e1``     eV          Deformation Potential
    ``m``      m_0         Effective Mass
    ``t``      K           Absolute Temperature
    **Output** —           —
    ``mu``     cm²·s⁻¹·V⁻¹ Carrier Mobility
    ========== =========== =====================

    Formula
    =======

    Ref: `Link Deformation Potentials and Mobilities in Non-Polar Crystals | Phys. Rev.
    <https://journals.aps.org/pr/abstract/10.1103/PhysRev.80.72>`_

    **Formula A.39:**

    .. math:: \mu_i = \frac{2 (2\pi)^{1/2} e \hbar^4 C_{ii}}{3 {m_i}^{5/2} (k_\mathrm{B} T)^{3/2} {E_1}_i^2}

    """
    # SI 单位换算 与 指数计算
    factor_c = c_i * GPa_to_Pa
    factor_e1 = (e1_i * eV_to_J) ** -2
    factor_m = (m_i * m0_to_kg) ** -2.5
    # 计算 常数 的贡献部分
    factor = 2 * ((2 * pi) ** 0.5) * e * (hbar**4) / (3 * ((k_b * t) ** 1.5))
    # 计算 载流子迁移率
    mu = factor * factor_c * factor_e1 * factor_m
    # 换算 载流子迁移率 单位
    mu = mu * m_to_cm**2
    return mu


def carrier_mobility_2d_i(
    *,
    c_i, e1_i, m_i,
    c_j, e1_j, m_j,
    t, method="dp_2d",
):  # fmt: skip
    R"""
    Get carrier mobility **component** :math:`\mu_i` by deformation potential theory for **2D** materials.

    ========== =========== =====================
    Argument   Unit        Explanation
    ========== =========== =====================
    **Input**  —           —
    ``c``      N/m         2D Elastic constants
    ``e1``     eV          Deformation Potential
    ``m``      m_0         Effective Mass
    ``t``      K           Absolute Temperature
    **Output** —           —
    ``mu``     cm²·s⁻¹·V⁻¹ Carrier Mobility
    ========== =========== =====================

    Formula
    =======

    Ref: `Mobility anisotropy of two-dimensional semiconductors | Phys. Rev. B
    <https://journals.aps.org/prb/abstract/10.1103/PhysRevB.94.235306>`_

    You can choose from three different methods by ``method`` argument.

    - ``dp_2d`` (See Ref. Formula **33**) (Default)
        The most widely used version of the deformation potential theory for 2D materials.

        .. math::

            \mu_i = \frac
            {e \hbar^3 C^\mathrm{(2D)}_{ii}}
            { (k_{\mathrm{B}} T) (m_i)^{\frac{3}{2}} (m_j)^{\frac{1}{2}} {(E_1)}_i^2} \\

    - ``lang``  (See Ref. Formula **26**) (Recommended)
        The modified version from Haifeng Lang that better accounts for anisotropy.

        .. math::

            \mu_i = \frac {e \hbar^3}
            {
                (k_{\mathrm{B}} T) (m_i)^{\frac{3}{2}} (m_j)^{\frac{1}{2}}
            }
            \cdot F_{\mathrm{ani}} (E_1)
            \cdot F_{\mathrm{ani}} (C^{\mathrm{(2D)}})

    - ``lang_simplified``  (See Ref. Formula **27**)
        The low order approximation of the above formula.

        .. math::

            \mu_i = \frac {e \hbar^3}
            {
                (k_{\mathrm{B}} T) (m_i)^{\frac{3}{2}} (m_j)^{\frac{1}{2}}
            }
            \cdot \left( \frac{9 E_{1i}^2 + 7 E_{1i} E_{1j} + 4 E_{1j}^2} {20} \right)^{-1}
            \cdot \left( \frac{5 C^{\mathrm{(2D)}}_{ii} + 3 C^{\mathrm{(2D)}}_{jj} } {8} \right)

    """
    # 计算 弹性模量 和 形变势 的贡献部分
    method = method.lower()
    if method in ["lang", "l"]:
        average_c = (c_i + c_j) / 2
        delta_c = (c_j - c_i) / 2
        i = 1 / (sqrt(average_c**2 - delta_c**2))
        j = (average_c / delta_c) * (1 / average_c - i)
        factor_c_ii = (i + j - sqrt(i**2 - j**2)) / (j * sqrt(i**2 - j**2))
        average_e1 = (e1_i + e1_j) / 2
        delta_e1 = (e1_j - e1_i) / 2
        a = average_e1**2 + delta_e1**2 / 2
        b = average_e1 * delta_e1
        factor_e1_i_eV = (a + b - sqrt(a**2 - b**2)) / (b * sqrt(a**2 - b**2))
    elif method in ["lang_simplified", "ls"]:
        factor_c_ii = (5 * c_i + 3 * c_j) / 8
        factor_e1_i_eV = 1 / ((9 * e1_i**2 + 7 * e1_i * e1_j + 4 * e1_j**2) / 20)
    elif method in ["dp_2d", "dp2d"]:
        factor_c_ii = c_i
        factor_e1_i_eV = e1_i**-2
    else:
        raise ValueError(f'method "{method}" wrong.')
    # 计算 形变势 的贡献部分
    factor_e1_i = factor_e1_i_eV * eV_to_J**-2
    # 计算 有效质量 的贡献部分
    factor_m_i = 1 / (m_i * sqrt(m_i * m_j) * m0_to_kg**2)
    # 计算 常数 的贡献部分
    factor = (e * (hbar**3)) / (k_b * t)
    # 计算 载流子迁移率
    mu = factor * factor_c_ii * factor_e1_i * factor_m_i
    # 换算 载流子迁移率 单位
    mu = mu * m_to_cm**2
    return mu


def carrier_mobility_2d_v(
    *,
    c_i, e1_i, m_i,
    c_j, e1_j, m_j,
    t, method="dp_2d",
):  # fmt: skip
    R"""
    Get carrier mobility 2D **vector** :math:`(\mu_i, \mu_j)` by deformation potential theory for **2D** materials.
    """
    mu_i = carrier_mobility_2d_i(
        c_i=c_i, e1_i=e1_i, m_i=m_i,
        c_j=c_j, e1_j=e1_j, m_j=m_j,
        t=t, method=method,
    )  # fmt: skip
    mu_j = carrier_mobility_2d_i(
        c_i=c_j, e1_i=e1_j, m_i=m_j,
        c_j=c_i, e1_j=e1_i, m_j=m_i,
        t=t, method=method,
    )  # fmt: skip
    return mu_i, mu_j


def relaxtion_time(mu, m, unit: dict = None):
    R"""
    Get carrier relaxtion time :math:`\tau` by carrier mobility and effective mass.

    ========== =========== =====================
    Argument   Unit        Explanation
    ========== =========== =====================
    **Input**  —           —
    ``mu``     cm²·s⁻¹·V⁻¹ Carrier Mobility
    ``m``      m_0         Effective Mass
    **Output** —           —
    ``tau``    s or fs     Relaxation Time
    ========== =========== =====================

    Formula
    =======
    .. math:: \tau = \mu * m / e

    """
    if unit is None:
        unit = {"tau": "s"}
    if unit["tau"] == "s":
        return (mu / m_to_cm**2) * (m * m0_to_kg) / e
    elif unit["tau"] == "fs":
        return ((mu / m_to_cm**2) * (m * m0_to_kg) / e) * s_to_fs
    else:
        raise ValueError("unit now only support {'tau':'s'} and {'tau':'fs'}.")


if __name__ == "__main__":
    mu = carrier_mobility_2d_i(
        c_i=70, c_j=72, e1_i=8, e1_j=9, m_i=0.15, m_j=0.16, method="dp_2d", t=300
    )
    tau = relaxtion_time(mu=mu, m=0.15, unit={"tau": "fs"})
    print(carrier_mobility_3d_i(c=72, m=0.18, e1=18.4, t=200))
    print(carrier_mobility_3d_i(c=56, m=0.18, e1=21.6, t=200))
    print(carrier_mobility_3d_i(c=72, m=0.18, e1=18.4, t=300))
    print(carrier_mobility_3d_i(c=56, m=0.18, e1=21.6, t=300))
    print(f"mu = {mu} cm²·s⁻¹·V⁻¹")
    print(f"tau = {tau} fs")
