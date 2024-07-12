TITLE Fast A-type potassium current (Kv4.2)


NEURON {
    SUFFIX kaf_lts
    USEION k READ ek WRITE ik
    RANGE gbar, gk, ik, q

    USEION PKAc READ PKAci VALENCE 0
    RANGE mod_pka_g_min, mod_pka_g_max, mod_pka_g_half, mod_pka_g_slope 
    RANGE modulation_factor			     
}

UNITS {
    (S) = (siemens)
    (mV) = (millivolt)
    (mA) = (milliamp)
}

PARAMETER {
    gbar = 0.0 	(S/cm2) 
    :q = 1	: room temperature (unspecified)
    q = 3	: body temperature 35 C
    mod_pka_g_min = 1 (1)
    mod_pka_g_max = 1 (1)
    mod_pka_g_half = 0.000100 (mM)
    mod_pka_g_slope = 0.01 (mM)
}

ASSIGNED {
    v (mV)
    ek (mV)
    ik (mA/cm2)
    gk (S/cm2)
    minf
    mtau (ms)
    hinf
    htau (ms)
    PKAci (mM)
    modulation_factor (1)
}

STATE { m h }

BREAKPOINT {
     SOLVE states METHOD cnexp
     modulation_factor=modulation(PKAci, mod_pka_g_min, mod_pka_g_max, mod_pka_g_half, mod_pka_g_slope)	   
	   
     gk = gbar*m*m*h*modulation_factor
     ik = gk*(v-ek)
}

DERIVATIVE states {
    rates()
    m' = (minf-m)/mtau*q
    h' = (hinf-h)/htau*q
}

INITIAL {
    rates()
    m = minf
    h = hinf
}

PROCEDURE rates() {
    UNITSOFF
    minf = 1/(1+exp((v-(-10))/(-17.7)))
    mtau = (0.9+1.1/(1+exp((v-(-30))/10)))*2
    hinf = 1/(1+exp((v-(-75.6))/11.8))
    htau = 14
    UNITSON
}


FUNCTION modulation(conc (mM), mod_min (1), mod_max (1), mod_half (mM), mod_slope (mM)) (1) {
    : returns modulation factor
    modulation = mod_min + (mod_max-mod_min) / (1 + exp(-(conc - mod_half)/mod_slope))
}

	       
COMMENT

Original data by Tkatch et al (2000) [1]. Neostriatal neurons were acutely
dissociated from young adult rats, age P28-P42.  Electrophysiological
recordings were done at unspecified temperature (room temperature 20-22 C
assumed). Potentials were not corrected for the liquid junction potential
(estimated 1-2 mV).

Conductance kinetics of m2h type is used [2].  Activation m^1 matches
experimental data [1, Fig.2C]. Activation time constants were fitted to
tabulated data [1, Fig.2B] by Alexander Kozlov <akozlov@kth.se> and scaled
up x2 for m2 kinetics.  Slope of inactivation function fitted to the data
[1, Fig.3B] with half inactivation potential -75.6 mV. Temperature factor
q between 3 [2] and 1.5 [3] was used for body temperature.

[1] Tkatch T, Baranauskas G, Surmeier DJ (2000) Kv4.2 mRNA abundance and
A-type K(+) current amplitude are linearly related in basal ganglia and
basal forebrain neurons. J Neurosci 20(2):579-88.

[2] Wolf JA, Moyer JT, Lazarewicz MT, Contreras D, Benoit-Marand M,
O'Donnell P, Finkel LH (2005) NMDA/AMPA ratio impacts state transitions
and entrainment to oscillations in a computational model of the nucleus
accumbens medium spiny projection neuron. J Neurosci 25(40):9080-95.

[3]  Evans RC, Morera-Herreras T, Cui Y, Du K, Sheehan T, Kotaleski JH,
Venance L, Blackwell KT (2012) The effects of NMDA subunit composition on
calcium influx and spike timing-dependent plasticity in striatal medium
spiny neurons. PLoS Comput Biol 8(4):e1002493.

ENDCOMMENT
