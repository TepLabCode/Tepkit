from typing import Annotated, Literal

from loguru import logger
from rich.panel import Panel
from tepkit.io import StructuredTextFile
from tepkit.core.vasp import VaspState


class Outcar(StructuredTextFile):
    default_file_name = "OUTCAR"

    @property
    def fermi_energy(self, key_text="E-fermi") -> float:
        for line_number, line in enumerate(self.lines, start=1):
            if key_text in line:
                logger.info('Find "E-fermi" line:')
                text = f"{line_number} |" + line.replace("\n", "")
                print(Panel(text))
                e_fermi = float(line.split()[2])
                break
        else:
            raise Exception("Tepkit can not find the Fermi energy in OUTCAR.")
        logger.info(f"Get Fermi energy: E_F = {e_fermi} eV")
        return e_fermi

    def job_state(self) -> VaspState:
        if "Total CPU time used" in self.content:
            return VaspState.Finished
        else:
            return VaspState.Uncompleted

    def get_piezoelectric_stress_tensors(
        self,
        cell_z: Annotated[float, Literal["Ang"]] | None = None,
        only_xy: bool = False,
    ) -> dict:
        import pandas as pd

        result = dict()
        result["only_xy"] = only_xy
        # Unit
        if cell_z is not None:
            result["unit"] = "10^-10 C/m"
        else:
            result["unit"] = "C/m^2"
        # Piezoelectric Stress Coefficient
        voigt_notation = ["xx", "yy", "zz", "yz", "zx", "xy"]
        for index, line in enumerate(self.lines):
            if (
                "PIEZOELECTRIC TENSOR" in line
                and "for field" in line
                and "C/m^2" in line
            ):
                df = pd.DataFrame(
                    [line.split() for line in self.lines[index + 3 : index + 6]],
                    columns=[None, "xx", "yy", "zz", "xy", "yz", "zx"],
                )
                df.set_index(None, inplace=True)
                df = df.astype(float)
                df = df.reindex(columns=voigt_notation)
                df.columns.names = ["\\"]
                if cell_z:
                    df *= cell_z
                if only_xy:
                    df = df.loc[:, ["xx", "yy", "xy"]]
                if "IONIC" in line:
                    result["ionic"] = df
                else:
                    result["electronic"] = df
                if "ionic" in result and "electronic" in result:
                    result["total"] = result["ionic"] + result["electronic"]
                    break
        else:
            logger.warning("Not enough piezoelectric information found in OUTCAR.")
        return result


if __name__ == "__main__":
    pass
