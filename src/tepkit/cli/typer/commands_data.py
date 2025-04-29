builtin_groups_data = [
    {
        "group_names": ["c01", "vasp"],
        "group_module": "tepkit.functions.vasp",
        "group_help": "VASP tools.",
        "sub_commands": [
            # Get Data
            {
                "command_names": ["f01", "get-band"],
                "function_name": "get_band",
                "command_panel": "Get Data",
            },
            {
                "command_names": ["f02", "neighbor-distances"],
                "function_name": "get_neighbor_distances",
                "command_panel": "Get Data",
            },
            {
                "command_names": ["f03", "pe"],
                "function_name": "get_piezoelectric_stress_tensors",
                "command_panel": "Get Data",
            },
            # Get Data (2D)
            {
                "command_names": ["f11", "thickness"],
                "function_name": "get_thickness_info",
                "command_panel": "Get Data (2D)",
            },
            {
                "command_names": ["f12", "sym-points"],
                "function_name": "get_high_symmetry_points_2d",
                "command_panel": "Get Data (2D)",
            },
            # Action
            {
                "command_names": ["f21", "supercell"],
                "function_name": "supercell",
                "command_panel": "Action",
            },
            {
                "command_names": ["f22", "get-bz-kpoints"],
                "function_name": "get_bz_kpoints",
                "command_panel": "Action",
            },
            {
                "command_names": ["f90", "stop"],
                "function_name": "stop_vasp",
                "command_panel": "Action",
            },
            {
                "command_names": ["f91", "clear"],
                "function_name": "clear_outputs",
                "command_panel": "Action",
            },
            # Plot
            {
                "command_names": ["f31", "band-contour"],
                "function_name": "band_contour",
                "command_panel": "Plot",
                "kwargs": {"no_args_is_help": True},
            },
            {
                "command_names": ["f32", "plot-kpoints"],
                "function_name": "plot_ibzkpt",
                "command_panel": "Plot",
            },
        ],
    },
    {
        "group_names": ["c02", "phonopy"],
        "group_module": "tepkit.functions.phonopy",
        "group_help": "Phonopy tools.",
        "sub_commands": [
            {
                "command_names": ["rms"],
                "function_name": "rms",
            },
        ],
    },
    {
        "group_names": ["c03", "3ord", "thirdorder"],
        "group_module": "tepkit.functions.thirdorder",
        "group_help": "thirdorder tools.",
        "sub_commands": [
            {
                "command_names": ["f02", "set_jobs"],
                "function_name": "set_jobs_3rd",
                "command_panel": "Tools",
            },
            {
                "command_names": ["f03", "check_dupl"],
                "function_name": "check_duplicate_jobs",
                "command_panel": "Tools",
            },
            {
                "command_names": ["f04", "check"],
                "function_name": "check_jobs",
                "command_panel": "Tools",
            },
            {
                "command_names": ["f11", "adjust_cutoff"],
                "function_name": "adjust_cutoff",
                "command_panel": "Tools",
            },
            {
                "command_names": ["f41", "vasp_sow"],
                "function_name": "vasp_sow_3rd",
                "command_panel": "thirdorder_vasp",
            },
            {
                "command_names": ["f49", "vasp_reap"],
                "function_name": "vasp_reap",
                "command_panel": "thirdorder_vasp",
            },
        ],
    },
    {
        "group_names": ["c04", "4ord", "fourthorder"],
        "group_module": "tepkit.functions.thirdorder",
        "group_help": "fourthorder tools.",
        "sub_commands": [
            {
                "command_names": ["f02", "set_jobs"],
                "function_name": "set_jobs_4th",
                "command_panel": "Tools",
            },
            {
                "command_names": ["f03", "check_dupl"],
                "function_name": "check_duplicate_jobs",
                "command_panel": "Tools",
            },
            {
                "command_names": ["f04", "check"],
                "function_name": "check_jobs",
                "command_panel": "Tools",
            },
            {
                "command_names": ["f11", "adjust_cutoff"],
                "function_name": "adjust_cutoff",
                "command_panel": "Tools",
            },
            {
                "command_names": ["f41", "vasp_sow"],
                "function_name": "vasp_sow_4th",
                "command_panel": "fourthorder_vasp",
            },
        ],
    },
    {
        "group_names": ["c05", "shengbte"],
        "group_module": "tepkit.functions.shengbte",
        "group_help": "ShengBTE tools.",
        "sub_commands": [
            {
                "command_names": ["control"],
                "function_name": "poscar_to_control",
            },
        ],
    },
    {
        "group_names": ["c06", "sym"],
        "group_module": "tepkit.functions.symmetry",
        "group_help": "symmetry tools.",
        "sub_commands": [
            {
                "command_names": ["f01", "layer-group"],
                "function_name": "get_layer_group",
            },
        ],
    },
    {
        "group_names": ["c99", "custom"],
        "group_module": "tepkit.functions.custom",
        "group_help": "Custom functions.",
        "sub_commands": [],
    },
]

builtin_commands_data = [
    {
        "command_names": ["f01", "dp"],
        "function_module": "tepkit.functions.direct",
        "function_name": "dp",
    },
]

# example_groups_data = [
#     {
#         "group_names": ["<short_name>", "<long_name>"],
#         "group_module": "<module_path>",
#         "group_help": "<group_help>",
#         "sub_groups": [{}, {}, ...],
#         "sub_commands": [{}, {}, ...],
#     },
#     {},
#     ...,
# ]

# example_commands_data = [
#     {
#         "command_names": ["<short_name>", "<long_name>"],
#         "function_module": "<module_path>",
#         "function_name": "<function_name>",
#         "kwargs": {},
#     },
#     {},
#     ...,
# ]
