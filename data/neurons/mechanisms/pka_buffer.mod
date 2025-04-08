TITLE PKAc placeholder for bath

NEURON {
	SUFFIX pka_buffer
	USEION PKAc WRITE PKAci VALENCE 0
	RANGE baseline
}

UNITS {
	(molar) = (1/liter)
	(mM) = (millimolar)
}

PARAMETER {
	baseline = 3.6e-6 (mM)
}

STATE { PKAci (mM) }

INITIAL { 
	PKAci = baseline 
}

BREAKPOINT {
	PKAci = baseline
}

COMMENT

This is a placeholder that sets PKAc to a default value that can be read by the other ion channel models.


ENDCOMMENT