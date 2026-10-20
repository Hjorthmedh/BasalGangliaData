## FS–FS chemical synapses

Cortical control of striatal fast-spiking interneuron synchrony, 2022  
Paige N. McKeon, Garrett W. Bunce, Mary H. Patton, Rong Chen and Brian N. Mathur  
https://physoc.onlinelibrary.wiley.com/doi/10.1113/JP282850

No chemical synapses between FS-FS

---

# Striatum Connectivity Parameters

## SPN–SPN GABA failure rate

**Source:** Taverna et al. (2008), Figure 2C  
**Parameter:** `failRate` in `striatum-connectivity.json`  
**Value:** 0.50 (all four SPN→SPN connections)

Failure rates were digitized from Fig. 2C using ddigitize and pooled across
all 27 observations (D1→D1, D1→D2, D2→D1, D2→D2). The per-group means ranged
from 34% to 61%, but were not significantly different individually or when 
compared by presynaptic cell type (dSPN: 59%, N=10; iSPN: 44%, N=17; Welch 
t-test p≈0.18), supporting use of the fully pooled mean (49.6%, rounded to 0.50).

| Connection | N  | Mean (%) | SD (%) | Median (%) |
|------------|----|----------|--------|------------|
| D1→D1      |  7 |    61.09 |  19.63 |      68.77 |
| D1→D2      |  3 |    54.14 |  48.44 |      67.30 |
| D2→D1      |  6 |    34.07 |  25.49 |      29.53 |
| D2→D2      | 11 |    49.61 |  23.35 |      54.06 |
| **Pooled** | 27 |    49.63 |  26.41 |      54.06 |

> Note: digitized point counts do not always match the sample sizes reported in
> the article (D1→D1: N=7 digitized vs. n=8 reported; D2→D2: N=11 vs. n=10).
> Per-group medians match the paper values. Values are based on the digitized
> figure, not raw source data.

**Extracted data files:**
- `Taverna2008_fig2C_failure_rate.png` — digitized figure
- `Taverna2008_fig2C_fr.json` — raw digitized data points (ddigitize format)
