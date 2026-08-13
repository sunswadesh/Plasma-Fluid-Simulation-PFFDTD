# Parallel fp screening sweep (Tu/Miyake band).
# Uses Start-Process with per-case working directories (avoids Start-Job path issues).

param(
  [int[]]$SheathWidths = @(0, 10),
  [double]$Fp = 2000000,
  [double[]]$FpRatios = @(0.3, 0.5, 0.7, 0.85, 0.95, 1.0, 1.05, 1.1, 1.2, 1.5),
  [int]$VcRate = 10,
  [int]$MinIter = 100000,
  [int]$MinDriveCycles = 15,
  [double]$Dt = 6.671114e-11,
  [int]$T = 100,
  [int]$MaxParallel = 4,
  [int]$LogicalCores = 0,
  [switch]$SkipCompleted
)

$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if ($LogicalCores -le 0) {
  $LogicalCores = [int]$env:NUMBER_OF_PROCESSORS
  if ($LogicalCores -le 0) { $LogicalCores = 8 }
}
if ($MaxParallel -lt 1) { $MaxParallel = 1 }
if ($MaxParallel -gt $LogicalCores) { $MaxParallel = $LogicalCores }

$OmpThreads = [math]::Max(1, [int][math]::Floor($LogicalCores / $MaxParallel))

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
  if ($Frequency -le 0 -or $Dt -le 0) { return $MinIter }
  $needed = [math]::Ceiling($MinDriveCycles / ($Frequency * $Dt))
  $iter = [math]::Max($MinIter, $needed)
  return [int]([math]::Ceiling($iter / 10000.0) * 10000)
}

function Test-CaseComplete {
  param([string]$OutDir)
  $vc = Join-Path $OutDir 'data.vc'
  $log = Join-Path $OutDir 'simulation.log'
  if (-not (Test-Path $vc)) { return $false }
  if ((Get-Item $vc).Length -lt 300000) { return $false }
  if (-not (Test-Path $log)) { return $false }
  return (Select-String -Path $log -Pattern 'Elapsed Time' -Quiet)
}

function Prepare-CaseInput {
  param(
    [string]$OutDir,
    [string]$StrTemplate,
    [int]$F
  )
  if (-not (Test-Path $OutDir)) {
    New-Item -ItemType Directory -Path $OutDir -Force | Out-Null
  }
  $tempStr = Join-Path $OutDir "temp_f${F}.str"
  $strContent = Get-Content $StrTemplate
  for ($i = 0; $i -lt $strContent.Length; $i++) {
    if ($strContent[$i] -match '^35\s+35\s+33\s+3\s+1\s+\d+') {
      $strContent[$i] = "35`t35`t33`t3`t1`t$F"
    }
  }
  Set-Content $tempStr $strContent
}

