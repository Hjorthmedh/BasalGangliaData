TITLE Glutamatergic synapse with short-term plasticity (stp)

COMMENT

ENDCOMMENT

NEURON {
    THREADSAFE
    POINT_PROCESS tmGlut_double
    RANGE tau1_ampa, tau2_ampa, tau3_ampa, tau1_nmda, tau2_nmda, tau3_nmda
    RANGE I2_ampa, I3_ampa, I2_nmda, I3_nmda
    RANGE tpeak_ampa, factor_ampa, tpeak_nmda, factor_nmda
    RANGE g_ampa, g_nmda, i_ampa, i_nmda, itot_ampa, itot_nmda, nmda_ratio
    RANGE e, g, i, q, mg
    RANGE tau, tauR, tauF, U, u0
    RANGE ca_ratio_ampa, ca_ratio_nmda, mggate, use_stp
    RANGE failRate

    USEION DA READ DAi VALENCE 0
    RANGE mod_da_g_ampa_min, mod_da_g_ampa_max, mod_da_g_ampa_half, mod_da_g_ampa_slope
    RANGE mod_da_g_nmda_min, mod_da_g_nmda_max, mod_da_g_nmda_half, mod_da_g_nmda_slope
    RANGE modulation_factor_ampa, modulation_factor_nmda, modulation_factor_fail
    
    NONSPECIFIC_CURRENT i
    USEION cal WRITE ical VALENCE 2

    RANDOM release_probability
}

UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (uS) = (microsiemens)
    (mM) = (milli/liter)
}

PARAMETER {
    : input_region ; cell_type
    e = 0 (mV)
    tau = 3 (ms)
    tauR = 100 (ms)  : tauR > tau
    tauF = 100 (ms)  : tauF >= 0
    U = 0.3 (1) <0, 1>
    u0 = 0.1 (1) <0, 1>
    ca_ratio_ampa = 0.005
    ca_ratio_nmda = 0.1
    mg = 1 (mM)

    mod_da_g_ampa_min = 1 (1)
    mod_da_g_ampa_max = 1 (1)
    mod_da_g_ampa_half = 0.000100 (mM)
    mod_da_g_ampa_slope = 0.01 (mM)

    mod_da_g_nmda_min = 1 (1)
    mod_da_g_nmda_max = 1 (1)
    mod_da_g_nmda_half = 0.000100 (mM)
    mod_da_g_nmda_slope = 0.01 (mM)

    mod_da_fail_min = 0 (1)
    mod_da_fail_max = 0 (1)
    mod_da_fail_half = 0.000100 (mM)
    mod_da_fail_slope = 0.01 (mM)

    failRateScaling = 0
    failRate = 0
    use_stp = 1     : to turn of use_stp -> use 0

    : No PARAMETER defaults here by design -- tau1/2/3, I2/I3, tpeak, factor
    : (per receptor type) and nmda_ratio are set externally, per pathway,
    : from JSON config (see ../../synapses/striatum/tmGlut_double_config/
    : for pathway-specific fits, and ../../synapses/striatum/
    : tmGlut_double-default.json for the generic default -- see COMMENT
    : block below for the fit + Q10 derivation behind that default).
    tau1_ampa      (ms)
    tau2_ampa      (ms)
    tau3_ampa      (ms)
    I2_ampa
    I3_ampa
    tpeak_ampa     (ms)
    factor_ampa
    tau1_nmda      (ms)
    tau2_nmda      (ms)
    tau3_nmda      (ms)
    I2_nmda
    I3_nmda
    tpeak_nmda     (ms)
    factor_nmda
    nmda_ratio




}

ASSIGNED {
    v (mV)
    i (nA)
    i_ampa (nA)
    i_nmda (nA)
    ical (nA)
    ical_ampa (nA)
    ical_nmda (nA)
    g (uS)
    g_ampa (uS)
    g_nmda (uS)

    x
    DAi (mM)
    modulation_factor_ampa (1)
    modulation_factor_nmda (1)
    modulation_factor_fail (1)


}

