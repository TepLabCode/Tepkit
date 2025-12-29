# Change Log

## 0.2.1 (2025-10-11)

### CLI Changes

- **Add:** 2 new commands `tepkit vasp check` and `tepkit vasp check-dirs`
- **Remove:** 2 obsolete commands `tepkit thirdorder check` and `tepkit fourthorder check-dirs`
  (now use `tepkit vasp check-dirs` instead)


- **Add:** 1 new command group `tepkit vasp kpoints`
- **Add:** 1 new command `tepkit vasp kpoints auto`
- **Move:** `tepkit vasp f32|plot-kpoints` ➜ `tepkit vasp kpoints plot`


- **Add:** 1 new command group `tepkit vasp poscar`
- **Add:** 1 new command `tepkit vasp poscar volume`
- **Move:** `tepkit vasp f21|supercell` ➜ `tepkit vasp poscar supercell`


- **Add:** 1 new command group `tepkit vasp others`
- **Move:** `tepkit f01|dp` ➜ `tepkit others f01|dp`

### Core Changes

- **Add:** 1 new class `tepkit.io.vasp.RegularKpoints`
- **Add:** 1 new module `tepkit.io.mlip`
  - **Add:** 1 new class `tepkit.io.mlip.MlipCfg`

### Miscellaneous

- Add `logger.raw` as a shortcut for `logger.opt(raw=True)`
- Set the default newline of `StructuredTextFile.to_file()` to `\n` (LF)
