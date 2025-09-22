TITLE non conducting non-channel

COMMENT
 Usage: 
 insert this channel to all sections 
 to make sure they have the three major ions
 (this way one can set the reversal potential of an ion
  in all sections without checking if the ion is precent)
ENDCOMMENT

UNITS {}

NEURON {
 SUFFIX nonconducting_k_na_ca
 USEION na WRITE ina
 USEION k WRITE ik
 USEION ca WRITE ica VALENCE 2
}

PARAMETER {
 ik = 0
 ina = 0
 ica = 0
}

STATE {}

ASSIGNED {}

BREAKPOINT {}
