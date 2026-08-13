# Targeted CW sweep for Tu f_res(Sd): 1.5–2.3 MHz, Sd=0..10.
# V/I (.vc) only — no field dumps, muted solver console.

param(
  [int[]]$SheathWidths = @(0, 2, 4, 6, 8, 10),
  [int[]]$FrequenciesHz = @(
    1500000, 1600000, 1700000, 1750000, 1800000, 1850000,
    1900000, 2000000, 2100000, 2200000, 2300000
  ),
  [double]$Fp = 2000000,
  [int]$VcRate = 10,
  [int]$MinIter = 100000,
  [int]$MinDriveCycles = 15,
  [double]$Dt = 6.671114e-11,
  [int]$T = 100,
  [int]$MaxParallel = 2,
  [int]$OmpThreads = 4,
  [switch]$SkipCompleted
)

$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$exepath = Join-Path $root 'pffdtd_parallel.exe'
if (-not (Test-Path $exepath)) {
  $exepath = Join-Path $root 'build\pffdtd_parallel.exe'
}
if (-not (Test-Path $exepath)) {
  throw 'pffdtd_parallel.exe not found'
}

$strTemplate = Join-Path $root 'sheath_sine_vc.str'
if (-not (Test-Path $strTemplate)) {
  throw "Missing template: $strTemplate"
}

$outbase = Join-Path $root 'results\sheath_cw_tu'
New-Item -ItemType Directory -Path $outbase -Force | Out-Null
$masterLog = Join-Path $outbase 'cw_tu.log'

function Get-MaxIterForFrequency {
  param([double]$Frequency, [int]$MinIter)
  if ($Frequency -le 0 -or $Dt -le 0) { return $MinIter }
  $needed = [math]::Ceiling($MinDriveCycles / ($Frequency * $Dt))
  $iter = [math]::Max($MinIter, $needed)
  return [int]([math]::Ceiling($iter / 10000.0) * 10000)
}

function Test-CaseComplete {
  param([string]$OutDir)
  $vc = Join-Path $OutDir 'data.vc'
  if (-not (Test-Path $vc)) { return $false }
  return ((Get-Item $vc).Length -ge 300000)
}

function Start-CwTuCase {
  param(
    [string]$Root,
    [string]$ExePath,
    [string]$StrTemplate,
    [string]$OutDir,
    [int]$Sd,
    [int]$F,
    [int]$MaxIter,
    [double]$Fp,
    [int]$T,
    [int]$VcRate,
    [int]$OmpThreads
  )
  return Start-Job -ScriptBlock {
    param($Root, $ExePath, $StrTemplate, $OutDir, $Sd, $F, $MaxIter, $Fp, $T, $VcRate, $OmpThreads)
    Set-Location $Root
    $env:OMP_NUM_THREADS = "$OmpThreads"
    New-Item -ItemType Directory -Path $OutDir -Force | Out-Null

    $tempStr = Join-Path $OutDir "temp_f${F}.str"
    $strContent = Get-Content $StrTemplate
    for ($i = 0; $i -lt $strContent.Length; $i++) {
      if ($strContent[$i] -match '^35\s+35\s+33\s+3\s+1\s+\d+') {
        $strContent[$i] = "35`t35`t33`t3`t1`t$F"
      }
    }
    Set-Content -Path $tempStr -Value $strContent

    $logfile = Join-Path $OutDir 'simulation.log'
    $inputBase = Join-Path $OutDir "temp_f$F"
    $outfile = Join-Path $OutDir 'data'

    if (Test-Path "$outfile.fd") { Remove-Item "$outfile.fd" -Force -ErrorAction SilentlyContinue }
    if (Test-Path "$outfile.vc") { Remove-Item "$outfile.vc" -Force -ErrorAction SilentlyContinue }

    $t0 = Get-Date
    "START $(Get-Date -Format s) Sd=$Sd f=$F MaxIter=$MaxIter VcRate=$VcRate OMP=$OmpThreads" |
      Set-Content $logfile

    & $ExePath $inputBase $outfile $Fp 0.1 0 0 0 $T $Sd $VcRate $MaxIter > $null 2> $null
    $code = $LASTEXITCODE
    $mins = [math]::Round(((Get-Date) - $t0).TotalMinutes, 1)

    if (Test-Path "$outfile.fd") { Remove-Item "$outfile.fd" -Force -ErrorAction SilentlyContinue }

    $vcBytes = if (Test-Path "$outfile.vc") { (Get-Item "$outfile.vc").Length } else { 0 }
    "DONE  $(Get-Date -Format s) exit=$code minutes=$mins vc_bytes=$vcBytes" | Add-Content $logfile

    return [PSCustomObject]@{ Sd = $Sd; F = $F; ExitCode = $code; Minutes = $mins; VcBytes = $vcBytes }
  } -ArgumentList $Root, $ExePath, $StrTemplate, $OutDir, $Sd, $F, $MaxIter, $Fp, $T, $VcRate, $OmpThreads
}

