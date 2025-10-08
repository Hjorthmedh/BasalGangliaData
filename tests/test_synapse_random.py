from neuron import h
import numpy as np

h.load_file("stdrun.hoc")

soma = h.Section(name="soma")
syn_1 = h.tmGlut(soma(0.5))
syn_1.failRate = 0.5
syn_2 = h.tmGlut(soma(0.5))
syn_2.failRate = 0.5

spikes = np.arange(100, 1000, 10, dtype=int)

spike_times_1 = h.Vector(spikes)
stim_1 = h.VecStim()
stim_1.play(spike_times_1)

spike_times_2 = h.Vector(spikes)
stim_2 = h.VecStim()
stim_2.play(spike_times_2)

nc_1 = h.NetCon(stim_1, syn_1)
nc_1.weight[0] = 1
nc_2 = h.NetCon(stim_2, syn_2)
nc_2.weight[0] = 1

g_1 = h.Vector().record(syn_1._ref_g)
g_2 = h.Vector().record(syn_2._ref_g)
t = h.Vector().record(h._ref_t)

h.finitialize(-65)
h.tstop = 1000
h.run()

import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=np.array(t), y=np.array(g_1), name="first synapse"))
fig.add_trace(go.Scatter(x=np.array(t), y=np.array(g_2), name="second synapse"))
fig.show()
