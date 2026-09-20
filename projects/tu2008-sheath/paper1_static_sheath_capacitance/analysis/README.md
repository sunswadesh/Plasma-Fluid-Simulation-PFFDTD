# Paper 1 analysis products

| Path | Content |
|------|---------|
| [`data/ceff_vs_frequency.txt`](data/ceff_vs_frequency.txt) | Per-frequency \(Z\) and diagnostic \(C_\mathrm{eff}\) |
| [`data/ceff_vs_coax_summary.txt`](data/ceff_vs_coax_summary.txt) | Low-\(f\) \(C_\mathrm{eff}\) vs monopole and **dipole** coax |
| [`data/imz_vs_sd.txt`](data/imz_vs_sd.txt) | Primary loading evidence: \(\mathrm{Im}\{Z\}(S_d)\) at fixed \(f\) |
| [`data/circuit_overlay_1600kHz.txt`](data/circuit_overlay_1600kHz.txt) | \(Z(S_d=0)+1/(j\omega C_\mathrm{dip})\) residuals |
| [`data/fres_summary.txt`](data/fres_summary.txt) | Resonance markers, including upper limits |
| [`figures/`](figures/) | Publication figures (copied to `../draft/figures/`) |
| [`ceff_notes.md`](ceff_notes.md) | Method notes after review revision |
| [`FREE_SPACE_CONTROL.md`](FREE_SPACE_CONTROL.md) | Open free-space CW plan |
| [`LOWF_INTERMEDIATE_PLAN.md`](LOWF_INTERMEDIATE_PLAN.md) | Open low-\(f\) plan for \(S_d=4,6,8\) and dense \(S_d=2\) |
| [`fig6_continuity.md`](fig6_continuity.md) | Combined-band stitch check (low-\(f\) ↔ dense) |
| [`check_fig6_continuity.py`](check_fig6_continuity.py) | Continuity diagnostics |
| [`make_ceff_products.py`](make_ceff_products.py) | Regenerator |

```powershell
python projects/tu2008-sheath/paper1_static_sheath_capacitance/analysis/make_ceff_products.py
```
(run from the repo root)
