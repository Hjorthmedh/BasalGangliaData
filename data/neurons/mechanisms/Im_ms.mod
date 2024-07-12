COMMENT
Mechanism taken from Doron et al., 2017
https://senselab.med.yale.edu/ModelDB/ShowModel.cshtml?model=231427&file=/reproduction/Im.mod#tabs-2

Reference :     Adams et al. 1982 - M-currents and other potassium currents in bullfrog sympathetic neurones

corrected rates using q10 = 2.3, target temperature 34, orginal 21


ENDCOMMENT

NEURON	{
	SUFFIX Im_ms
	USEION k READ ek WRITE ik
	RANGE gbar, gIm, ik

    USEION PKA READ PKAci VALENCE 0
    RANGE mod_pka_g_min, mod_pka_g_max, mod_pka_g_half, mod_pka_g_slope 
    RANGE modulation_factor
			      
}

UNITS	{
	(S) = (siemens)
	(mV) = (millivolt)
	(mA) = (milliamp)
}

PARAMETER	{
     gbar = 0.00001 (S/cm2)

    mod_pka_g_min = 1 (1)
    mod_pka_g_max = 1 (1)
    mod_pka_g_half = 0.000100 (mM)
    mod_pka_g_slope = 0.01 (mM)		    
}

ASSIGNED	{
	v	(mV)
	ek	(mV)
	ik	(mA/cm2)
	gIm	(S/cm2)
	mInf
	mTau
	mAlpha
	mBeta
    PKAci (mM)
    modulation_factor (1)
}

STATE	{ 
	m
}

BREAKPOINT	{
     SOLVE states METHOD cnexp
    modulation_factor=modulation(PKAci, mod_pka_g_min, mod_pka_g_max, mod_pka_g_half, mod_pka_g_slope)	   
	   
	gIm = gbar*m*modulation_factor
	ik = gIm*(v-ek)
}

DERIVATIVE states	{
	rates()
	m' = (mInf-m)/mTau
}

INITIAL{
	rates()
	m = mInf
}

PROCEDURE rates(){
  LOCAL qt
  qt = 2.3^((34-21)/10)

	UNITSOFF
		mAlpha = 3.3e-3*exp(2.5*0.04*(v - -35))
		mBeta = 3.3e-3*exp(-2.5*0.04*(v - -35))
		mInf = mAlpha/(mAlpha + mBeta)
		mTau = (1/(mAlpha + mBeta))/qt
	UNITSON
}

FUNCTION modulation(conc (mM), mod_min (1), mod_max (1), mod_half (mM), mod_slope (mM)) (1) {
    : returns modulation factor
    modulation = mod_min + (mod_max-mod_min) / (1 + exp(-(conc - mod_half)/mod_slope))
}
