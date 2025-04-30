TITLE SK-type calcium activated K channel (KCa2.2)

: The Ca-buffer for SK should use microdomains, and the time constant should be
: Ca-dependent, faster time constant for higher Ca-concentration
: DA does not directly modulate SK, but rather the Ca channels (ie the Ca influx)
: Temporary fix for Ca-dynamics, we allow DA to directly modulate the SK channel (phenomelogical solution as real modulation is indirect)					
	      
UNITS {
    (molar) = (1/liter)
    (mV) = (millivolt)
    (mA) = (milliamp)
    (mM) = (millimolar)
}

NEURON {
    SUFFIX sk_ms
    USEION ca READ cai
    USEION k READ ek WRITE ik
    USEION PKAc READ PKAci VALENCE 0
    
    RANGE gbar, ik, o
    RANGE mod_pka_g_min, mod_pka_g_max, mod_pka_g_half, mod_pka_g_hill 
    RANGE modulation_factor
    			 
}

PARAMETER {
    gbar = 0.0 	(mho/cm2)
    :q = 1	: room temperature
    q = 1	: body temperature
    mod_pka_g_min = 1 (1)
    mod_pka_g_max = 1 (1)
    mod_pka_g_half = 0.000100 (mM)
    mod_pka_g_hill = 4 (1)

}

ASSIGNED {
    v (mV)
    ik (mA/cm2)
    cai (mM) 
    ek (mV)
    oinf
    otau (ms)
    PKAci (mM)
    modulation_factor (1)

}

STATE { o }

BREAKPOINT {
    SOLVE state METHOD cnexp
     modulation_factor=hill(PKAci, mod_pka_g_min, mod_pka_g_max, mod_pka_g_half, mod_pka_g_hill)		   
    ik = gbar*o*(v-ek) * modulation_factor
}

DERIVATIVE state {
    rate(v, cai)
    o' = (oinf-o)/otau*q
}

INITIAL {
    rate(v, cai)
    o = oinf
}

PROCEDURE rate(v (mV), ca (mM)) {
    LOCAL a
    a = (ca/0.57e-3)^5.2
    oinf = a/(1+a)
    otau = 4.9
}

FUNCTION hill(conc (mM),  mod_min (1), mod_max (1), half_activation (mM), hill_coefficient (1)) (1) {
	hill = mod_min + (mod_max-mod_min) * pow(conc, hill_coefficient) / (pow(conc, hill_coefficient) + pow(half_activation, hill_coefficient))
}


COMMENT

Experimental data was obtained for the apamin-sensitive clone rSK2 from
rat brain cDNA expressed in Xenopus oocytes [1,2].  All experiments were
performed at room tempretaure.

Original model [3] used calcium dependence from [2, Fig.2] and calcium
activation time constant from [1,  Fig.13]. NEURON implementation by
Alexander Kozlov <akozlov@kth.se> follows the revised model [4].

[1] Hirschberg B, Maylie J, Adelman JP, Marrion NV (1998) Gating of
recombinant small-conductance Ca-activated K+ channels by calcium. J
Gen Physiol 111(4):565-81.

[2] Maylie J, Bond CT, Herson PS, Lee WS, Adelman JP (2004) Small
conductance Ca2+-activated K+ channels and calmodulin. J Physiol 554(Pt
2):255-61.

[3] Evans RC, Morera-Herreras T, Cui Y, Du K, Sheehan T, Kotaleski JH,
Venance L, Blackwell KT (2012) The effects of NMDA subunit composition on
calcium influx and spike timing-dependent plasticity in striatal medium
spiny neurons. PLoS Comput Biol 8(4):e1002493.

[4] Evans RC, Maniar YM, Blackwell KT (2013) Dynamic modulation of
spike timing-dependent calcium influx during corticostriatal upstates. J
Neurophysiol 110(7):1631-45.

ENDCOMMENT
