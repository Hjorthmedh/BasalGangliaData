:Migliore file Modify by Maciej Lazarewicz (mailto:mlazarew@gmu.edu) May/16/2001

TITLE l-calcium channel
: l-type calcium channel

: copy by josh

COMMENT

Neuromodulation is added as functions:
    
    modulationDA = 1 + modDA*(maxModDA-1)*levelDA

where:
    
    modDA  [0]: is a switch for turning modulation on or off {1/0}
    maxModDA [1]: is the maximum modulation for this specific channel (read from the param file)
                    e.g. 10% increase would correspond to a factor of 1.1 (100% +10%) {0-inf}
    levelDA  [0]: is an additional parameter for scaling modulation. 
                Can be used simulate non static modulation by gradually changing the value from 0 to 1 {0-1}
									
	  Further neuromodulators can be added by for example:
          modulationDA = 1 + modDA*(maxModDA-1)
	  modulationACh = 1 + modACh*(maxModACh-1)
	  ....

	  etc. for other neuromodulators
	  
	   
								     
[] == default values
{} == ranges
    
ENDCOMMENT

NEURON {
	SUFFIX cal_ch
	USEION ca READ cai,cao WRITE ica
        RANGE  gbar,ica , gcal
	GLOBAL vhm, vcm
	GLOBAL Ctm, atm, btm, tm0, vhtm
        GLOBAL minf,tau
        RANGE modACh, maxModACh, levelACh

}

UNITS {
	(mA) 	= 	(milliamp)
	(mV) 	= 	(millivolt)
	FARADAY =  	(faraday)  (kilocoulombs)
	R 	= 	(k-mole) (joule/degC)
	KTOMV 	= .0853 (mV/degC)
}

PARAMETER {
	v (mV)
	celsius = 6.3	(degC)
	gbar	= .003 	(mho/cm2)
	ki	= .001 	(mM)
	cai 		(mM)
	cao 		(mM)
        tfa	= 1
	vhm = -1.5
	vcm = 5.6
	Ctm = 3
	atm = 12
	btm = 11
	tm0 = 0
	vhtm = -2
        modACh = 0
        maxModACh = 1
        levelACh = 0

}

STATE { m }

ASSIGNED {
	ica (mA/cm2)
        gcal (mho/cm2)
        minf
        tau   (ms)
}

BREAKPOINT {
	SOLVE state METHOD cnexp
	gcal = gbar*m*m*h2(cai)*modulationACh()
	ica  = gcal*ghk(v,cai,cao)
}

INITIAL {
	rate(v)
	m = minf
}

FUNCTION h2(cai(mM)) {
	h2 = ki/(ki+cai)
}

FUNCTION ghk(v(mV), ci(mM), co(mM)) (mV) {
        LOCAL nu,f

        f = KTF(celsius)/2
        nu = v/f
        ghk=-f*(1. - (ci/co)*exp(nu))*efun(nu)
}

FUNCTION KTF(celsius (DegC)) (mV) {
        KTF = ((25./293.15)*(celsius + 273.15))
}

FUNCTION efun(z) {
	if (fabs(z) < 1e-4) {
		efun = 1 - z/2
	}else{
		efun = z/(exp(z) - 1)
	}
}

FUNCTION alp(v(mV)) (1/ms) {
	TABLE FROM -150 TO 150 WITH 200
	alp = 15.69*(-1.0*v+81.5)/(exp((-1.0*v+81.5)/10.0)-1.0)
}

FUNCTION bet(v(mV)) (1/ms) {
	TABLE FROM -150 TO 150 WITH 200
	bet = 0.29*exp(-v/10.86)
}

DERIVATIVE state {  
        rate(v)
        m' = (minf - m)/tau
}

PROCEDURE rate(v (mV)) { :callable from hoc
        LOCAL a

        a    = alp(v)
        :tau  = 1/(tfa*(a + bet(v)))
        :minf = tfa*a*tau
	tau = Ctm/(exp((v-vhtm)/atm) + exp((vhtm-v)/btm)) + tm0
	minf = 1/(1+exp(-(v-vhm)/vcm))
}
 
FUNCTION modulationACh() {
    : returns modulation factor
    
    modulationACh = 1 + modACh*(maxModACh-1)*levelACh 
}












