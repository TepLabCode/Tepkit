poscar="./POSCAR"
supercell="3 3 1"
old_cutoff="-3"
new_cutoff="-2"
old_work_dir="cutoff-3-complated"
new_work_dir="cutoff-2-new"

# python thirdorder_vasp.py sow ${supercell} ${new_cutoff}
# tepkit thirdorder set --dir ${new_work_dir}
tepkit thirdorder adjust_cutoff --old ${old_work_dir} --new ${new_work_dir}

if [ ! -f "thirdorder_vasp.py" ]; then
    echo "Error: thirdorder_vasp.py does not exist."
    exit 1
fi
if [ ! -f "thirdorder_common.py" ]; then
    echo "Error: thirdorder_common.py does not exist."
    exit 1
fi

find ${old_work_dir}/job* -name vasprun.xml | sort -n | python thirdorder_vasp.py reap ${supercell} ${old_cutoff}
mv "FORCE_CONSTANTS_3RD" "./FORCE_CONSTANTS_3RD (${supercell} ${old_cutoff})"

find ${new_work_dir}/job* -name vasprun.xml | sort -n | python thirdorder_vasp.py reap ${supercell} ${new_cutoff}
mv "FORCE_CONSTANTS_3RD" "./FORCE_CONSTANTS_3RD (${supercell} ${new_cutoff})"