$cases = @()
foreach ($f in $FrequenciesHz) {
  $maxIter = Get-MaxIterForFrequency -Frequency $f -MinIter $MinIter
  foreach ($sd in $SheathWidths) {
    $cases += [PSCustomObject]@{
      Sd      = $sd
      F       = $f
      MaxIter = $maxIter
      OutDir  = (Join-Path $outbase "sd${sd}_f${f}")
    }
  }
}

$startAll = Get-Date
@(
  "[$($startAll.ToString('s'))] Targeted CW Tu sweep: $($cases.Count) cases",
  "  Sds=$($SheathWidths -join ',')",
  "  freqs_MHz=$([string]::Join(',', ($FrequenciesHz | ForEach-Object { '{0:N2}' -f ($_ / 1e6) })))",
  "  Fp=$Fp  VcRate=$VcRate  MaxParallel=$MaxParallel  OMP=$OmpThreads",
  "  template=$strTemplate  (no .fd block)",
  "  exe=$exepath"
) | Set-Content $masterLog

$queue = [System.Collections.Generic.Queue[object]]::new()
foreach ($c in $cases) { $queue.Enqueue($c) }
$running = @{}
$failed = 0
$completed = 0
$skipped = 0

while (($queue.Count -gt 0) -or ($running.Count -gt 0)) {
  while (($running.Count -lt $MaxParallel) -and ($queue.Count -gt 0)) {
    $case = $queue.Dequeue()
    if ($SkipCompleted -and (Test-CaseComplete -OutDir $case.OutDir)) {
      "[$((Get-Date).ToString('s'))] SKIP Sd=$($case.Sd) f=$($case.F)" | Add-Content $masterLog
      $skipped++
      continue
    }

    $j = Start-CwTuCase `
      -Root $root `
      -ExePath $exepath `
      -StrTemplate $strTemplate `
      -OutDir $case.OutDir `
      -Sd $case.Sd `
      -F $case.F `
      -MaxIter $case.MaxIter `
      -Fp $Fp `
      -T $T `
      -VcRate $VcRate `
      -OmpThreads $OmpThreads
    $running[$j.Id] = @{ Job = $j; Case = $case; Start = Get-Date }
    "[$((Get-Date).ToString('s'))] START Sd=$($case.Sd) f=$($case.F) MaxIter=$($case.MaxIter) job=$($j.Id)" |
      Add-Content $masterLog
  }

  Start-Sleep -Seconds 30
  $doneIds = @()
  foreach ($id in @($running.Keys)) {
    $entry = $running[$id]
    $j = $entry.Job
    if ($j.State -eq 'Completed' -or $j.State -eq 'Failed') {
      $r = Receive-Job $j -ErrorAction SilentlyContinue
      if ($null -ne $r) {
        if ($r.ExitCode -ne 0) {
          "[$((Get-Date).ToString('s'))] ERROR Sd=$($r.Sd) f=$($r.F) exit=$($r.ExitCode) in $($r.Minutes) min" |
            Add-Content $masterLog
          $failed++
        } else {
          "[$((Get-Date).ToString('s'))] DONE  Sd=$($r.Sd) f=$($r.F) in $($r.Minutes) min" |
            Add-Content $masterLog
          $completed++
        }
      } else {
        "[$((Get-Date).ToString('s'))] DONE  Sd=$($entry.Case.Sd) f=$($entry.Case.F) state=$($j.State) (no result)" |
          Add-Content $masterLog
        $failed++
      }
      Remove-Job $j -Force -ErrorAction SilentlyContinue
      $doneIds += $id
    }
  }
  foreach ($id in $doneIds) { $running.Remove($id) }

  if (($running.Count -gt 0) -or ($queue.Count -gt 0)) {
    "[$((Get-Date).ToString('s'))] heartbeat running=$($running.Count) pending=$($queue.Count) done=$completed skip=$skipped fail=$failed" |
      Add-Content $masterLog
  }
}

$hrs = [math]::Round(((Get-Date) - $startAll).TotalHours, 2)
"[$((Get-Date).ToString('s'))] CW Tu sweep finished in $hrs h (completed=$completed skipped=$skipped failed=$failed)" |
  Add-Content $masterLog

if ($failed -gt 0) { exit 1 }
