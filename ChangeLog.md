# Change Log

## 0.2.2 (2026-04-17)

### CLI Changes

- **Update:** Add 1 new option `--list/-l` into `vasp check-dirs` command to activate list mode.

### Core Changes

- None

### Bug Fixes

- **Fixed:** Option `--group/-g` not working in `vasp check-dirs` command.
- **Fixed:** Different behavior of `*` on windows and linux caused by `windows_expand_args`.
- **Fixed:** Incorrect auto name when saving CSV file in `tepkit.functions.phonopy.rms.rms()`.  
  (now `tepkit.RMS_of_3rdIFCs.csv` -> `tepkit.RMS_of_2ndIFCs.csv`)
- **Fixed:** Support `lib64` in `Fourthorder_tools/setup.py` file.
- 
### Miscellaneous

- Add the `__main__.py` file to enable `python -m tepkit` entry.
- Update document.

---

## 0.2.1 (2025-12-29)

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
