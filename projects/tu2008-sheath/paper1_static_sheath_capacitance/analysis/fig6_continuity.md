# Figure 6 continuity (combined 0.50–2.30 MHz)

**Script:** `check_fig6_continuity.py`  
**Date:** 2026-09-20

## Campaign stitch

Low-\(f\) (`cw_lowf_summary.txt`) and dense (`cw_tu_summary.txt`) share all \((S_d,f)\) cells at \(f\ge 1.50\,\mathrm{MHz}\) for \(S_d=0,2,10\). Relative difference is **0** (same phasors copied into the low-\(f\) table). The stitch is not an independent re-measurement.

## Join behavior

| \(S_d\) | Join | Notes |
|--------:|------|-------|
| 0 | \(1.40\to 1.60\,\mathrm{MHz}\) gap | Incomplete `sd0_f1500000` restart omitted (Re≈2.1 kΩ outlier). Rising inductive trend continuous across gap (\(\|\Delta Z\|/\|Z\|\approx 0.36\) over 200 kHz). |
| 2 | \(1.40\to 1.50\to 1.60\) | Smooth: rel ≈ 0.11, 0.17 |
| 10 | \(1.40\to 1.50\to 1.60\) | Smooth: rel ≈ 0.12, 0.10 |

## Large jumps that are *not* stitch artifacts

- \(S_d=2\) near 0.50–0.80 MHz: inductive island / approach to provisional \(f_\mathrm{res}\).
- \(S_d=0,2\) near \(f_p\): plasma-resonance swing.

## Verdict

Figure 6 is continuous across the campaign join for \(S_d=2,10\). \(S_d=0\) has a documented missing tone at 1.50 MHz but no discontinuous jump in the retained neighbors.
