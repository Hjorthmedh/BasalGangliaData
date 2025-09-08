TITLE Fast transient sodium current

COMMENT

original file decorator
-----------------------
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
-----------------------------------------------------------------------

-Jan -24: adding Ca permability of channel (RL)
-Feb -24: slow inactivation gate added following dynamics of: 
    https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4254877/ (RL)
-April -24: time constant of slow inactivation updated from 160 -> 580 in accordance with: 
	https://pubmed.ncbi.nlm.nih.gov/25852980/
	https://modeldb.science/183722?tab=2&file=YuCanavier2015/soma_bursting_ODE.m (RL)

- earlier (2019-2020ish)

Neuromodulation is added as functions:
    
    modulationDA = 1 + modDA*(maxModDA-1)*levelDA

where:
    
    modDA  [0]: is a switch for turning modulation on or off {1/0}
    maxModDA [1]: is the maximum modulation for this specific channel (read from the param file)
                    e.g. 10% increase would correspond to a factor of 1.1 (100% +10%) {0-inf}
    levelDA  [0]: is an additional parameter for scaling modulation. 
                Can be used simulate non static modulation by gradually changing the value from 0 to 1 {0-1}
									
	  Further neuromodulators can be added (assuming they are independent...) by for example:
          modulationDA = 1 + modDA*(maxModDA-1)
	  modulationACh = 1 + modACh*(maxModACh-1)
	  ....

	  etc. for other neuromodulators	   
								     
[] == default values
{} == ranges

ENDCOMMENT

NEURON {
    SUFFIX naf_th
    USEION na READ ena WRITE ina
    RANGE ca_ratio
    USEION ca WRITE ica VALENCE 2
    RANGE vhalf_hs, slope_hs, tconst_hs, tmin_hs, thalf_hs, hs, h, use_hs
    RANGE mhalf, mslope, hhalf
    RANGE gbar, g, q, i
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
    ca_ratio = 0.005
    
    mslope = 10
    mhalf = -25
    hhalf = -62
    
    use_hs = 1 : use slow inactivation gate if 1 (else don't use)
    vhalf_hs = -54.8
    slope_hs = 1.57
    tconst_hs = 160
    tmin_hs = 20
    thalf_hs = 47.2
}

ASSIGNED {
    v (mV)
    ena (mV)
    ina (mA/cm2)
    ica (nA)
    g (S/cm2)
    minf
    mtau (ms)
    hinf
    htau (ms)
    hsinf
    hstau (ms)
    i (mA/cm2)
}

STATE { m h hs}

BREAKPOINT {
    LOCAL itotal
    SOLVE states METHOD cnexp
    if (use_hs == 1) {
    	g = gbar*m*m*m*h*hs
	} else {
    	g = gbar*m*m*m*h
	}
    itotal = g*(v-ena)
    ica = ca_ratio*itotal
    ina = itotal - ica : should this be adjusted for valence?
    i = ina + ica
    
}

DERIVATIVE states {
    rates()
    m' = (minf-m)/mtau*q
    h' = (hinf-h)/htau*q
    if (use_hs == 1) {
    	hs' = (hsinf-hs)/hstau  : q-factor not added since time constant changed anyway
	}
}

INITIAL {
    rates()
    m = minf
    h = hinf
    if (use_hs == 1) {
    	hs = hsinf
	}
}

PROCEDURE rates() {
    UNITSOFF
    :minf = 1/(1+exp((v-(-25.5))/(-9.2)))
    :mtau = 0.33+1/(exp((v-(-62))/14)+exp((v-(-60))/(-17)))
    :hinf = 1/(1+exp((v-(-63.2))/6))
    :htau = 0.6+1/(exp((v-(-44))/8)+exp((v-(-99))/(-44)))
    minf = 1/(1+exp(-(v-mhalf)/(mslope)))
    mtau = 0.33+1/(exp((v-(-62))/14)+exp((v-(-60))/(-17)))
    hinf = 1/(1+exp((v-hhalf)/6))
    htau = 0.6+1/(exp((v-(-44))/8)+exp((v-(-99))/(-44)))
    if (use_hs == 1) {
		hsinf = 1/(1+exp((v-(vhalf_hs))/slope_hs))
		hstau = tmin_hs + tconst_hs/(1 + exp(v + thalf_hs))
	}
    UNITSON
}