STATE {
    A_ampa (uS)
    B_ampa (uS)
    C_ampa (uS)
    A_nmda (uS)
    B_nmda (uS)
    C_nmda (uS)
}

INITIAL {

    A_ampa = 0
    B_ampa = 0
    C_ampa = 0

    A_nmda = 0
    B_nmda = 0
    C_nmda = 0

}

BREAKPOINT {
    LOCAL itot_nmda, itot_ampa, mggate
    SOLVE state METHOD cnexp


    modulation_factor_ampa=hill(DAi, mod_da_g_ampa_min, mod_da_g_ampa_max, mod_da_g_ampa_half, mod_da_g_ampa_slope)
    modulation_factor_nmda=hill(DAi, mod_da_g_nmda_min, mod_da_g_nmda_max, mod_da_g_nmda_half, mod_da_g_nmda_slope)
    modulation_factor_fail=hill(DAi, mod_da_fail_min, mod_da_fail_max, mod_da_fail_half, mod_da_fail_slope)
    
    : NMDA
    mggate    = 1 / (1 + exp(-0.062 (/mV) * v) * (mg / 2.62 (mM))) : 3.57 instead of 2.62 if LJP not corrected
    g_nmda    = (I3_nmda*C_nmda + I2_nmda* B_nmda - (I3_nmda+I2_nmda)* A_nmda) * modulation_factor_nmda
    itot_nmda = g_nmda * (v - e) * mggate
    ical_nmda = ca_ratio_nmda*itot_nmda
    i_nmda    = itot_nmda - ical_nmda

    : AMPA
    g_ampa    = (I3_ampa*C_ampa + I2_ampa* B_ampa - (I3_ampa+I2_ampa)* A_ampa)  * modulation_factor_ampa
    itot_ampa = g_ampa*(v - e)
    ical_ampa = ca_ratio_ampa*itot_ampa
    i_ampa    = itot_ampa - ical_ampa

    : total values
    ical      = ical_nmda + ical_ampa
    g         = g_ampa + g_nmda
    i         = i_ampa + i_nmda

    : printf("%g\t%g\t%g\t%g\t%g\n",tau1_ampa,B_ampa,A_ampa,B_nmda,A_nmda)
    : printf("%g\t%g\t%g\t%g\t%g\n",v,g_nmda,g,i,ical)
    : printf("%g\t%g\t%g\t%g\t%g\n",tau1_ampa,tau2_ampa,tau1_nmda,tau2_nmda,nmda_ratio)
    : printf("%g\t\n",tau)
}

DERIVATIVE state {
    A_ampa' = -A_ampa/tau1_ampa
    B_ampa' = -B_ampa/tau2_ampa
    C_ampa' = -C_ampa/tau3_ampa
    A_nmda' = -A_nmda/tau1_nmda
    B_nmda' = -B_nmda/tau2_nmda
    C_nmda' = -C_nmda/tau3_nmda
}

NET_RECEIVE(weight (uS), y, z, u, tsyn (ms)) {
    LOCAL weight_ampa, weight_nmda
    INITIAL {
        y = 0
        z = 0
        u = u0
        tsyn = t
        : printf("t\t t-tsyn\t y\t z\t u\n")

    }

    if ( weight <= 0 ) {
VERBATIM
        return;
ENDVERBATIM
    }
    if( urand() > failRate*(1 + modulation_factor_fail)) {

      z = z*exp(-(t-tsyn)/tauR)
      z = z + (y*(exp(-(t-tsyn)/tau) - exp(-(t-tsyn)/tauR)) / (tau/tauR - 1) )
      y = y*exp(-(t-tsyn)/tau)
      x = 1-y-z
      if (tauF > 0) {
          u = u*exp(-(t-tsyn)/tauF)
          u = u + U*(1-u)
      } else {
          u = U
      }

      if (use_stp > 0) {
  	 : We divide by U to normalise, so that g gives amplitude
           : of first activation
          weight_ampa = weight *x*u / U
      } else {
          weight_ampa = weight
      }

      weight_nmda = weight_ampa*nmda_ratio

      A_ampa = A_ampa + weight_ampa*factor_ampa
      B_ampa = B_ampa + weight_ampa*factor_ampa
      C_ampa = C_ampa + weight_ampa*factor_ampa
      A_nmda = A_nmda + weight_nmda*factor_nmda
      B_nmda = B_nmda + weight_nmda*factor_nmda
      C_nmda = C_nmda + weight_nmda*factor_nmda

      y = y + x*u
      : printf("** %g\t%g\t%g\t%g\t%g\n", t, t-tsyn, y, z, u)
      tsyn = t
    }
}

