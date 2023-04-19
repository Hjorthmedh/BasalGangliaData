dopamine = dict(kas_ms={"somatic": [0.65, 0.85],
                        "basal": [0.65, 0.85]}, kaf_ms={"somatic": [0.75, 0.85],
                                                        "basal": [0.75, 0.85]}, can_ms={"somatic": [0.2, 1]})
dopamine = dict(ion_channel=dict(soma=["kas_ms", "kaf_ms", "can_ms"],
                                 dendrite=["kas_ms", "kaf_ms"]),
                receptor=dict(tmGabaA={"maxMod": 0.8}),
                external_input=dict(tmGlut={"maxMod_AMPA": 1.2,
                                            "maxMod_NMDA": 1.3,
                                            "failRate": 0.7}))

acetylcholine = dict(naf_ms={"all": [1, 1.2]},
                     kaf_ms={"somatic": [-10, 0], "basal": [-10, 0]},
                     kir_ms={"somatic": [0.8, 1], "basal": [0.8, 1]},
                     cal12_ms={"somatic": [0.3, 0.7], "basal": [0.3, 0.7]},
                     cal13_ms={"somatic": [0.3, 0.7], "basal": [0.3, 0.7]},
                     can_ms={"somatic": [0.65, 0.85]},
                     Im_ms={"axonal": [0, 0.4]})
