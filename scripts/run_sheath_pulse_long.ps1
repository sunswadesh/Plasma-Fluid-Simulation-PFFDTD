# Long broadband pulse sheath sweep (post coupling fix).
# D-Gaussian peaked at SparHz; fp=2 MHz (known resonance band).
# MaxIter=1e6 => T~67 us, df~15 kHz.
param(
  [int[]]$SheathWidths = @(0, 2, 4, 6, 8, 10),
  [double]$Fp = 2000000,
  [int]$SparHz = 2000000,
  [int]$VcRate = 50,
  [int]$MaxIter = 200000,
  [int]$T = 2000,
  [int]$Jobs = 2,
  [int]$OmpThreads = 4
)

$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$exepath = Join-Path $root 'pffdtd_parallel.exe'
if (-not (Test-Path $exepath)) { throw 'pffdtd_parallel.exe not found' }

$strTemplate = Join-Path $root 'sheath.str'
$outbase = Join-Path $root 'results\sheath_pulse_long'
New-Item -ItemType Directory -Path $outbase -Force | Out-Null
$masterLog = Join-Path $outbase 'pulse_long.log'

$dt = 6.671114e-11
$Tsim = $MaxIter * $dt
$df = if ($Tsim -gt 0) { 1.0 / $Tsim } else { 0 }
$startAll = Get-Date
@"
[$($startAll.ToString('s'))] Starting long pulse sweep
  Sds=$($SheathWidths -join ',')  Fp=$Fp  Spar=$SparHz  MaxIter=$MaxIter
  VcRate=$VcRate  Jobs=$Jobs  OMP=$OmpThreads
  T_sim=${Tsim}s  df~${df}Hz
"@ | Set-Content $masterLog

function Start-PulseCase {
  param($Sd)
  return Start-Job -ScriptBlock {
    param($root, $exepath, $strTemplate, $outbase, $Sd, $Fp, $SparHz, $T, $VcRate, $MaxIter, $OmpThreads)
    $env:OMP_NUM_THREADS = "$OmpThreads"
    Set-Location $root
    $outdir = Join-Path $outbase ("sd{0}" -f $Sd)
    New-Item -ItemType Directory -Path $outdir -Force | Out-Null
    $outfile = Join-Path $outdir 'data'
    $logfile = Join-Path $outdir 'simulation.log'
    $tempStr = Join-Path $outdir ("temp_pulse_sd{0}.str" -f $Sd)
    $tempBase = Join-Path $outdir ("temp_pulse_sd{0}" -f $Sd)

    $strContent = Get-Content $strTemplate
    for ($i = 0; $i -lt $strContent.Length; $i++) {
      if ($strContent[$i] -match '^35\s+35\s+33\s+3\s+5\s+\d+') {
        $strContent[$i] = "35`t35`t33`t3`t5`t$SparHz"
      }
    }
    Set-Content -Path $tempStr -Value $strContent

    if (Test-Path "$outfile.fd") { Remove-Item "$outfile.fd" -Force }
    if (Test-Path "$outfile.vc") { Remove-Item "$outfile.vc" -Force }

    $t0 = Get-Date
    # .vc is the science product. Mute console (printf) entirely — it was a major
    # wall-clock cost when redirected into simulation.log.
    "START $(Get-Date -Format s) Sd=$Sd MaxIter=$MaxIter VcRate=$VcRate OMP=$OmpThreads" | Set-Content $logfile
    & $exepath $tempBase $outfile $Fp 0.1 0 0 0 $T $Sd $VcRate $MaxIter > $null 2> $null
    $code = $LASTEXITCODE
    $mins = [math]::Round(((Get-Date) - $t0).TotalMinutes, 1)
    "DONE  $(Get-Date -Format s) exit=$code minutes=$mins" | Add-Content $logfile
    return [PSCustomObject]@{ Sd = $Sd; ExitCode = $code; Minutes = $mins }
  } -ArgumentList $root, $exepath, $strTemplate, $outbase, $Sd, $Fp, $SparHz, $T, $VcRate, $MaxIter, $OmpThreads
}

$queue = [System.Collections.Generic.Queue[int]]::new()
foreach ($sd in $SheathWidths) { $queue.Enqueue($sd) }
$running = @{}

while (($queue.Count -gt 0) -or ($running.Count -gt 0)) {
  while (($running.Count -lt $Jobs) -and ($queue.Count -gt 0)) {
    $sd = $queue.Dequeue()
    $j = Start-PulseCase -Sd $sd
    $running[$j.Id] = @{ Job = $j; Sd = $sd; Start = Get-Date }
    "[$((Get-Date).ToString('s'))] START Sd=$sd job=$($j.Id)" | Add-Content $masterLog
  }

  Start-Sleep -Seconds 30
  $doneIds = @()
  foreach ($id in @($running.Keys)) {
    $entry = $running[$id]
    $j = $entry.Job
    if ($j.State -eq 'Completed' -or $j.State -eq 'Failed') {
      $r = Receive-Job $j -ErrorAction SilentlyContinue
      $mins = [math]::Round(((Get-Date) - $entry.Start).TotalMinutes, 1)
      if ($null -ne $r) {
        "[$((Get-Date).ToString('s'))] DONE  Sd=$($r.Sd) exit=$($r.ExitCode) in $($r.Minutes) min" |
          Add-Content $masterLog
      } else {
        "[$((Get-Date).ToString('s'))] DONE  Sd=$($entry.Sd) state=$($j.State) in ${mins} min (no result)" |
          Add-Content $masterLog
      }
      Remove-Job $j -Force -ErrorAction SilentlyContinue
      $doneIds += $id
    }
  }
  foreach ($id in $doneIds) { $running.Remove($id) }

  $runN = $running.Count
  $pendN = $queue.Count
  "[$((Get-Date).ToString('s'))] heartbeat running=$runN pending=$pendN" | Add-Content $masterLog
}

$hrs = [math]::Round(((Get-Date) - $startAll).TotalHours, 2)
"[$((Get-Date).ToString('s'))] long pulse sweep finished in $hrs hours" | Add-Content $masterLog
