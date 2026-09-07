# Paper 2 — Plan checklist

Last updated: 2026-09-07

## Design (before coding)

- [ ] Choose \(r_s(t)\) law: simple sinusoid vs Song \(r_s^2 = r_{s0}^2 + \Re\{ja^2 e^{j\omega t}\}\) analogue
- [ ] Define discrete update: recompute distance field vs radial threshold only
- [ ] Diagnostics list: feed \(V,I,Z\); optional probe \(E\) outside max sheath; cycle-averaged power
- [ ] Write `design/rs_t_spec.md`

## Implementation

- [ ] Feature flag for time-varying sheath mask in plasma/sheath module
- [ ] Regression: static \(S_d\) still bit-matches Paper 1 when \(\Delta r=0\)
- [ ] Single-tone pilot script under `../scripts/` (or paper-local)

## Analysis / manuscript

- [ ] Static vs oscillating comparison figure
- [ ] \(\Delta r\) scan
- [ ] Discussion: what kinematic model can and cannot claim vs Song/Tu
- [ ] `draft/outline.md`
