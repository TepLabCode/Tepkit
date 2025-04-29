from tepkit.io.boltztrap2 import Condtens
from tepkit.io.vasp import Poscar

# Read Files
poscar = Poscar.from_dir(R".\input-boltztrap2")
kappal = Condtens.from_dir(R".\input-boltztrap2")
kappal.df.to_csv("boltztrap2_before_etc.csv")
# Effective Thickness Correction
proportion = poscar.thickness_info["effective_thickness_proportion"]
kappal.effective_thickness_correction(proportion=proportion)
kappal.df.to_csv("boltztrap2_after_etc.csv")
