#!/usr/bin/python3

import json
import argparse
import numpy as np
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, help="morphometric statistics (json)")
parser.add_argument("-n", metavar='<str>', dest='neurite', type=str,
                    choices=['axon', 'dend'], default='dend',
                    help="neurite type (axon, dend) [dend]")

args = parser.parse_args()
mm = json.load(open(args.file))

neurite_xdim = np.array([mm[x][args.neurite]['xdim'] for x in mm])
neurite_ydim = np.array([mm[x][args.neurite]['ydim'] for x in mm])
neurite_zdim = np.array([mm[x][args.neurite]['zdim'] for x in mm])
neurite_extent = np.array([max(mm[x][args.neurite]['xdim'],
                            mm[x][args.neurite]['ydim'],
                            mm[x][args.neurite]['ydim']) for x in mm])
neurite_length = np.array([mm[x][args.neurite]['length'] for x in mm])
neurite_nstem = np.array([mm[x][args.neurite]['nstem'] for x in mm])
neurite_nbranch = np.array([mm[x][args.neurite]['nbranch'] for x in mm])
neurite_nterm = np.array([mm[x][args.neurite]['nterm'] for x in mm])

plt.style.use('seaborn-darkgrid')

fig, axs = plt.subplots(2, 3, figsize=(12,8))
fig.suptitle(f'{args.file} ({args.neurite})')

axs[0, 0].hist(neurite_xdim, histtype='step', lw=3, color='r', alpha=0.5)
axs[0, 0].hist(neurite_ydim, histtype='step', lw=3, color='g', alpha=0.5)
axs[0, 0].hist(neurite_zdim, histtype='step', lw=3, color='tab:blue', alpha=0.5)
axs[0, 0].set_xlabel('X, Y, Z extent ($\mu$m)')
axs[0, 0].set_xlim(left=0)

axs[0, 1].hist(neurite_extent, rwidth=0.8, alpha=0.5)
axs[0, 1].axvline(neurite_extent.mean(), ls='--', lw=3)
axs[0, 1].set_xlabel('Max extent ($\mu$m)')
axs[0, 1].set_xlim(left=0)

axs[0, 2].hist(neurite_length, rwidth=0.8, alpha=0.5)
axs[0, 2].axvline(neurite_length.mean(), ls='--', lw=3)
axs[0, 2].set_xlabel('Total length ($\mu$m)')
axs[0, 2].set_xlim(left=0)

axs[1, 0].hist(neurite_nstem, rwidth=0.8, alpha=0.5)
axs[1, 0].axvline(neurite_nstem.mean(), ls='--', lw=3)
axs[1, 0].set_xlabel('Number of primary branches')
axs[1, 0].set_xlim(left=0)

axs[1, 1].hist(neurite_nbranch, rwidth=0.8, alpha=0.5)
axs[1, 1].axvline(neurite_nbranch.mean(), ls='--', lw=3)
axs[1, 1].set_xlabel('Number of branch points')
axs[1, 1].set_xlim(left=0)

axs[1, 2].hist(neurite_nterm, rwidth=0.8, alpha=0.5)
axs[1, 2].axvline(neurite_nterm.mean(), ls='--', lw=3)
axs[1, 2].set_xlabel('Number of terminal points')
axs[1, 2].set_xlim(left=0)

plt.tight_layout()
plt.show()
