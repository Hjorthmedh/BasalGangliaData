TITLE Fast transient sodium current


NEURON {
    SUFFIX naf_ms
    USEION na READ ena WRITE ina
    RANGE gbar, gna, ina
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
    gbar = 0.0 (S/cm2) 
    :q = 1	: room temperature 22 C
    q = 1.8	: body temperature 35 C
    mod_pka_g_min = 1 (1)
    mod_pka_g_max = 1 (1)
    mod_pka_g_half = 0.000100 (mM)
    mod_pka_g_hill = 4 (1)
}

ASSIGNED {
    v (mV)
    ena (mV)
    ina (mA/cm2)
    gna (S/cm2)
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
	   
    gna = gbar*m*m*m*h*modulation_factor
    ina = gna*(v-ena)
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
    :minf = 1/(1+exp((v-(-25.5))/(-9.2)))
    :mtau = 0.33+1/(exp((v-(-62))/14)+exp((v-(-60))/(-17)))
    :hinf = 1/(1+exp((v-(-63.2))/6))
    :htau = 0.6+1/(exp((v-(-44))/8)+exp((v-(-99))/(-44)))
    minf = 1/(1+exp((v-(-25))/(-10)))
    mtau = 0.33+1/(exp((v-(-62))/14)+exp((v-(-60))/(-17)))
    hinf = 1/(1+exp((v-(-62))/6))
    htau = 0.6+1/(exp((v-(-44))/8)+exp((v-(-99))/(-44)))
    UNITSON
}


FUNCTION hill(conc (mM),  mod_min (1), mod_max (1), half_activation (mM), hill_coefficient (1)) (1) {
	hill = mod_min + (mod_max-mod_min) * pow(conc, hill_coefficient) / (pow(conc, hill_coefficient) + pow(half_activation, hill_coefficient))
}


	       
COMMENT

Original data by Ogata and Tatebayashi (1990) [1]. Neostriatal neurons
of medium size (putative medium spiny neurons) freshly isolated from
the adult guinea pig brain (either sex, 200 g). Data compensated for
the liquid junction potential (-13 mV). Experiments carried out at room
temperature (22 C). Conductance fitted by m3h kinetics.

Smooth fit of mtau and htau data [1] by Alexander Kozlov <akozlov@kth.se>
assuming natural logarithm of tau values [1, Figs. 5 and 9] and
temperature correction factor of 1.8 [2] as suggested by Robert Lindroos
<robert.lindroos@ki.se>.

[1] Ogata N, Tatebayashi H (1990) Sodium current kinetics in freshly
isolated neostriatal neurones of the adult guinea pig. Pflugers Arch
416(5):594-603.

[2] Schwarz JR (1986) The effect of temperature on Na currents in rat
myelinated nerve fibres. Pflugers Arch. 406(4):397-404.

ENDCOMMENT
