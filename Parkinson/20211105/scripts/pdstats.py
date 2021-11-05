#!/usr/bin/python3

import glob
import json
import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.rcParams['figure.figsize'] = (8, 6)


plt.style.use('seaborn-darkgrid')


def get_data(files):
    data = dict()
    for pd, dfile in enumerate(files):
        d = json.load(open(dfile))
        dd = dict()
        dd['length'] = [d[cell]['dend']['length'] for cell in d]
        dd['nbranch'] = [d[cell]['dend']['nbranch'] for cell in d]
        dd['nstem'] = [d[cell]['dend']['nstem'] for cell in d]
        dd['nterm'] = [d[cell]['dend']['nterm'] for cell in d]
        data[pd] = dd
    return data


d1data = get_data(sorted([x for x in glob.iglob('./pd?-dspn.json')]))
d2data = get_data(sorted([x for x in glob.iglob('./pd?-ispn.json')]))
xticks = [0, 1, 2, 3]
xlabels = ['Control', 'PD1', 'PD2', 'PD3']

x = np.array(list(d1data.keys()))
ax1 = plt.subplot(2,2,1)
ax1.errorbar(x-0.05, [np.mean(d1data[pd]['length']) for pd in d1data],
             yerr=[np.std(d1data[pd]['length']) for pd in d1data],
             label='dSPN', fmt='o-')
ax1.errorbar(x+0.05, [np.mean(d2data[pd]['length']) for pd in d2data],
             yerr=[np.std(d2data[pd]['length']) for pd in d2data],
             label='iSPN', fmt='o-')
ax1.set_xticks(xticks)
ax1.set_xticklabels(xlabels)
ax1.set_title('Total dendritic length')
ax1.set_ylim(bottom=0)
#ax1.legend()

ax2 = plt.subplot(2,2,2)
ax2.errorbar(x-0.05, [np.mean(d1data[pd]['nbranch']) for pd in d1data],
             yerr=[np.std(d1data[pd]['nbranch']) for pd in d1data],
             label='dSPN', fmt='o-')
ax2.errorbar(x+0.05, [np.mean(d2data[pd]['nbranch']) for pd in d2data],
             yerr=[np.std(d2data[pd]['nbranch']) for pd in d2data],
             label='iSPN', fmt='o-')
ax2.set_xticks(xticks)
ax2.set_xticklabels(xlabels)
ax2.set_title('Number of branching points')
ax2.set_ylim(bottom=0)
ax2.legend()

ax3 = plt.subplot(2,2,3)
ax3.errorbar(x-0.05, [np.mean(d1data[pd]['nstem']) for pd in d1data],
             yerr=[np.std(d1data[pd]['nstem']) for pd in d1data], fmt='o-')
ax3.errorbar(x+0.05, [np.mean(d2data[pd]['nstem']) for pd in d2data],
             yerr=[np.std(d2data[pd]['nstem']) for pd in d2data], fmt='o-')
ax3.set_xticks(xticks)
ax3.set_xticklabels(xlabels)
ax3.set_title('Number of primary dendrites')
ax3.set_ylim(bottom=0)

ax4 = plt.subplot(2,2,4)
ax4.errorbar(x-0.05, [np.mean(d1data[pd]['nterm']) for pd in d1data],
             yerr=[np.std(d1data[pd]['nterm']) for pd in d1data], fmt='o-')
ax4.errorbar(x+0.05, [np.mean(d2data[pd]['nterm']) for pd in d2data],
             yerr=[np.std(d2data[pd]['nterm']) for pd in d2data], fmt='o-')
ax4.set_xticks(xticks)
ax4.set_xticklabels(xlabels)
ax4.set_title('Number of terminals')
ax4.set_ylim(bottom=0)

plt.tight_layout()
plt.show()
