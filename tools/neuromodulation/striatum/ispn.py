dopamine = dict(
    ion_channel=dict(soma=["naf_ms", "kas_ms", "kaf_ms", "kir_ms", "cal12_ms", "cal13_ms", "can_ms", "car_ms"],
                     dendrite=["naf_ms", "kas_ms", "kaf_ms", "kir_ms", "cal12_ms", "cal13_ms", "can_ms", "car_ms"],
                     axon=["naf_ms", "kas_ms"]),
    receptor=dict(tmGabaA={"maxMod": 0.99}),
    external_input=dict(tmGlut={"maxMod_AMPA": 0.95,
                                "maxMod_NMDA": 0.8,
                                "failRate": 1.3}))
