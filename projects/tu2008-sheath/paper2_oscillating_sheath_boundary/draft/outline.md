# Paper 2 — Radio Science manuscript outline

**Target journal:** *Radio Science* (AGU)  
**Working title:** Kinematic Oscillating Sheath Boundary in Three-Dimensional Plasma Fluid FDTD: Isolating Song’s Moving-Boundary Coupling Without PIC  
**Draft file:** [`manuscript.tex`](manuscript.tex)  
**Status:** Skeleton with science framing; figures/results TBD after pilot.

---

## Intended section map (AGU order)

1. **Title / authors / affiliations**
2. **Key Points** (≤3, ≤140 chars, no jargon symbols if possible)
3. **Abstract** (<250 words)
4. **Plain Language Summary** (<200 words)
5. **Keywords**
6. **1. Introduction** — antenna–sheath loading; Song \(\dot{r}_s\); gap between static jackets and PIC; Paper 1 series-\(C\) context
7. **2. Model and Methods**
   - 2.1 PF-FDTD Maxwell–fluid core
   - 2.2 Kinematic \(r_s(t)\) mask (this work)
   - 2.3 Diagnostics: feed \(Z\), controls (static brackets)
8. **3. Results** — static vs oscillating; \(\Delta r\) scan (placeholder)
9. **4. Discussion** — what kinematics can/cannot claim vs Song/Tu; Paper 3 gate
10. **5. Conclusions**
11. **Acknowledgments**
12. **Open Research**
13. **References**
14. **Figures / Tables**

## Figures planned

| Fig | Content |
|-----|---------|
| 1 | Geometry + staircased \(r_s(t)\) schematic |
| 2 | Static vs oscillating feed \(Z\) (or \(V,I\) phasors) at pilot tone |
| 3 | \(\Delta r\) amplitude scan |
| 4 | Optional: cycle-averaged power / phase vs Song sketch |

## Build

Requires AGU class `agujournal2019` (or `agujournal2025`) from [AGU LaTeX templates](https://www.agu.org/publications/authors/journals/submission-checklists). Place `.cls` / `.bst` beside `manuscript.tex`, then:

```bash
pdflatex manuscript
bibtex manuscript
pdflatex manuscript
pdflatex manuscript
```

Until the class is installed, the `.tex` still documents structure and draft prose.
