# Paper 2 matched soft Delta-r scan: SheathSoftEdge = c * DeltaR (default c=1)
# Oscillating cases only; static brackets reused from prior soft campaigns in analysis.
# Outputs under results/paper2_delta_r_matched/

param(
  [int]$Rs0 = 4,
  [double[]]$DeltaRs = @(0.5, 1.0, 1.5, 2.0),
  [double]$SoftFrac = 1.0,
  [double]$PhaseDeg = 0.0,
  [int]$FrequencyHz = 700000,
  [double]$Fp = 2000000,
  [int]$VcRate = 10,
  [int]$MinIter = 100000,
  [int]$MinDriveCycles = 20,
  [double]$Dt = 6.671114e-11,
  [int]$T = 100,
  [int]$MaxParallel = 2,
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
if (-not (Test-Path $strTemplate)) { throw "Missing $strTemplate" }

$outbase = Join-Path $root 'results\paper2_delta_r_matched'
New-Item -ItemType Directory -Path $outbase -Force | Out-Null
$masterLog = Join-Path $outbase 'scan_master.log'

function Get-MaxIterForFrequency {
  param([double]$Frequency, [int]$MinIter)
  if ($Frequency -le 0 -or $Dt -le 0) { return $MinIter }
  $needed = [math]::Ceiling($MinDriveCycles / ($Frequency * $Dt))
  $iter = [math]::Max($MinIter, $needed)
  return [int]([math]::Ceiling($iter / 10000.0) * 10000)
}

function Start-DrCase {
  param($Root,$ExePath,$StrTemplate,$OutDir,$Name,$Sd,$DeltaR,$Phase,$SoftEdge,$F,$MaxIter,$Fp,$T,$VcRate,$OmpThreads)
  return Start-Job -ScriptBlock {
    param($Root,$ExePath,$StrTemplate,$OutDir,$Name,$Sd,$DeltaR,$Phase,$SoftEdge,$F,$MaxIter,$Fp,$T,$VcRate,$OmpThreads)
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
    if (Test-Path "$outfile.vc") { Remove-Item "$outfile.vc" -Force -ErrorAction SilentlyContinue }
    $t0 = Get-Date
    "START $(Get-Date -Format s) $Name Sd=$Sd dR=$DeltaR soft=$SoftEdge MaxIter=$MaxIter" | Set-Content $logfile
    & $ExePath $inputBase $outfile $Fp 0.1 0 0 0 $T $Sd $VcRate $MaxIter $DeltaR $Phase 0 $SoftEdge *> $null
    $code = $LASTEXITCODE
    $mins = [math]::Round(((Get-Date) - $t0).TotalMinutes, 2)
    $vcBytes = if (Test-Path "$outfile.vc") { (Get-Item "$outfile.vc").Length } else { 0 }
    "DONE $(Get-Date -Format s) exit=$code minutes=$mins vc_bytes=$vcBytes" | Add-Content $logfile
    return [PSCustomObject]@{ Name=$Name; ExitCode=$code; Minutes=$mins; VcBytes=$vcBytes }
  } -ArgumentList $Root,$ExePath,$StrTemplate,$OutDir,$Name,$Sd,$DeltaR,$Phase,$SoftEdge,$F,$MaxIter,$Fp,$T,$VcRate,$OmpThreads
}

$maxIter = Get-MaxIterForFrequency -Frequency $FrequencyHz -MinIter $MinIter
$cases = @()
foreach ($dr in $DeltaRs) {
  $soft = [math]::Max(0.25, $SoftFrac * $dr)
  $tag = ('dr{0}' -f (('{0:0.##}' -f $dr) -replace '\.','p'))
  # Skip dr=1 soft=1: identical to soft pilot (reuse in analysis)
  if ([math]::Abs($dr - 1.0) -lt 1e-9 -and [math]::Abs($soft - 1.0) -lt 1e-9) { continue }
  $cases += @{ Name = "osc_$tag"; DeltaR = [double]$dr; SoftEdge = [double]$soft }
}

$startAll = Get-Date
@(
  "[$($startAll.ToString('s'))] Matched soft Delta-r: $($cases.Count) osc cases, SoftFrac=$SoftFrac"
  "f=$FrequencyHz MaxIter=$maxIter MaxParallel=$MaxParallel OMP=$OmpThreads"
) | Set-Content $masterLog

if ($DryRun) {
  $cases | ForEach-Object { Write-Host ("DRY {0} dR={1} soft={2}" -f $_.Name, $_.DeltaR, $_.SoftEdge) }
  return
}

$queue = [System.Collections.Queue]::new()
foreach ($c in $cases) {
  $outDir = Join-Path $outbase $c.Name
  $vc = Join-Path $outDir 'data.vc'
  if ($SkipCompleted -and (Test-Path $vc) -and ((Get-Item $vc).Length -ge 1000000)) {
    "[$(Get-Date -Format s)] SKIP $($c.Name)" | Add-Content $masterLog
    continue
  }
  $queue.Enqueue($c)
}

$running = @()
while ($queue.Count -gt 0 -or $running.Count -gt 0) {
  while ($running.Count -lt $MaxParallel -and $queue.Count -gt 0) {
    $c = $queue.Dequeue()
    $outDir = Join-Path $outbase $c.Name
    "[$(Get-Date -Format s)] START $($c.Name) dR=$($c.DeltaR) soft=$($c.SoftEdge)" | Tee-Object -FilePath $masterLog -Append
    $job = Start-DrCase -Root $root -ExePath $exepath -StrTemplate $strTemplate `
      -OutDir $outDir -Name $c.Name -Sd $Rs0 -DeltaR $c.DeltaR -Phase $PhaseDeg `
      -SoftEdge $c.SoftEdge -F $FrequencyHz -MaxIter $maxIter -Fp $Fp -T $T -VcRate $VcRate -OmpThreads $OmpThreads
    $running += ,@{ Name = $c.Name; Job = $job }
  }
  Start-Sleep -Seconds 20
  $still = @()
  foreach ($r in $running) {
    if ($r.Job.State -eq 'Running') { $still += ,$r; continue }
    $res = Receive-Job $r.Job -ErrorAction SilentlyContinue
    Remove-Job $r.Job -Force -ErrorAction SilentlyContinue
    $line = if ($res) { "DONE $($res.Name) exit=$($res.ExitCode) minutes=$($res.Minutes) vc=$($res.VcBytes)" } else { "DONE $($r.Name)" }
    "[$(Get-Date -Format s)] $line" | Tee-Object -FilePath $masterLog -Append
  }
  $running = $still
}

$minsAll = [math]::Round(((Get-Date) - $startAll).TotalMinutes, 1)
"[$(Get-Date -Format s)] ALL DONE wall_minutes=$minsAll" | Tee-Object -FilePath $masterLog -Append
Write-Host "Outputs under $outbase"
