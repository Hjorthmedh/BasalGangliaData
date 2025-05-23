TITLE Slowly inactivating A-type potassium current (Kv1.2)


NEURON {
    SUFFIX kas_ms
    USEION k READ ek WRITE ik
    RANGE gbar, gk, ik

    USEION PKAc READ PKAci VALENCE 0
    RANGE mod_pka_g_min, mod_pka_g_max, mod_pka_g_half, mod_pka_g_hill 
    RANGE modulation_factor			 

}

UNITS {
    (S) = (siemens)
    (mV) = (millivolt)
    (mA) = (milliamp)
}

PARAMETER {
    gbar = 0.0 	(S/cm2) 
    a = 0.8
    :q = 1	: room temperature 22-24 C
    q = 3	: body temperature 33 C

    mod_pka_g_min = 1 (1)
    mod_pka_g_max = 1 (1)
    mod_pka_g_half = 0.000100 (mM)
    mod_pka_g_hill = 4 (mM)

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
    modulation_factor=hill(PKAci, mod_pka_g_min, mod_pka_g_max, mod_pka_g_half, mod_pka_g_hill)	   

    gk = gbar*m*m*(h*a+1-a)*modulation_factor
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
    minf = 1/(1+exp((v-(-27))/(-16)))
    mtau = 3.4+89.2*exp(-((v-(-34.3))/30.1)^2)
    hinf = 1/(1+exp((v-(-33.5))/21.5))
    htau = 548.7*6/(exp((v-(-96))/(-29.01))+exp((v-(-96))/100))
    : Du 2017
    :LOCAL alpha, beta, sum
    :UNITSOFF
    :alpha = 0.25/(1+exp((v-50)/(-20)))
    :beta = 0.05/(1+exp((v-(-90))/35))
    :sum = alpha+beta
    :minf = alpha/sum
    :mtau = 1/sum
    :
    :alpha = 0.0025/(1+exp((v-(-95))/16))
    :beta = 0.002/(1+exp((v-50)/(-70)))
    :sum = alpha+beta
    :hinf = a+(alpha/sum)*(1-a)
    :htau = 1/sum
    UNITSON
}

FUNCTION hill(conc (mM),  mod_min (1), mod_max (1), half_activation (mM), hill_coefficient (1)) (1) {
	UNITSOFF
	hill = mod_min + (mod_max-mod_min) * pow(conc, hill_coefficient) / (pow(conc, hill_coefficient) + pow(half_activation, hill_coefficient))
	UNITSON
}


	       
COMMENT

Experimental data by Shen et al (2004) [1]. Medium spiny neurons were
acutely dissociated from from young adult (P21-P28) Sprague-Dawley rat
brain. All recordings were conducted at 22-24 C. No correction for the
liquid junction potential was reported.

Conductance kinetics of m2h type is used [1,2] with partial inactivation,
m2 (a h + (1-a)). Fraction a is set to 0.8, as in [1, Fig.6B]; other
values for a are possible [2] (see also kas.mod in companion code).
Equation for htau [1] is corrected to match the authors' data [1, Fig.6B].
Time constants were corrected to body temperature with factor q=3 [1-3].
Later modification by Du [4] is close to this model with adjusted
inactivation.

[1] Shen W, Hernandez-Lopez S, Tkatch T, Held JE, Surmeier DJ (2004)
Kv1.2-containing K+ channels regulate subthreshold excitability of
striatal medium spiny neurons. J Neurophysiol 91(3):1337-49.

[2] Wolf JA, Moyer JT, Lazarewicz MT, Contreras D, Benoit-Marand M,
O'Donnell P, Finkel LH (2005) NMDA/AMPA ratio impacts state transitions
and entrainment to oscillations in a computational model of the nucleus
accumbens medium spiny projection neuron. J Neurosci 25(40):9080-95.

[3] Evans RC, Maniar YM, Blackwell KT (2013) Dynamic modulation of
spike timing-dependent calcium influx during corticostriatal upstates. J
Neurophysiol 110(7):1631-45.

[4] Du K, Wu YW, Lindroos R, Liu Y, Rózsa B, Katona G, Ding JB,
Kotaleski JH (2017) Cell-type-specific inhibition of the dendritic
plateau potential in striatal spiny projection neurons. Proc Natl Acad
Sci USA 114:E7612-E7621.

ENDCOMMENT
