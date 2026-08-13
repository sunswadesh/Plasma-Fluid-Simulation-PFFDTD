# Overnight runner: incomplete + missing cases from default 2D sheath sweep.
# Cases: sd4_f300000 (redo) + Sd=6,8,10 x {100,150,200,300} kHz

param(
  [int]$VcRate = 10,
  [int]$MaxIter = 100000,
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

$outbase = Join-Path $root 'results\sheath_2d_sweep'
if (-not (Test-Path $outbase)) {
  New-Item -ItemType Directory -Path $outbase -Force | Out-Null
}

$cases = @(
  @{ Sd = 4;  F = 300000 },
  @{ Sd = 6;  F = 100000 },
  @{ Sd = 6;  F = 150000 },
  @{ Sd = 6;  F = 200000 },
  @{ Sd = 6;  F = 300000 },
  @{ Sd = 8;  F = 100000 },
  @{ Sd = 8;  F = 150000 },
  @{ Sd = 8;  F = 200000 },
  @{ Sd = 8;  F = 300000 },
  @{ Sd = 10; F = 100000 },
  @{ Sd = 10; F = 150000 },
  @{ Sd = 10; F = 200000 },
  @{ Sd = 10; F = 300000 }
)

$masterLog = Join-Path $outbase 'remaining_overnight.log'
$startAll = Get-Date
"[$($startAll.ToString('s'))] Starting remaining 2D sweep: $($cases.Count) cases" | Tee-Object -FilePath $masterLog
"Executable: $exepath" | Tee-Object -FilePath $masterLog -Append
"VcRate=$VcRate MaxIter=$MaxIter T=$T FREQ_PLASMA=2000000" | Tee-Object -FilePath $masterLog -Append

$idx = 0
foreach ($case in $cases) {
  $idx++
  $Sd = $case.Sd
  $f = $case.F
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
  "[$($t0.ToString('s'))] ($idx/$($cases.Count)) START Sd=$Sd f=$f Hz" | Tee-Object -FilePath $masterLog -Append

  & $exepath (Join-Path $outdir "temp_f${f}") $outfile 2000000 0.1 0 0 0 $T $Sd $VcRate $MaxIter > $logfile 2>&1
  $code = $LASTEXITCODE
  $t1 = Get-Date
  $mins = [math]::Round(($t1 - $t0).TotalMinutes, 1)

  if ($code -ne 0) {
    "[$($t1.ToString('s'))] ($idx/$($cases.Count)) ERROR Sd=$Sd f=$f exit=$code after ${mins} min" | Tee-Object -FilePath $masterLog -Append
  } else {
    "[$($t1.ToString('s'))] ($idx/$($cases.Count)) DONE  Sd=$Sd f=$f in ${mins} min" | Tee-Object -FilePath $masterLog -Append
  }
}

$endAll = Get-Date
$totalHrs = [math]::Round(($endAll - $startAll).TotalHours, 2)
"[$($endAll.ToString('s'))] Remaining 2D sweep complete in $totalHrs hours" | Tee-Object -FilePath $masterLog -Append
