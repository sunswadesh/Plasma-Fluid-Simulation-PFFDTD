# Paper 2 — Plan checklist

Last updated: 2026-09-22

## Design (before coding)

- [x] Choose \(r_s(t)\) law: sinusoid first
- [x] Discrete update: soft-edge default; hard staircase retained
- [x] Diagnostics list
- [x] Write `design/rs_t_spec.md`

## Implementation

- [x] Feature flag / \(\Delta r>0\) oscillating path
- [x] Static path when \(\Delta r=0\)
- [x] Soft-edge \(N_0\) blend (`SheathSoftEdge`, CLI argv[15])
- [x] Pilot scripts

## Analysis / manuscript

- [x] Hard pilot: static vs oscillating figures
- [x] Soft-edge re-test; hard-vs-soft note
- [ ] \(\Delta r\) scan (soft)
- [ ] Phase scan
- [x] Discussion caveats vs Song/Tu
- [x] Radio Science draft Results updated (hard + soft)
