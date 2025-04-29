high_symmetry_paths_data = {
    # fmt: off
    "Setyawan2010": {
        # Square (tp)
        # ├ A.4. Tetragonal (TET, tP) | Fig.4 | Table 5
        # └ a-right/b-right
        ("tp", "right") : [["G", "A", "D1", "G"]],
        # Rectangular (op)
        # ├ A.6. Orthorhombic (ORC, oP) | Fig.7 | Table 8
        # └ a1 < a2 | a-right/b-right
        ("op", "right") : [["G", "A", "D1", "B", "G"]],
        # Centered rectangular (oc)
        # ├ A.9. C-centered orthorhombic (ORCC, oS) | Fig.12 | Table 12
        # └ a < b | a1 = (a/2, b/2, 0) | a2 = (a/2, b/2, 0) | => a-obtuse/b-acute
        ("oc", "acute") : [["G", "D1", "B", "C2B", "C2", "G"]],
        ("oc", "obtuse"): [["G", "D2", "B", "C1B", "C1", "G"]],
        # Hexagonal (hp)
        # ├ A.10. Hexagonal (HEX, hP) | Fig. 13 | Table 13
        # └ a1 = (a/2, -√3/2 a, 0) | a2 = (a/2, √3/2 a, 0) | => a-obtuse/b-acute
        ("hp", "acute") : [["G", "A", "D1", "G"]],
        ("hp", "obtuse"): [["G", "A", "C1A", "G"]],
        # Oblique (mp)
        # ├ A.12. Monoclinic (MCL, mP) | Fig.16 | Table 16
        # └ α < 90° => a-acute/b-obtuse
        ("mp", "acute") : [["G", "AR", "C2A", "C2", "C2B", "B", "G"]],
        ("mp", "obtuse"): [["G", "A", "C1A", "C1", "C1B", "B", "G"]],
    }
    # fmt: on
}
"""
记录了不同风格的高对称点路径序列。
Setyawan2010 [1]

[1] W. Setyawan and S. Curtarolo, High-throughput electronic band structure calculations: Challenges and tools,
    Comput. Mater. Sci. 49, 299 (2010). https://linkinghub.elsevier.com/retrieve/pii/S0927025610002697
"""

high_symmetry_points_text_data = {
    "Setyawan2010": {
        # Square (tp)
        ("tp", "right"): {
            "G": "Γ",
            "A": "X",
            "D1": "M",
        },
        # Rectangular (op)
        ("op", "right"): {
            "G": "Γ",
            "A": "X",
            "D1": "S",
            "B": "Y",
        },
        # Centered-Rectangular (oc)
        ("oc", "acute"): {
            "G": "Γ",
            "D1": "X",
            "B": "S",
            "C2B": "X1",
            "C2": "Y",
        },
        ("oc", "obtuse"): {
            "G": "Γ",
            "D2": "X",
            "B": "S",
            "C1B": "X1",
            "C1": "Y",
        },
        # Hexagonal (hp)
        ("hp", "acute"): {
            "G": "Γ",
            "A": "M",
            "D1": "K",
        },
        ("hp", "obtuse"): {
            "G": "Γ",
            "A": "M",
            "C1A": "K",
        },
        # Oblique (mp)
        ("mp", "acute"): {
            "G": "Γ",
            "AR": "X",
            "C2A": "H1",
            "C2": "C",
            "C2B": "H",
            "B": "Y",
        },
        ("mp", "obtuse"): {
            "G": "Γ",
            "A": "X",
            "C1A": "H1",
            "C1": "C",
            "C1B": "H",
            "B": "Y",
        },
    }
}
"""
记录了不同风格的高对称点的命名。
"""
