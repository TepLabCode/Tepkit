import tomllib
from io import StringIO
from pathlib import Path

import pandas as pd
from tepkit.cli import logger
from tepkit.formulas.dp import (
    carrier_mobility_2d_v,
    carrier_mobility_3d_i,
    relaxtion_time,
)
from tepkit.io.output import save_df
from tepkit.utils.rich_tools import print_panel

CONFIG_TEMPLATE = """
[input]
dimension   = -1    # 2 or 3
temperature = 300   # Unit: K

[input.2D]
data = \"\"\"
Direction  Carrier  E_1       C_2D      m_eff
x          e        NaN       NaN       NaN
x          h        NaN       NaN       NaN
y          e        NaN       NaN       NaN
y          h        NaN       NaN       NaN
\"\"\"  # Unit:        eV        N/m       m_0

method = "lang"  # "lang" / "lang_simplified" / "dp_2d"

[input.3D]
data = \"\"\"
Direction  Carrier  E_1       C_3D      m_eff
x          e        NaN       NaN       NaN
x          h        NaN       NaN       NaN
y          e        NaN       NaN       NaN
y          h        NaN       NaN       NaN
z          e        NaN       NaN       NaN
z          h        NaN       NaN       NaN
\"\"\"  # Unit:        eV        GPa       m_0

method = "dp_3d" # "dp_3d"

"""


def dp(
    config: Path = "tepkit.dp.in.toml",
    init_config: bool = False,
    save: bool = False,
    to: Path = "tepkit.dp.out.csv",
    t: float = None,
):
    """
    Calculate carrier mobility and relaxation time using DP method.

    :param save: Save the results to a file.
    :param to: The output file path.
    :param config: The input file path.
    :param init_config: Create a template input file.
    :param t: Override the temperature (K) in the input file.
    :typer config      flag: --in
    :typer save        flag: --save
    :typer init_config flag: --init
    :typer t           flag: -t
    """
    # Create config template file
    if init_config:
        with open(config, "w") as f:
            f.write(CONFIG_TEMPLATE)
        logger.opt(colors=True).info(f"Config file created: <blue>`{config}`</>.")
        return
    # Load config file
    if not Path(config).exists():
        print_panel(
            f"Input file [blue]`{config}`[/blue] not found.\n"
            f"You can run [bright_cyan]`tepkit dp --init`[/bright_cyan] to get a input file template.",
            preset="error",
        )
        quit()
    logger.c.info(f"Loading config file: <blue>`{config}`</>...")
    with open(config, "rb") as f:
        dp_dict = tomllib.load(f)
    # Parse input data
    match dp_dict["input"]["dimension"]:
        case 2:
            data = dp_dict["input"]["2D"]["data"]
        case 3:
            data = dp_dict["input"]["3D"]["data"]
        case _:
            print_panel(
                f"The value of [bright_cyan]`dimension`[/bright_cyan] in the [blue]`{config}`[/blue] "
                f"must be [bright_cyan]2[/bright_cyan] or [bright_cyan]3[/bright_cyan].",
                preset="error",
            )
            quit()
    df = pd.read_csv(
        StringIO(data),
        sep=r"\s+",
        index_col=[0, 1],
        header=0,
        dtype={
            "E_1": float,
            "C_2D": float,
            "m_eff": float,
        },
    )
    logger.info(f"Parsed input data:")
    print(df.reset_index().to_string(index=False))
    logger.info(f"Calculating the results...")
    df["mu"] = None
    df["tau"] = None
    t = t or dp_dict["input"]["temperature"]
    match dp_dict["input"]["dimension"]:
        case 2:
            df_x, df_y = df.loc["x"], df.loc["y"]
            method = dp_dict["input"]["2D"]["method"]
            mu_x, mu_y = carrier_mobility_2d_v(
                c_i=df_x["C_2D"],
                c_j=df_y["C_2D"],
                e1_i=df_x["E_1"],
                e1_j=df_y["E_1"],
                m_i=df_x["m_eff"],
                m_j=df_y["m_eff"],
                t=t,
                method=method,
            )
            for carrier in ["e", "h"]:
                df.loc[("x", carrier), "mu"] = mu_x[carrier]
                df.loc[("y", carrier), "mu"] = mu_y[carrier]
        case 3:
            method = dp_dict["input"]["3D"]["method"]
            df["mu"] = carrier_mobility_3d_i(
                c_i=df["C_3D"],
                e1_i=df["E_1"],
                m_i=df["m_eff"],
                t=t,
                method=method,
            )
        case _:
            raise ValueError("Invalid dimension.")
    df["tau"] = relaxtion_time(mu=df["mu"], m=df["m_eff"], unit={"tau": "fs"})
    logger.info(f"Results:")
    print(f"Temperature: {t} K")
    print(f"Method     : {method}")
    print(f"Units      : [mu (cm²·s⁻¹·V⁻¹)][tau (fs)]")
    print(df.reset_index().to_string(index=False))

    if save:
        logger.info(f"Saving the results...")
        save_name = to.stem + "." + method + "." + str(t) + "K" + to.suffix
        save_path = to.with_name(save_name)
        save_df(df, save_path)
        logger.c.info(f"Results saved to: <blue>`{save_path.name}`</>.")
