import os
import pandas
import numpy as np
import matplotlib.pyplot as plt

trace_table_file = "traces/trace_table.txt"
trace_table = pandas.read_csv(trace_table_file, sep="\t", header=0,
                              names=["data_file", "unknown1", "unknown2", "frequency", "n_stim", "delay"])

if not os.path.exists("figures"):
    os.mkdir("figures")

for f_name in trace_table["data_file"]:
    print(f"Plotting {f_name}")
    
    volt = np.genfromtxt(os.path.join("traces", f_name), delimiter=",")
    # Freq is 5-20kHz, let's guess 10kHz here
    time = np.arange(0, len(volt)) * 1e-4

    amp_file = os.path.join("amplitudes", f"{f_name}_amp.dat")
    print(f"Loading {amp_file}") 
    amp_data = np.genfromtxt(amp_file, delimiter="\t")

    t_input = amp_data[:,0]
    amp_input = amp_data[:,1]

    plt.figure()
    plt.plot(time, volt, 'k-')
    # plt.ion()
    # plt.show()

    fig_name = os.path.join("figures", f"{f_name}.png".replace(".txt",""))

    for t, amp in zip(t_input, amp_input):
        t_idx = np.argmin(np.abs(time - t))
        t_peak_idx = np.argmax(volt[t_idx:t_idx+250]) + t_idx
        
        plt.plot([time[t_peak_idx], time[t_peak_idx]],
                 [volt[t_peak_idx], volt[t_peak_idx]-amp], 'r-')
    
    plt.savefig(fig_name)
    plt.close()
    
#    import pdb
#    pdb.set_trace()




    
