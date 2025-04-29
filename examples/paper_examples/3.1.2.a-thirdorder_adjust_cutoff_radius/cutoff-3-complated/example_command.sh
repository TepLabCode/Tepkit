
for i in {01..72}
do
    cd job-$i
        echo job-$i start >> ../thirdorder.log
        mpirun -np 4 vasp_std > vasp.log
        echo job-$i end   >> ../thirdorder.log
    cd ..
done
