# Striatal GABA synapses from Planert et al, 2010

Data from Figure 5, and Table 1 was used.

1. Data points from Figure 5A was manually extracted using plot digitizer. This provided D (TauR) and F (TauF) for ispn-ispn, ispn-dspn, dspn-spn, fs-spn.

2. Using mean and standard deviations from table 1, we identified the dspn-dspn and dspn-ispn points among the dspn-spn points, fullfilling the constraints (3 of each).

3. The U values are missing in Figure 5A, we adopted two stratergies.

A) Create JSON parameter files with the average U value for each synapse parameter set.

B) Sample U values and using them together with the extracted tauF and tauR.

Google Gemini was used for code generation.


Code is here:
https://github.com/Hjorthmedh/synaptic_fitting