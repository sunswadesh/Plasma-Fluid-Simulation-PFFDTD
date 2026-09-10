# Paper 2 single-tone pilot: static vs oscillating sheath
# Compares feed V/I at one CW frequency for:
#   - static rs0
#   - static rs0 + ceil(dR)  (upper bracket)
#   - oscillating rs(t) = rs0 + dR sin(wt+phi)
#
# Usage:
#   powershell -File projects/tu2008-sheath/scripts/run_paper2_rs_t_pilot.ps1
#   powershell -File ... -MaxParallel 3 -OmpThreads 2

param(
  [int]$Rs0 = 4,
  [double]$DeltaR = 1.0,
  [double]$PhaseDeg = 0.0,
  [int]$FrequencyHz = 700000,
  [double]$Fp = 2000000,
  [int]$VcRate = 10,
  [int]$MinIter = 100000,
  [int]$MinDriveCycles = 20,
  [double]$Dt = 6.671114e-11,
  [int]$T = 100,
  [int]$MaxParallel = 3,
  [int]$OmpThreads = 2,
  [switch]$SkipCompleted,
  [switch]$DryRun
)

$ErrorActionPreference = 'Continue'

. "$PSScriptRoot\config.ps1"
Initialize-SheathRun
$root = $PffdtdRoot
$exepath = Get-PffdtdExe -Variant rs_t
$strTemplate = Join-Path $root 'sheath_sine_vc.str'
if (-not (Test-Path $strTemplate)) {
  throw "Missing template: $strTemplate"
}

$outbase = Join-Path $root 'results\paper2_rs_t_pilot'
New-Item -ItemType Directory -Path $outbase -Force | Out-Null
$masterLog = Join-Path $outbase 'pilot_master.log'

function Get-MaxIterForFrequency {
  param([double]$Frequency, [int]$MinIter)
  if ($Frequency -le 0 -or $Dt -le 0) { return $MinIter }
  $needed = [math]::Ceiling($MinDriveCycles / ($Frequency * $Dt))
  $iter = [math]::Max($MinIter, $needed)
  return [int]([math]::Ceiling($iter / 10000.0) * 10000)
}

function Start-PilotCase {
  param(
    [string]$Root,
    [string]$ExePath,
    [string]$StrTemplate,
    [string]$OutDir,
    [string]$Name,
    [int]$Sd,
    [double]$DeltaR,
    [double]$Phase,
    [int]$F,
    [int]$MaxIter,
    [double]$Fp,
    [int]$T,
    [int]$VcRate,
    [int]$OmpThreads
  )
  return Start-Job -ScriptBlock {
    param($Root, $ExePath, $StrTemplate, $OutDir, $Name, $Sd, $DeltaR, $Phase, $F, $MaxIter, $Fp, $T, $VcRate, $OmpThreads)
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
    $vc = "$outfile.vc"

    if (Test-Path "$outfile.fd") { Remove-Item "$outfile.fd" -Force -ErrorAction SilentlyContinue }
    if (Test-Path $vc) { Remove-Item $vc -Force -ErrorAction SilentlyContinue }

    $t0 = Get-Date
    "START $(Get-Date -Format s) $Name Sd=$Sd dR=$DeltaR phi=$Phase MaxIter=$MaxIter OMP=$OmpThreads" |
      Set-Content $logfile

    & $ExePath $inputBase $outfile $Fp 0.1 0 0 0 $T $Sd $VcRate $MaxIter $DeltaR $Phase 0 *> $null
    $code = $LASTEXITCODE
    $mins = [math]::Round(((Get-Date) - $t0).TotalMinutes, 2)
    $vcBytes = if (Test-Path $vc) { (Get-Item $vc).Length } else { 0 }
    "DONE  $(Get-Date -Format s) exit=$code minutes=$mins vc_bytes=$vcBytes" | Add-Content $logfile

    return [PSCustomObject]@{
      Name = $Name; ExitCode = $code; Minutes = $mins; VcBytes = $vcBytes
    }
  } -ArgumentList $Root, $ExePath, $StrTemplate, $OutDir, $Name, $Sd, $DeltaR, $Phase, $F, $MaxIter, $Fp, $T, $VcRate, $OmpThreads
}

