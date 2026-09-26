# Paper 2 — Plan checklist

Last updated: 2026-09-25

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
- [x] Soft-edge width sensitivity (0.5 / 1 / 2); out-of-bracket survives
- [x] Sparse frequency set (500 / 700 / 1200 kHz); out-of-bracket at 3/3
- [x] Phase scan \(\phi\) at 700 kHz (\(\arg Z\) span \(\sim 72^\circ\); coherent)
- [x] Matched soft \(\Delta r\) (\(\mathrm{soft}=\Delta r\)); out-of-bracket 4/4, still non-monotonic
- [x] Radio Science draft Results (through matched \(\Delta r\)); framing rewrite done

## Forward work (from SCIENCE.md §3, §5)

### Manuscript

- [x] Reframe draft: dynamic vs static loading; Song/Tu as motivation only

### Numerics / \(\Delta r\)

- [x] Soft-edge sensitivity at fixed \(\Delta r=1\) (0.5 / 1 / 2 cell edge)
- [x] Revisit \(\Delta r\) with matched soft policy (\(\mathrm{soft}\propto\Delta r\))

### Physics scans

- [x] Sparse frequency set (2–3 tones, soft \(\Delta r=1\) + brackets)
- [x] Phase scan \(\phi\) at 700 kHz
- [x] Cleaner diagnostics: harmonics of \(I\) (phase campaign); cycle-averaged power / exterior \(E\) still open

### Optional stronger nulls

- [ ] Frozen-\(r_s\) snapshots vs true osc
- [ ] Time-averaged / effective-radius static null

## Explicit non-goals (Paper 2)

- Matching Song analytic reactance or Tu PIC to a percent target
- Self-consistent charging / PIC (Paper 3)
- Claiming “kinetic electron-free ion sheath” for the density-floor hole
