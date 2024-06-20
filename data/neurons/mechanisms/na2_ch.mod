COMMENT
NA2_CH.MOD

c1 - c2 - c3 - c4 - c5 - o  - is1
|    |    |    |    |    |
i1 - i2 - i3 - i4 - i5 - i6 - is2

FAST

6/18/2003

    
ENDCOMMENT


NEURON {
	SUFFIX na2_ch
	USEION na READ ena WRITE ina
	RANGE g, ina, gbar, a
	GLOBAL Con, Coff, Oon, Ooff
	GLOBAL a0, vha, vca
	GLOBAL b0, vhb, vcb
	GLOBAL g0
	GLOBAL d0
	GLOBAL aS1, aS2, bS
    USEION PKA READ PKAi VALENCE 0
    RANGE mod_pka_g_min, mod_pka_g_max, mod_pka_g_half, mod_pka_g_slope 
    RANGE modulation_factor
}

UNITS {
	(mV) = (millivolt)
	(mA) = (milliamp)
	(S) = (siemens)
}

PARAMETER {
	gbar = 1	(S/cm2)

	a0 = 37		(1/ms)	: alpha
	vha  = 45	(mV)
	vca = 40	(mV)

	b0 = 10		(1/ms)	: beta
	vhb = -50	(mV)
	vcb = -10	(mV)

	g0 = 40		(1/ms)	: gamma

	d0 = 30		(1/ms)	: delta

	aS1 = 0.0025	(1/ms)
	aS2 = 0.0002	(1/ms)
	bS = 0.00017	(1/ms)

	Con = 0.001	(1/ms)
	Coff = 0.1	(1/ms)
	Oon = 1.6	(1/ms)
	Ooff = 0.01	(1/ms)
    mod_pka_g_min = 1 (1)
    mod_pka_g_max = 1 (1)
    mod_pka_g_half = 0.000100 (mM)
    mod_pka_g_slope = 0.01 (mM)
}

ASSIGNED {
	v	(mV)
	ena	(mV)
	g	(S/cm2)
	ina	(mA/cm2)
	alpha	(1/ms)
	beta	(1/ms)
	gamma	(1/ms)
	delta	(1/ms)
	a
    PKAi (mM)
    modulation_factor (1)
}

STATE {
	c1  : closed
	c2
	c3
	c4
	c5
	ct  : total closed
	o   : open
	i1  : fast inactivated
	i2
	i3
	i4
	i5
	i6   
	ift : total fast inactivated
	is1 : slow inactivated
	is2
	ist : total slow inactivated
	it  : total inactivated
}

BREAKPOINT {
     SOLVE kin METHOD sparse
    modulation_factor=modulation(PKAi, mod_pka_g_min, mod_pka_g_max, mod_pka_g_half, mod_pka_g_slope)	   
	   
	g = gbar*o*modulation_factor
	ina = g*(v-ena)
	ct = c1 + c2 + c3 + c4 + c5
	ift = i1 + i2 + i3 + i4 + i5 + i6
	ist = is1 + is2
	it = ift + ist
}

INITIAL {
	SOLVE kin STEADYSTATE sparse
}

KINETIC kin{
	rates(v)

	~ c1 <-> c2 (4*alpha, beta)
	~ c2 <-> c3 (3*alpha, 2*beta)
	~ c3 <-> c4 (2*alpha, 3*beta)
	~ c4 <-> c5 (alpha, 4*beta)
	~ c5 <-> o  (gamma, delta)
	~ o <-> is1 (aS1, bS)

	~ i1 <-> i2 (4*alpha*a, beta/a)
	~ i2 <-> i3 (3*alpha*a, 2*beta/a)
	~ i3 <-> i4 (2*alpha*a, 3*beta/a)
	~ i4 <-> i5 (alpha*a, 4*beta/a)
	~ i5 <-> i6 (gamma, delta)
	~ i6 <-> is2 (aS2, bS)

	~ c1 <-> i1 (Con, Coff)
	~ c2 <-> i2 (Con*a, Coff/a)
	~ c3 <-> i3 (Con*a^2, Coff/a^2)
	~ c4 <-> i4 (Con*a^3, Coff/a^3)
	~ c5 <-> i5 (Con*a^4, Coff/a^4)
	~ o <-> i6  (Oon, Ooff)

	CONSERVE c1+c2+c3+c4+c5+i1+i2+i3+i4+i5+i6+is1+is2+o=1
}

PROCEDURE rates(v(millivolt)) {
	alpha = a0*exp((v-vha)/vca)
	beta = b0*exp((v-vhb)/vcb)
	gamma = g0
	delta = d0

	a = ((Coff/Con)/(Ooff/Oon))^(1/8)
}

FUNCTION modulation(conc (mM), mod_min (1), mod_max (1), mod_half (mM), mod_slope (mM)) (1) {
    : returns modulation factor
    modulation = mod_min + (mod_max-mod_min) / (1 + exp(-(conc - mod_half)/mod_slope))
}