function Start-CaseProcess {
  param(
    [string]$ExePath,
    [string]$OutDir,
    [int]$Sd,
    [int]$F,
    [double]$Ratio,
    [int]$MaxIter,
    [double]$Fp,
    [int]$VcRate,
    [int]$T,
    [int]$OmpThreads,
    [string]$MasterLog
  )

  Prepare-CaseInput -OutDir $OutDir -StrTemplate $Script:strTemplate -F $F
  $logfile = Join-Path $OutDir 'simulation.log'
  $inputBase = "temp_f$F"
  $t0 = Get-Date
  "[$($t0.ToString('s'))] START Sd=$Sd f=$F Hz ($Ratio fp) MaxIter=$MaxIter OMP=$OmpThreads" |
    Add-Content -Path $MasterLog

  $argList = @(
    $inputBase, 'data',
    [string]$Fp, '0.1', '0', '0', '0',
    [string]$T, [string]$Sd, [string]$VcRate, [string]$MaxIter
  ) -join ' '

  $psCommand = "`$env:OMP_NUM_THREADS='$OmpThreads'; & '$ExePath' $argList *> '$logfile'; exit `$LASTEXITCODE"
  $proc = Start-Process `
    -FilePath 'powershell.exe' `
    -ArgumentList @('-NoProfile', '-Command', $psCommand) `
    -WorkingDirectory $OutDir `
    -PassThru `
    -WindowStyle Hidden

  return [PSCustomObject]@{
    Process = $proc
    OutDir  = $OutDir
    Sd      = $Sd
    F       = $F
    Ratio   = $Ratio
    MaxIter = $MaxIter
    Start   = $t0
  }
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
      OutDir  = (Join-Path $outbase "sd${sd}_f${f}")
    }
  }
}

$masterLog = Join-Path $outbase 'screen_parallel.log'
$startAll = Get-Date
"[$($startAll.ToString('s'))] Parallel fp screening: $($cases.Count) cases, MaxParallel=$MaxParallel, OMP_NUM_THREADS=$OmpThreads" |
  Tee-Object -FilePath $masterLog
"Executable: $exepath" | Tee-Object -FilePath $masterLog -Append

$env:OMP_NUM_THREADS = "$OmpThreads"
$env:OMP_WAIT_POLICY = 'PASSIVE'

$running = @()
$failed = 0
$completed = 0
$idx = 0
$total = $cases.Count

foreach ($case in $cases) {
  if ($SkipCompleted -and (Test-CaseComplete -OutDir $case.OutDir)) {
    "[$((Get-Date).ToString('s'))] SKIP complete Sd=$($case.Sd) f=$($case.F)" | Tee-Object -FilePath $masterLog -Append
    $completed++
    continue
  }

  while ($running.Count -ge $MaxParallel) {
    Start-Sleep -Seconds 10
    $still = @()
    foreach ($entry in $running) {
      if ($entry.Process.HasExited) {
        $mins = [math]::Round(((Get-Date) - $entry.Start).TotalMinutes, 1)
        if ($entry.Process.ExitCode -ne 0) {
          "[$((Get-Date).ToString('s'))] ERROR Sd=$($entry.Sd) f=$($entry.F) exit=$($entry.Process.ExitCode) after ${mins} min" |
            Add-Content -Path $masterLog
          $failed++
        } else {
          "[$((Get-Date).ToString('s'))] DONE  Sd=$($entry.Sd) f=$($entry.F) in ${mins} min" |
            Add-Content -Path $masterLog
          $completed++
        }
      } else {
        $still += $entry
      }
    }
    $running = $still
  }

  $idx++
  "[$((Get-Date).ToString('s'))] Queue ($idx/$total) Sd=$($case.Sd) f=$($case.F) MaxIter=$($case.MaxIter)" |
    Tee-Object -FilePath $masterLog -Append

  $entry = Start-CaseProcess `
    -ExePath $exepath `
    -OutDir $case.OutDir `
    -Sd $case.Sd `
    -F $case.F `
    -Ratio $case.Ratio `
    -MaxIter $case.MaxIter `
    -Fp $Fp `
    -VcRate $VcRate `
    -T $T `
    -OmpThreads $OmpThreads `
    -MasterLog $masterLog

  $running += $entry
}

while ($running.Count -gt 0) {
  Start-Sleep -Seconds 10
  $still = @()
  foreach ($entry in $running) {
    if ($entry.Process.HasExited) {
      $mins = [math]::Round(((Get-Date) - $entry.Start).TotalMinutes, 1)
      if ($entry.Process.ExitCode -ne 0) {
        "[$((Get-Date).ToString('s'))] ERROR Sd=$($entry.Sd) f=$($entry.F) exit=$($entry.Process.ExitCode) after ${mins} min" |
          Add-Content -Path $masterLog
        $failed++
      } else {
        "[$((Get-Date).ToString('s'))] DONE  Sd=$($entry.Sd) f=$($entry.F) in ${mins} min" |
          Add-Content -Path $masterLog
        $completed++
      }
    } else {
      $still += $entry
    }
  }
  $running = $still
}

$endAll = Get-Date
$totalHrs = [math]::Round(($endAll - $startAll).TotalHours, 2)
"[$($endAll.ToString('s'))] Parallel screening finished in $totalHrs hours (completed=$completed failed=$failed)" |
  Tee-Object -FilePath $masterLog -Append

if ($failed -gt 0) { exit 1 }
