:Kir2_ch.MOD
: Kir2, inwardly rectifying channel


NEURON {
	SUFFIX kir2_ch
	USEION k READ ek WRITE ik
	RANGE g, ninf, tn, ik, gbar
	GLOBAL C_tn, vh, vc

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
	gbar = 3	(S/cm2)
	ek		(mV)
	vh = -80	(mV)
	vc = 5		(mV)
	C_tn = 1	(ms)
    mod_pka_g_min = 1 (1)
    mod_pka_g_max = 1 (1)
    mod_pka_g_half = 0.000100 (mM)
    mod_pka_g_slope = 0.01 (mM)
}

ASSIGNED {
	v	(mV)
	ninf
	tn	(ms)
	ik	(mA/cm2)
	g	(S/cm2)
    PKAci (mM)
    modulation_factor (1)
}

STATE {
	n
}

BREAKPOINT {
	SOLVE states METHOD cnexp
        modulation_factor=modulation(PKAci, mod_pka_g_min, mod_pka_g_max, mod_pka_g_half, mod_pka_g_slope)	   

        g = gbar*n*modulation_factor
	ik = g*(v-ek)
}

DERIVATIVE states{
	values()
	n' = (ninf - n)/tn
}

INITIAL {
	values()
	n = ninf
}

PROCEDURE values() {
	ninf = 1/(1 + exp((v - vh)/vc))
	tn = C_tn
}

FUNCTION modulation(conc (mM), mod_min (1), mod_max (1), mod_half (mM), mod_slope (mM)) (1) {
    : returns modulation factor
    modulation = mod_min + (mod_max-mod_min) / (1 + exp(-(conc - mod_half)/mod_slope))
}
