# Delete the old mechanisms folder if needed

nrnivmodl /home/hjorth/HBP/BasalGangliaData/Parkinson/Bo2022/PD2/mechanisms
mpirun -n 2 snudda simulate TEST1-PD2-final --time 0.1
