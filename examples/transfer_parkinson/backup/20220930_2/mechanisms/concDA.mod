COMMENT
Two state kinetic scheme  which reproduces the concentration change of dopamine.

ENDCOMMENT

NEURON {
	POINT_PROCESS concDA
	RANGE tau1, tau2, e
	RANGE amplitude
	RANGE modulation_input
	NONSPECIFIC_CURRENT i
}

UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	
}

PARAMETER {
	tau1 = 400 (ms) <1e-9,1e9>
	tau2 = 300 (ms) <1e-9,1e9>
	amplitude = 0.25e-4
	modulation_input = 0
}

ASSIGNED {
     factor
     i (nM)
}

STATE {
	A 
	B 
}

INITIAL {
	LOCAL tp
	if (tau1/tau2 > 0.9999) {
		tau1 = 0.9999*tau2
	}
	if (tau1/tau2 < 1e-9) {
		tau1 = tau2*1e-9
	}
	A = 0
	B = 0
	tp = (tau1*tau2)/(tau2 - tau1) * log(tau2/tau1)
	factor = -exp(-tp/tau1) + exp(-tp/tau2)
	factor = 1/factor
}

BREAKPOINT {
	SOLVE state METHOD cnexp
	i = amplitude*(B-A)*modulator()		   
	
}

DERIVATIVE state {
	A' = -A/tau1
	B' = -B/tau2
}

NET_RECEIVE(weight (uS)) {
	A = A + weight*factor
	B = B + weight*factor
}

FUNCTION modulator() {

     modulator = modulation_input
     }
