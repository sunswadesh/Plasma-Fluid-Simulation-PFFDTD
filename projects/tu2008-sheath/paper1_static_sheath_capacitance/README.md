# Paper 1 — Static sheath capacitance

**Working title.** *Emergent series loading of a plasma-immersed dipole by a prescribed vacuum jacket in 3D fluid FDTD.*

**Status:** Radio Science draft revised for senior-scientist review (dipole coax, circuit overlay, band-limited loading claim, completed methods). Free-space CW and low-\(f\) for \(S_d=4,6,8\) remain open controls.  
**Guide:** [`../PROJECT_GUIDE.md`](../PROJECT_GUIDE.md)  
**Draft PDF:** [`draft/paper1_radioscience.pdf`](draft/paper1_radioscience.pdf)

---

## Science question

Does a **prescribed volumetric vacuum jacket** of width \(S_d\Delta x\) in PF-FDTD load a plasma-immersed dipole as an emergent **series** gap, and how does that loading compare with a **dipole** coaxial estimate?

This is the **quasi-static bridge**: sampling different sheath thicknesses without claiming oscillating-boundary or PIC fidelity.

## Observables (success metrics)

| Metric | Target |
|--------|--------|
| Dense-band \(\mathrm{Im}\{Z\}(S_d)\) below \(f_p\) | Monotonic capacitive loading |
| Near-\(f_p\) behavior | Report ordering reversal honestly |
| Dipole coax comparison | \(C_\mathrm{sh}^\mathrm{(dip)}=C_\mathrm{mono}/4\); order-unity ratio |
| Circuit overlay | Show where \(Z_0+1/(j\omega C)\) fails (\(\mathrm{Re}\{Z\}\)) |
| Free-space \(f_\mathrm{res}\) | Open upper anchor |
| Multi-marker \(Z(f)\) | Report Im-zero **and** \|Z\|; do not equate them |

**Not a success metric:** Im-zero climbing with \(S_d\); monopole “scale factor 0.3”.

## Folder layout

```text
paper1_static_sheath_capacitance/
├── README.md
├── PLAN.md
├── analysis/          ← tables/figures (C_eff, ImZ, circuit overlay)
└── draft/             ← Radio Science manuscript
```

## Depends on / feeds

- **Depends on:** Phases 4–8 (coupling + CW).  
- **Feeds:** Paper 2 (trusted static baseline before moving \(r_s\)).
