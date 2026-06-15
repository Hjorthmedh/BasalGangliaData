# TH (Tyrosine Hydroxylase Positive) Neurons

## Model

The active model is `md_20171011_cell_1_2_ChIN_TH`, containing 25 parameter sets from a BluePyOpt optimisation. This replaces the older `cell1` model (6 parameter sets, different channel configuration). The new target model is optimized with bpo while the old was not. The new target/model does not go into depolarization block as easily as the old target/model.