FUNCTION urand() {
    urand = random_uniform(release_probability)
}

FUNCTION hill(conc (mM),  mod_min (1), mod_max (1), half_activation (mM), hill_coefficient (1)) (1) {
     hill = mod_min + (mod_max-mod_min) * pow(conc, hill_coefficient) / (pow(conc, hill_coefficient) + pow(half_activation, hill_coefficient))
 }



COMMENT
(2026-06-25) Per Johannes's direction, moved the AMPA/NMDA default
tau1/2/3, I2/I3, factor, and tpeak values (added below on 2026-06-24,
see that note) out of PARAMETER and into an external JSON config
instead: ../../synapses/striatum/tmGlut_double-default.json, alongside
the existing per-pathway configs in
../../synapses/striatum/tmGlut_double_config/. PARAMETER itself is back
to its original bare-declaration state (these RANGE vars are set
externally, per the 2020-09 note below). The numbers themselves, and the
fit they came from, are unchanged from the 2026-06-24 note -- only where
they live changed. NMDA values in that JSON were originally fit against
digitisation-derived targets later found inconsistent with Chapman et
al. 2003's own reported decay components; both the JSON and the note
below have since been updated with a corrected refit against the paper's
actual values (szmod validate_synapse/optimize_double_joint.py).

(2026-06-24) AMPA/NMDA time constants for the triple-exponential kernel
ported from the szmod project's validate_synapse/ pipeline
(github.com/Hjorthmedh/szmod, branch feature/tmglut-double-tau-fit), fit
using the same joint Nelder-Mead procedure described in tmglut.mod's
COMMENT block (8 szmod WT SPN models, full distance-stratified dendrite
set averaged every iteration). Only the PARAMETER defaults (since moved
to JSON, see the 2026-06-25 note above) and this note were added -- the
DA/ACh modulation formalism and everything else here are unchanged.
tau1/2/3, I2/I3, factor, and tpeak previously had no defaults at all (had
to be set externally before every run, see the 2020-09 note below); they
now have static, pre-scaled-at-35 degC default values, same convention as
tmglut.mod (just sourced from JSON rather than PARAMETER).

AMPA: a regularized 4-param fit (tau1, tau2, tau3, I3_ampa; I2_ampa=1
fixed) against the same targets tmglut.mod uses (Ding et al. 2008 CS/TS
Table 1 midpoint: t10-90=2.1 ms, tau2=4.74 ms) converged to I3_ampa ~
0.0075 -- negligible -- confirming AMPA decay does not need the 3rd
exponential. tau1_ampa/tau2_ampa from that fit converge to the same
values as tmglut.mod's own 2-exponential fit, since with I3=0 the two
mechanisms' AMPA kernels are mathematically identical:
	tau1_ampa = 1.688 ms,  tau2_ampa = 3.443 ms,  I2_ampa = 1,  I3_ampa = 0
	(tau3_ampa is then inert; any value > tau1_ampa works, e.g. 5*tau2_ampa)

