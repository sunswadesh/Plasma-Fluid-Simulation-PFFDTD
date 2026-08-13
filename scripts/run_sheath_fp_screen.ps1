# Screening sweep near electron plasma frequency (Tu/Miyake band).
# 2 sheath widths x 10 source frequencies = 20 runs.
# Frequencies are 0.3..1.5 x Fp with per-run MaxIter sized for >=15 drive cycles.

param(
  [int[]]$SheathWidths = @(0, 10),
  [double]$Fp = 2000000,
  [double[]]$FpRatios = @(0.3, 0.5, 0.7, 0.85, 0.95, 1.0, 1.05, 1.1, 1.2, 1.5),
  [int]$VcRate = 10,
  [int]$MinIter = 100000,
  [int]$MinDriveCycles = 15,
  [double]$Dt = 6.671114e-11,
  [int]$T = 100
)

$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$exepath = Join-Path $root 'build\pffdtd_parallel.exe'
if (-not (Test-Path $exepath)) {
  $exepath = Join-Path $root 'pffdtd_parallel.exe'
}
if (-not (Test-Path $exepath)) {
  throw 'pffdtd_parallel.exe not found in root or build folder'
}

$strTemplate = Join-Path $root 'sheath_sine.str'
if (-not (Test-Path $strTemplate)) {
  throw "Missing template: $strTemplate"
}

$outbase = Join-Path $root 'results\sheath_fp_screen'
if (-not (Test-Path $outbase)) {
  New-Item -ItemType Directory -Path $outbase -Force | Out-Null
}

function Get-MaxIterForFrequency {
  param(
    [double]$Frequency,
    [double]$Dt,
    [int]$MinDriveCycles,
    [int]$MinIter
  )
  if ($Frequency -le 0 -or $Dt -le 0) {
    return $MinIter
  }
  $needed = [math]::Ceiling($MinDriveCycles / ($Frequency * $Dt))
  $iter = [math]::Max($MinIter, $needed)
  # Round up to 10k steps for stable runtimes
  return [int]([math]::Ceiling($iter / 10000.0) * 10000)
}

$cases = @()
foreach ($ratio in $FpRatios) {
  $f = [int][math]::Round($Fp * $ratio)
  $maxIter = Get-MaxIterForFrequency -Frequency $f -Dt $Dt -MinDriveCycles $MinDriveCycles -MinIter $MinIter
  foreach ($sd in $SheathWidths) {
    $cases += [PSCustomObject]@{
      Sd      = $sd
      F       = $f
      Ratio   = $ratio
      MaxIter = $maxIter
    }
  }
}

$masterLog = Join-Path $outbase 'screen.log'
$planFile = Join-Path $outbase 'run_plan.tsv'
$startAll = Get-Date

"[$($startAll.ToString('s'))] Starting fp screening sweep: $($cases.Count) cases" | Tee-Object -FilePath $masterLog
"Executable: $exepath" | Tee-Object -FilePath $masterLog -Append
"Fp=$Fp Hz  VcRate=$VcRate  MinIter=$MinIter  MinDriveCycles=$MinDriveCycles  dt=$Dt" | Tee-Object -FilePath $masterLog -Append

"Sd`tFreq_Hz`tRatio_fp`tMaxIter" | Set-Content $planFile
foreach ($case in $cases) {
  "$($case.Sd)`t$($case.F)`t$($case.Ratio)`t$($case.MaxIter)" | Add-Content $planFile
}

$idx = 0
foreach ($case in $cases) {
  $idx++
  $Sd = $case.Sd
  $f = $case.F
  $maxIter = $case.MaxIter
  $ratio = $case.Ratio

  $outdir = Join-Path $outbase "sd${Sd}_f${f}"
  if (-not (Test-Path $outdir)) {
    New-Item -ItemType Directory -Path $outdir -Force | Out-Null
  }

  $outfile = Join-Path $outdir 'data'
  $logfile = Join-Path $outdir 'simulation.log'
  $tempStr = Join-Path $outdir "temp_f${f}.str"

  $strContent = Get-Content $strTemplate
  for ($i = 0; $i -lt $strContent.Length; $i++) {
    if ($strContent[$i] -match '^35\s+35\s+33\s+3\s+1\s+\d+') {
      $strContent[$i] = "35`t35`t33`t3`t1`t$f"
    }
  }
  Set-Content $tempStr $strContent

  $t0 = Get-Date
  $cycles = [math]::Round($maxIter * $Dt * $f, 1)
  "[$($t0.ToString('s'))] ($idx/$($cases.Count)) START Sd=$Sd f=$f Hz ($ratio fp) MaxIter=$maxIter (~$cycles drive cycles)" |
    Tee-Object -FilePath $masterLog -Append

  & $exepath (Join-Path $outdir "temp_f${f}") $outfile $Fp 0.1 0 0 0 $T $Sd $VcRate $maxIter > $logfile 2>&1
  $code = $LASTEXITCODE
  $t1 = Get-Date
  $mins = [math]::Round(($t1 - $t0).TotalMinutes, 1)

  if ($code -ne 0) {
    "[$($t1.ToString('s'))] ($idx/$($cases.Count)) ERROR Sd=$Sd f=$f exit=$code after ${mins} min" |
      Tee-Object -FilePath $masterLog -Append
  } else {
    "[$($t1.ToString('s'))] ($idx/$($cases.Count)) DONE  Sd=$Sd f=$f in ${mins} min" |
      Tee-Object -FilePath $masterLog -Append
  }
}

$endAll = Get-Date
$totalHrs = [math]::Round(($endAll - $startAll).TotalHours, 2)
"[$($endAll.ToString('s'))] fp screening sweep complete in $totalHrs hours" | Tee-Object -FilePath $masterLog -Append
