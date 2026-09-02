# Low-frequency CW sweep: 0.5–1.5 MHz, Sd=0,2,10 (Tu f_res search below 1.5 MHz).
# Results: <repo-root>/results/sheath_cw_tu/
# Tuned for 4-core / 8-thread workstation: MaxParallel=2, OmpThreads=4.

param(
  [int[]]$SheathWidths = @(0, 2, 10),
  [int[]]$FrequenciesHz = @(
    500000, 600000, 700000, 800000, 900000, 1000000, 1100000,
    1200000, 1300000, 1400000, 1500000
  ),
  [int]$MaxParallel = 2,
  [int]$OmpThreads = 4,
  [switch]$SkipCompleted
)

$params = @{
  SheathWidths   = $SheathWidths
  FrequenciesHz  = $FrequenciesHz
  Fp             = 2000000
  MaxParallel    = $MaxParallel
  OmpThreads     = $OmpThreads
}
if ($SkipCompleted) { $params.SkipCompleted = $true }

& "$PSScriptRoot\run_sheath_cw_tu.ps1" @params