This isn't just an artifact of the single-decay-tau AMPA target giving
the optimizer nothing to fit a 2nd exponential to: szmod's
validate_synapse/Experimental_traces/fit_ding2008_ampa_biexp.py fits a
free biexponential directly to each of Ding et al. 2008's individual
digitised quantal AMPA traces (5 cortical + 6 thalamic) and finds no
stable second time constant -- 9/11 fits degenerate (the two taus
collapse together, or one amplitude fraction collapses to ~0/~1); the
2 that don't either hit the fit's upper bound (clearly fitting
digitisation noise) or carry ~0% of the amplitude in the "slow"
component anyway. Contrast with Chapman et al. 2003's NMDA traces below,
where the same free-fit procedure lands on a stable, consistent fast/slow
split across cells. AMPA decay genuinely looks monoexponential at the
single-trace level, not just at the population-mean level the 4.74ms
target was built from.

NMDA: Chapman et al. 2003 NMDA decay genuinely is biexponential. Fit
against rise + tau_fast + tau_slow + amp_fast_frac targets taken
directly from the paper's own reported decay components (not from a
digitised-trace re-fit -- an earlier version of this fit used
tau_fast=71.5ms/tau_slow=861.9ms/fast_frac=0.811 derived that way, found
inconsistent with the paper's own values and superseded; see git history
if needed):
	targets: rise=12.13 ms, tau_fast=48.0 ms, tau_slow=324.0 ms, amp_fast_frac=0.34
	(fast=48+-6 ms, slow=324+-37 ms, fast-amplitude-fraction=0.34+-0.03)

Fit (22 degC reference, joint Nelder-Mead, full-stratified, 8 models):
	tau1_nmda = 8.566 ms,  tau2_nmda = 40.336 ms,  tau3_nmda = 315.954 ms,
	I2_nmda = 1,  I3_nmda = 0.9538
	-> full-stratified validation (longer simlen for an accurate slow-tau
	read): rise=12.13 ms, tau_fast=47.8 ms, tau_slow=323.4 ms,
	amp_fast_frac=0.339 (targets: 12.13 / 48.0 / 324.0 / 0.34)

(2025-11-03) Switched to new modulation formalism, in line with new tmglut.mod

(2025-10-08) NEURON 9.0+ compatibility. Replaced scop_random with the
new RANDOM keyword.
See: https://nrn.readthedocs.io/en/latest/nmodl/language/nmodl_neuron_extension.html#random

(2020-09) C_ampa and C_nmda added to take into account a second decay time constant.
tpeak_ampa, tpeak_nmda, factor_ampa and factor_nmda are now calculated during the fitting procedure.
g_nmda and g_ampa updated.
mggate updated to take into account LJP correction. Ilaria Carannante, ilariac@kth.se

(2019-11-29) Synaptic failure rate (fail) added. Random factor, no
reproducibility guaranteed in parallel sim.

(2019-08-21) We normalise the activation by U, to make sure that g specifies
             the conductance of the first actvation

(2019-06-05) Q-factor was calculated in INITAL block, which meant if
the synapse was reinitalised then the time constants changed with each
initalise. Updated: Johannes Hjorth, hjorth@kth.se

- updates by Robert Lindroos (robert.lindroos at ki.se):
Missing line calculating Ca ratio of NMDA current fixed. The whole block were updated since
plotting ratios for both nmda and ampa gave 0.
- switch for turning of short term dynamics added. If used this synapse will summate.

Implementation of glutamatergic synapse model with short-term facilitation
and depression based on modified tmgsyn.mod [1] by Tsodyks et al [2].
Choice of time constants and calcium current model follows [3].
NEURON implementation by Alexander Kozlov <akozlov@kth.se>.

[1] tmgsyn.mod, ModelDB (https://senselab.med.yale.edu/ModelDB/),
accession number 3815.

[2] Tsodyks M, Uziel A, Markram H (2000) Synchrony generation in recurrent
networks with frequency-dependent synapses. J Neurosci. 20(1):RC50.

[3] Wolf JA, Moyer JT, Lazarewicz MT, Contreras D, Benoit-Marand M,
O'Donnell P, Finkel LH (2005) NMDA/AMPA ratio impacts state transitions
and entrainment to oscillations in a computational model of the nucleus
accumbens medium spiny projection neuron. J Neurosci 25(40):9080-95.
ENDCOMMENT
