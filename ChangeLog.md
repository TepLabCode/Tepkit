# Change Log

## 0.2.1 (2025-10-11)

### CLI Changes

- **Add:** 2 new commands `tepkit vasp check` and `tepkit vasp check-dirs`
- **Remove:** 2 obsolete commands `tepkit thirdorder check` and `tepkit fourthorder check-dirs`
  (now use `tepkit vasp check-dirs` instead)


- **Add:** 1 new command group `tepkit vasp kpoints`
- **Add:** 1 new command `tepkit vasp kpoints auto`
- **Move:** `tepkit vasp f32|plot-kpoints` ➜ `tepkit vasp kpoints plot`


- **Add:** 1 new command group `tepkit vasp others`
- **Move:** `tepkit f01|dp` ➜ `tepkit others f01|dp`

### Miscellaneous

- Add `logger.raw` as a shortcut for `logger.opt(raw=True)`
- Add a new class `RegularKpoints`
