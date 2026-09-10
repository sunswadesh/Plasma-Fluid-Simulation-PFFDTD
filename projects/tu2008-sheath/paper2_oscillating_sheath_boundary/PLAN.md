# Paper 2 — Plan checklist

Last updated: 2026-09-10

## Design (before coding)

- [x] Choose \(r_s(t)\) law: simple sinusoid vs Song \(r_s^2 = r_{s0}^2 + \Re\{ja^2 e^{j\omega t}\}\) analogue → **sinusoid first**
- [x] Define discrete update: recompute distance field vs radial threshold only → **threshold on cached PEC distance**
- [x] Diagnostics list: feed \(V,I,Z\); optional probe \(E\) outside max sheath; cycle-averaged power
- [x] Write `design/rs_t_spec.md`

## Implementation

- [x] Feature flag for time-varying sheath mask in plasma/sheath module (`SheathOscEnable` / \(\Delta r>0\))
- [x] Regression path: static \(S_d\) when \(\Delta r=0\) still uses `ApplySheath()` only
- [x] Single-tone pilot script under `../scripts/run_paper2_rs_t_pilot.ps1`

## Analysis / manuscript

- [x] Static vs oscillating comparison figure
- [ ] \(\Delta r\) scan
- [x] Discussion: what kinematic model can and cannot claim vs Song/Tu (staircasing caveat)
- [x] `draft/outline.md`
- [x] Radio Science AGU-format `draft/manuscript.tex` updated with pilot results
- [x] Analyzer `../scripts/analyze_paper2_pilot.py` + `analysis/pilot_findings.md`
