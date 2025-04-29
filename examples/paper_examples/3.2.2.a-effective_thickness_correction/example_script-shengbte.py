from tepkit.io.shengbte import KappaTensorVsT
from tepkit.io.vasp import Poscar

# Read Files
poscar = Poscar.from_dir(R".\input-shengbte")
kappal = KappaTensorVsT.from_dir(R".\input-shengbte")
kappal.df.to_csv("kappal_before_etc.csv")
# Effective Thickness Correction
proportion = poscar.thickness_info["effective_thickness_proportion"]
kappal.effective_thickness_correction(proportion=proportion)
kappal.df.to_csv("kappal_after_etc.csv")
