# Manuscript drafts (Paper 1)

## Radio Science (AGU) draft

| File | Role |
|------|------|
| [`paper1_radioscience.tex`](paper1_radioscience.tex) | Main manuscript |
| [`references.bib`](references.bib) | BibTeX sources (`apacite`) |
| [`paper1_radioscience.pdf`](paper1_radioscience.pdf) | Compiled PDF (AGU `agujournal2025` class) |
| `agujournal2025.cls`, `wiley-macros.tex`, … | Official AGU 2025 template files |
| [`figures/`](figures/) | Manuscript figures |

**Build** (from this folder; AGU 2025 class requires **XeLaTeX** + BibTeX/`apacite`):

```powershell
xelatex -interaction=nonstopmode paper1_radioscience.tex
bibtex paper1_radioscience
xelatex -interaction=nonstopmode paper1_radioscience.tex
xelatex -interaction=nonstopmode paper1_radioscience.tex
```

**Before submission:** fill real author list / affiliations / corresponding address; add Open Research repository DOI; optionally switch `\documentclass` from `draft` to `published` per AGU checklist; run open controls in `../analysis/FREE_SPACE_CONTROL.md` and `../analysis/LOWF_INTERMEDIATE_PLAN.md`.

Supporting analysis: [`../analysis/`](../analysis/) (`ceff_notes.md`, dipole coax tables, circuit overlay, `make_ceff_products.py`).