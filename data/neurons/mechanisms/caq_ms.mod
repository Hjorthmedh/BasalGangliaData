TITLE Q-type calcium current (Cav2.1)

UNITS {
    (mV) = (millivolt)
    (mA) = (milliamp)
    (S) = (siemens)
    (molar) = (1/liter)
    (mM) = (millimolar)
    FARADAY = (faraday) (coulomb)
    R = (k-mole) (joule/degC)
}

NEURON {
    SUFFIX caq_ms
    USEION ca READ cai, cao WRITE ica VALENCE 2
    USEION PKAc READ PKAci VALENCE 0
    RANGE pbar, ica
    RANGE mod_pka_p_min, mod_pka_p_max, mod_pka_p_half, mod_pka_p_hill
    RANGE mod_pka_p2_min, mod_pka_p2_max, mod_pka_p2_half, mod_pka_p2_hill
    RANGE modulation_factor		   

}

PARAMETER {
    pbar = 0.0 (cm/s)
    :q = 1	: room temperature 22 C
    q = 3	: body temperature 35 C

    mod_pka_p_min = 1 (1)
    mod_pka_p_max = 1 (1)
    mod_pka_p_half = 0.000100 (mM)
    mod_pka_p_hill = 4 (1)

    mod_pka_p2_min = 1 (1)
    mod_pka_p2_max = 1 (1)
    mod_pka_p2_half = 0.000100 (mM)
    mod_pka_p2_hill = 4 (1)
		       
} 

ASSIGNED { 
    v (mV)
    ica (mA/cm2)
    eca (mV)
    celsius (degC)
    cai (mM)
    cao (mM)
    minf
    mtau (ms)
    modulation_factor (1)
    modulation_factor2 (1)    
    PKAci (mM)
}

STATE { m }

BREAKPOINT {
    SOLVE states METHOD cnexp
    modulation_factor=hill(PKAci, mod_pka_p_min, mod_pka_p_max, mod_pka_p_half, mod_pka_p_hill)	   	   
    modulation_factor2=hill(PKAci, mod_pka_p2_min, mod_pka_p2_max, mod_pka_p2_half, mod_pka_p2_hill)	   	   
    ica = pbar*m*m*ghk(v, cai, cao)*modulation_factor*modulation_factor2
}

INITIAL {
    rates()
    m = minf
}

DERIVATIVE states { 
    rates()
    m' = (minf-m)/mtau*q
}

PROCEDURE rates() {
    UNITSOFF
    minf = 1/(1+exp((v-(-16.3))/(-7.9)))
    mtau = 1.13*2
    UNITSON
}

FUNCTION ghk(v (mV), ci (mM), co (mM)) (.001 coul/cm3) {
    LOCAL z, eci, eco
    z = (1e-3)*2*FARADAY*v/(R*(celsius+273.15))
    eco = co*efun(z)
    eci = ci*efun(-z)
    ghk = (1e-3)*2*FARADAY*(eci-eco)
}

FUNCTION efun(z) {
    if (fabs(z) < 1e-4) {
        efun = 1-z/2
    }else{
        efun = z/(exp(z)-1)
    }
}


FUNCTION hill(conc (mM),  mod_min (1), mod_max (1), half_activation (mM), hill_coefficient (1)) (1) {
	hill = mod_min + (mod_max-mod_min) * pow(conc, hill_coefficient) / (pow(conc, hill_coefficient) + pow(half_activation, hill_coefficient))
}


COMMENT

Activation curve was reconstructed for cultured NAc neurons from P5-P32
Charles River rat pups [1].  Activation time constant was measured in
culture neurons from cerebellum of P2-P5 rat pups [2] at room temperature
22 C.

Original NEURON model by Wolf (2005) [3] was modified by Alexander Kozlov
<akozlov@csc.kth.se>. Activation curve was fitted to m2 kinetics [4],
activation time constant was scaled up as well.

[1] Churchill D, Macvicar BA (1998) Biophysical and pharmacological
characterization of voltage-dependent Ca2+ channels in neurons isolated
from rat nucleus accumbens. J Neurophysiol 79(2):635-47.

[2] Randall A, Tsien RW (1995) Pharmacological dissection of multiple
types of Ca2+ channel currents in rat cerebellar granule neurons. J
Neurosci 15(4):2995-3012.

[3] Wolf JA, Moyer JT, Lazarewicz MT, Contreras D, Benoit-Marand M,
O'Donnell P, Finkel LH (2005) NMDA/AMPA ratio impacts state transitions
and entrainment to oscillations in a computational model of the nucleus
accumbens medium spiny projection neuron. J Neurosci 25(40):9080-95.

[4] Brown AM, Schwindt PC, Crill WE (1993) Voltage dependence and
activation kinetics of pharmacologically defined components of the
high-threshold calcium current in rat neocortical neurons. J Neurophysiol
70(4):1530-43.

ENDCOMMENT
