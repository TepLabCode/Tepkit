# Adjust cutoff radius

First, you need to create two folder created under different cutoff radius, like:

```
cutoff-a-completed
├── job-001
│   ├── INCAR
│   ├── KPOINTS
│   ├── POSCAR
│   ├── POTCAR
│   ├── ...
│   ├── OUTCAR
│   └── vasprun.xml
├── job-002
├── job-003
└── ...

cutoff-b-new
├── job-001
│   ├── INCAR
│   ├── KPOINTS
│   ├── POSCAR
│   └── POTCAR
├── job-002
├── job-003
└── ...
```

Then, you can run the command `tepkit thirdorder adjust_cutoff` like below:

```bash
tepkit thirdorder adjust_cutoff --old "cutoff-a-completed" --new "cutoff-b-new"
```

tepkit will check the POSCARs in their `job-*` dirs and copy the `vasprun.xml` from the old dir to new dir if they have identical `POSCAR`, and write a `tepkit.skip.info.toml` file in the new dir to denote the duplicate jobs.
- if new cutoff is **less than** old cutoff, you can directly extract the FORCE_CONSTANTS file in the new dir.

- if new cutoff is **greater than** than old cutoff, you need to calculate those uncompleted jobs first.
    Here is an example script to skip those completed jobs:
  
  ```bash
  #!/bin/bash
  
  cd "cutoff-b-new"
  
  for dir in job-*
  do
      cd ${dir}
      if [ -f "tepkit.skip.info.toml" ]
      then
          echo $(date) ${dir} "skipped." >> ../jobs.log
      else
          echo $(date) ${dir} "started..." >> ../jobs.log
          mpirun -np 8 vasp_std > vasp.log
          echo $(date) ${dir} "finished." >> ../jobs.log
      fi
      echo "----------" >> ../jobs.log
      cd ..
  done
  ```
