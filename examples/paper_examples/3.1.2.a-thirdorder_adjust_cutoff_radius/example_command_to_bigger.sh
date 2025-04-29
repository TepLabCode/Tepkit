poscar="./POSCAR"
supercell="3 3 1"
old_cutoff="-3"
new_cutoff="-4"
old_work_dir="cutoff-3-complated"
new_work_dir="cutoff-4-new"

# python thirdorder_vasp.py sow ${supercell} ${new_cutoff}
# tepkit thirdorder set --dir ${new_work_dir}
tepkit thirdorder adjust_cutoff --old ${old_work_dir} --new ${new_work_dir}
