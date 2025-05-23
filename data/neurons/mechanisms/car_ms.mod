TITLE R-type calcium current (Cav2.3)


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
    SUFFIX car_ms
    USEION ca READ cai, cao WRITE ica VALENCE 2
    RANGE pbar, ica

    USEION PKAc READ PKAci VALENCE 0
    RANGE mod_pka_p_min, mod_pka_p_max, mod_pka_p_half, mod_pka_p_hill 
    RANGE mod_pka_p2_min, mod_pka_p2_max, mod_pka_p2_half, mod_pka_p2_hill 
    RANGE modulation_factor, modulation_factor2

}

PARAMETER {
    pbar = 0.0 	(cm/s)
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
    hinf
    htau (ms)
    PKAci (mM)
    modulation_factor (1)
    modulation_factor2 (1)
}

STATE { m h }

BREAKPOINT {
     SOLVE states METHOD cnexp
     modulation_factor=hill(PKAci, mod_pka_p_min, mod_pka_p_max, mod_pka_p_half, mod_pka_p_hill)	   
     modulation_factor2=hill(PKAci, mod_pka_p2_min, mod_pka_p2_max, mod_pka_p2_half, mod_pka_p2_hill)	   	   
    ica = pbar*m*m*m*h*ghk(v, cai, cao)*modulation_factor*modulation_factor2
}

INITIAL {
    rates()
    m = minf
    h = hinf
}

DERIVATIVE states { 
    rates()
    m' = (minf-m)/mtau*q
    h' = (hinf-h)/htau*q
}

PROCEDURE rates() {
    UNITSOFF
    minf = 1/(1+exp((v-(-29))/(-9.6)))
    mtau = 5.1
    hinf = 1/(1+exp((v-(-33.3))/17))
    htau = 22+80/(1+exp((v-(-19))/5))
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
	UNITSOFF
	hill = mod_min + (mod_max-mod_min) * pow(conc, hill_coefficient) / (pow(conc, hill_coefficient) + pow(half_activation, hill_coefficient))
	UNITSON
}



COMMENT

Original data by Foehring  et al (2000) [1] for dissociated MSNs from
P28-P42 Sprague-Dawley rat brain. Unspecified recording temperature. The
liquid junction potential was around 8 mV and was not corrected. Kinetics
of m3h type was fitted.  Inactivation time constants were measured in
neurons from endopiriform nucleus of P7-P21 Hartley guinea pigs [2]
at room temperature 22 C.

Original NEURON model by Wolf (2005) [3] modified by Alexander Kozlov
<akozlov@kth.se>. Activation curve fitted to m^3 kinetics as in [4],
activation time constant matched m^3 originally [1]. Smooth fit of
inactivation time constant from [2,3].

[1] Foehring RC, Mermelstein PG, Song WJ, Ulrich S, Surmeier DJ
(2000) Unique properties of R-type calcium currents in neocortical and
neostriatal neurons. J Neurophysiol 84(5):2225-36.

[2] Brevi S, de Curtis M, Magistretti J (2001) Pharmacological and
biophysical characterization of voltage-gated calcium currents in the
endopiriform nucleus of the guinea pig. J Neurophysiol 85(5):2076-87.

[3] Wolf JA, Moyer JT, Lazarewicz MT, Contreras D, Benoit-Marand M,
O'Donnell P, Finkel LH (2005) NMDA/AMPA ratio impacts state transitions
and entrainment to oscillations in a computational model of the nucleus
accumbens medium spiny projection neuron. J Neurosci 25(40):9080-95.

[4] Evans RC, Maniar YM, Blackwell KT (2013) Dynamic modulation of
spike timing-dependent calcium influx during corticostriatal upstates. J
Neurophysiol 110(7):1631-45.

ENDCOMMENT
