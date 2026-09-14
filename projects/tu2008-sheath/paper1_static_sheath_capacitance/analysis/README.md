# Paper 1 analysis products

| Path | Content |
|------|---------|
| [`data/ceff_vs_frequency.txt`](data/ceff_vs_frequency.txt) | Per-frequency \(Z\) and \(C_\mathrm{eff}\) (all \(S_d\)) |
| [`data/ceff_vs_coax_summary.txt`](data/ceff_vs_coax_summary.txt) | Low-\(f\) and dense-band means vs coax |
| [`data/fres_summary.txt`](data/fres_summary.txt) | Resonance markers, including upper limits for \(S_d=4,6,8\) |
| [`figures/`](figures/) | Publication figures (copied to `../draft/figures/`) |
| [`ceff_notes.md`](ceff_notes.md) | Method notes, including why the low-\(f\) grid is only \(S_d=0,2,10\) |
| [`make_ceff_products.py`](make_ceff_products.py) | Regenerator |

```powershell
python projects/tu2008-sheath/paper1_static_sheath_capacitance/analysis/make_ceff_products.py
```
(run from the repo root)