$maxIter = Get-MaxIterForFrequency -Frequency $FrequencyHz -MinIter $MinIter
$rsMax = $Rs0 + [int][math]::Ceiling([math]::Abs($DeltaR))

$cases = @(
  @{ Name = "static_rs0";   Sd = $Rs0;   DeltaR = 0.0;     Phase = 0.0 },
  @{ Name = "static_rsmax"; Sd = $rsMax; DeltaR = 0.0;     Phase = 0.0 },
  @{ Name = "osc_rs_t";     Sd = $Rs0;   DeltaR = $DeltaR; Phase = $PhaseDeg }
)

$summary = Join-Path $outbase 'pilot_summary.txt'
$startAll = Get-Date
@(
  "Paper 2 rs(t) pilot  $($startAll.ToString('s'))",
  "f=$FrequencyHz Hz  fp=$Fp  rs0=$Rs0  dR=$DeltaR  phi=$PhaseDeg deg  MaxIter=$maxIter",
  "MaxParallel=$MaxParallel OmpThreads=$OmpThreads",
  "exe=$exepath",
  ""
) | Set-Content $summary
@(
  "[$($startAll.ToString('s'))] Paper 2 pilot: $($cases.Count) cases, MaxParallel=$MaxParallel, OMP=$OmpThreads"
) | Set-Content $masterLog

if ($DryRun) {
  foreach ($c in $cases) {
    "DRY $($c.Name) Sd=$($c.Sd) dR=$($c.DeltaR) phi=$($c.Phase) MaxIter=$maxIter" |
      Tee-Object -FilePath $summary -Append
  }
  Write-Host "Dry-run only. Summary: $summary"
  return
}

$queue = [System.Collections.Queue]::new()
foreach ($c in $cases) {
  $outDir = Join-Path $outbase $c.Name
  $vc = Join-Path $outDir 'data.vc'
  if ($SkipCompleted -and (Test-Path $vc) -and ((Get-Item $vc).Length -ge 100000)) {
    "SKIP $($c.Name) (existing data.vc)" | Tee-Object -FilePath $summary -Append
    continue
  }
  $queue.Enqueue($c)
}

$running = @()
while ($queue.Count -gt 0 -or $running.Count -gt 0) {
  while ($running.Count -lt $MaxParallel -and $queue.Count -gt 0) {
    $c = $queue.Dequeue()
    $outDir = Join-Path $outbase $c.Name
    "START $($c.Name) Sd=$($c.Sd) dR=$($c.DeltaR) phi=$($c.Phase)" |
      Tee-Object -FilePath $summary -Append
    "[$(Get-Date -Format s)] START $($c.Name)" | Add-Content $masterLog
    $job = Start-PilotCase -Root $root -ExePath $exepath -StrTemplate $strTemplate `
      -OutDir $outDir -Name $c.Name -Sd $c.Sd -DeltaR $c.DeltaR -Phase $c.Phase `
      -F $FrequencyHz -MaxIter $maxIter -Fp $Fp -T $T -VcRate $VcRate -OmpThreads $OmpThreads
    $running += ,@{ Name = $c.Name; Job = $job }
  }

  Start-Sleep -Seconds 15
  $still = @()
  foreach ($r in $running) {
    if ($r.Job.State -eq 'Running') {
      $still += ,$r
      continue
    }
    $res = Receive-Job $r.Job -ErrorAction SilentlyContinue
    Remove-Job $r.Job -Force -ErrorAction SilentlyContinue
    $line = if ($res) {
      "DONE $($res.Name) exit=$($res.ExitCode) minutes=$($res.Minutes) vc_bytes=$($res.VcBytes)"
    } else {
      "DONE $($r.Name) (no result object; check simulation.log)"
    }
    $line | Tee-Object -FilePath $summary -Append
    "[$(Get-Date -Format s)] $line" | Add-Content $masterLog
  }
  $running = $still
}

$minsAll = [math]::Round(((Get-Date) - $startAll).TotalMinutes, 1)
"ALL DONE wall_minutes=$minsAll" | Tee-Object -FilePath $summary -Append
"[$(Get-Date -Format s)] ALL DONE wall_minutes=$minsAll" | Add-Content $masterLog
Write-Host "Pilot outputs under $outbase"
Write-Host "Summary: $summary"
