"""Check Figure 6 (combined Z) continuity across frequencies and campaign join."""
from __future__ import annotations

from pathlib import Path

p = Path(__file__).resolve().parent / "data" / "ceff_vs_frequency.txt"
rows = []
for line in p.read_text(encoding="utf-8").splitlines():
    if line.startswith("#") or not line.strip() or line.startswith("Sd"):
        continue
    parts = line.split()
    sd = int(float(parts[0]))
    fr = float(parts[1])
    re = float(parts[2])
    im = float(parts[3])
    az = float(parts[4])
    rows.append((sd, fr, re, im, az))

print("=== Join region (1.3-1.7 MHz) ===")
print(f"{'Sd':>3} {'f_MHz':>7} {'Re':>12} {'Im':>12} {'Abs':>12}")
for sd in (0, 2, 10):
    for r in rows:
        if r[0] == sd and 1.3e6 <= r[1] <= 1.7e6:
            print(f"{r[0]:3d} {r[1]/1e6:7.3f} {r[2]:12.1f} {r[3]:12.1f} {r[4]:12.1f}")
    print()

print("=== Points at 1.50 MHz (campaign overlap / omission) ===")
for sd in (0, 2, 10):
    pts = [r for r in rows if r[0] == sd and abs(r[1] - 1.5e6) < 1]
    print(f"Sd={sd}: {len(pts)} point(s) -> {pts}")

print()
print("=== Adjacent-step relative jumps |dZ|/|Z_prev| ===")
for sd in (0, 2, 10):
    pts = sorted([r for r in rows if r[0] == sd], key=lambda x: x[1])
    print(f"--- Sd={sd} ---")
    for i in range(1, len(pts)):
        f0, f1 = pts[i - 1][1], pts[i][1]
        z0 = complex(pts[i - 1][2], pts[i - 1][3])
        z1 = complex(pts[i][2], pts[i][3])
        dz = abs(z1 - z0)
        az = abs(z0) if abs(z0) > 1 else 1.0
        rel = dz / az
        mark = " ***" if rel > 0.5 else (" *" if rel > 0.25 else "")
        join = ""
        if (f0 < 1.5e6 <= f1) or abs(f0 - 1.5e6) < 1 or abs(f1 - 1.5e6) < 1:
            join = " [JOIN]"
        print(
            f"  {f0/1e6:.3f}->{f1/1e6:.3f}: "
            f"dRe={z1.real-z0.real:+8.0f} dIm={z1.imag-z0.imag:+8.0f} "
            f"rel={rel:5.2f}{mark}{join}"
        )

print()
print("=== Gap sizes (missing tones) ===")
for sd in (0, 2, 10):
    pts = sorted([r for r in rows if r[0] == sd], key=lambda x: x[1])
    for i in range(1, len(pts)):
        df = pts[i][1] - pts[i - 1][1]
        if df > 150000:  # larger than normal 100 kHz step
            print(f"Sd={sd}: gap {pts[i-1][1]/1e6:.3f} -> {pts[i][1]/1e6:.3f} MHz (df={df/1e3:.0f} kHz)")
