from pathlib import Path

from tepkit.io.vasp.outcar import Outcar


def get_piezoelectric_stress_tensors(
    outcar: Path = "./OUTCAR",
    cell_z: float = None,
    only_xy: bool = False,
):
    """
    Get piezoelectric stress tensors from OUTCAR.

    :typer only_xy flag: --only-xy
    """
    from rich import print
    from rich.rule import Rule

    outcar = Outcar.from_file(outcar)
    result = outcar.get_piezoelectric_stress_tensors(cell_z=cell_z, only_xy=only_xy)
    unit = result["unit"]
    # logger.log(
    #     "NOTE",
    #     "The components will be output in Viogt notation order, which is different from OUTCAR.",
    # )
    print(Rule("Piezoelectric Stress Coefficient e^i_j"))
    print(Rule("Electronic Contribution", characters="-"))
    print(result["electronic"].to_string())
    print(Rule("Ionic Contribution", characters="-"))
    print(result["ionic"].to_string())
    print(Rule("Total (Electronic + Ionic)", characters="-"))
    print(result["total"].to_string())
    print(Rule(f"Unit ({unit})"))
    # logger.log("DONE", "Finfish!")


if __name__ == "__main__":
    pass
