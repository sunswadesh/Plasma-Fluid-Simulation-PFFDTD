# Paper 2 — Plan checklist

Last updated: 2026-09-23

**Science rationale (expanded):** [`SCIENCE.md`](SCIENCE.md) — outstanding issues, literature posture, and forward work.  
**Program rule:** Chase changing-vs-static sheath physics; do **not** treat Song/Tu numerical reproduction as the scoreboard.

---

## Design (before coding)

- [x] Choose \(r_s(t)\) law: sinusoid first
- [x] Discrete update: soft-edge default; hard staircase retained
- [x] Diagnostics list
- [x] Write `design/rs_t_spec.md`
- [x] Write `SCIENCE.md` (issues + forward plan)

## Implementation

- [x] Feature flag / \(\Delta r>0\) oscillating path
- [x] Static path when \(\Delta r=0\)
- [x] Soft-edge \(N_0\) blend (`SheathSoftEdge`, CLI argv[15])
- [x] Pilot + \(\Delta r\) scan scripts

## Analysis done

- [x] Hard pilot: static vs oscillating
- [x] Soft-edge re-test; hard-vs-soft note
- [x] Soft \(\Delta r\) scan (non-monotonic; documented)
- [x] Radio Science draft Results (hard + soft); **framing rewrite still open**

## Forward work (from SCIENCE.md §3, §5)

### Manuscript

- [ ] Reframe draft: dynamic vs static loading; Song/Tu as motivation only ([`SCIENCE.md` §3.5](SCIENCE.md))

### Numerics / \(\Delta r\)

- [ ] Soft-edge sensitivity at fixed \(\Delta r=1\) (0.5 / 1 / 2 cell edge)
- [ ] Revisit \(\Delta r\) with matched soft policy (\(\mathrm{soft}\propto\Delta r\) or fixed fraction); prefer absolute \(\Delta Z\) plots over rel-to-bracket alone

### Physics scans

- [ ] Sparse frequency set (2–3 tones, soft \(\Delta r=1\) + brackets) — not a full Paper 1 grid
- [ ] Phase scan \(\phi\) at 700 kHz
- [ ] Cleaner diagnostics: harmonics of \(I\), cycle-averaged power; optional exterior \(E\) probe

### Optional stronger nulls

- [ ] Frozen-\(r_s\) snapshots vs true osc
- [ ] Time-averaged / effective-radius static null

## Explicit non-goals (Paper 2)

- Matching Song analytic reactance or Tu PIC to a percent target
- Self-consistent charging / PIC (Paper 3)
- Claiming “kinetic electron-free ion sheath” for the density-floor hole
