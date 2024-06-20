TITLE I-h channel from Magee 1998 for distal dendrites


NEURON {
	SUFFIX hd_lts
	NONSPECIFIC_CURRENT i
        RANGE ghdbar, vhalfl
        RANGE linf,taul

    USEION PKA READ PKAi VALENCE 0
    RANGE mod_pka_g_min, mod_pka_g_max, mod_pka_g_half, mod_pka_g_slope 
    RANGE modulation_factor			
}

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)

}

PARAMETER {
                        v 		        (mV)
			ehd  = -30		(mV)        
			celsius 	    (degC)
			ghdbar=.0001 	(mho/cm2)
			vhalfl=-81   	(mV)
			kl=-8
			vhalft=-75   	(mV)
			a0t=0.011      	(/ms)
		        zetat=2.2    	(1)
			gmt=.4   	    (1)
			q10=4.5
		        qtl=1
    mod_pka_g_min = 1 (1)
    mod_pka_g_max = 1 (1)
    mod_pka_g_half = 0.000100 (mM)
    mod_pka_g_slope = 0.01 (mM)
}



STATE {
    l
}

ASSIGNED {
	i (mA/cm2)
    linf      
    taul
    ghd
    PKAi (mM)
    modulation_factor (1)
}

INITIAL {
	rate(v)
	l=linf
}


BREAKPOINT {
     SOLVE states METHOD cnexp
     modulation_factor=modulation(PKAi, mod_pka_g_min, mod_pka_g_max, mod_pka_g_half, mod_pka_g_slope)	   
	   
     ghd = ghdbar*l*modulation_factor
     i = ghd*(v-ehd)

}


FUNCTION alpt(v(mV)) {
    alpt = exp(0.0378*zetat*(v-vhalft)) 
}

FUNCTION bett(v(mV)) {
    bett = exp(0.0378*zetat*gmt*(v-vhalft)) 
}

DERIVATIVE states {     : exact when v held constant; integrates over dt step
    rate(v)
    l' =  (linf - l)/taul
}

PROCEDURE rate(v (mV)) { :callable from hoc
    LOCAL a,qt
    qt=q10^((celsius-33)/10)
    a = alpt(v)
    linf = 1/(1 + exp(-(v-vhalfl)/kl))
    :linf = 1/(1+ alpl(v))
    taul = bett(v)/(qtl*qt*a0t*(1+a))
}



FUNCTION modulation(conc (mM), mod_min (1), mod_max (1), mod_half (mM), mod_slope (mM)) (1) {
    : returns modulation factor
    modulation = mod_min + (mod_max-mod_min) / (1 + exp(-(conc - mod_half)/mod_slope))
}
