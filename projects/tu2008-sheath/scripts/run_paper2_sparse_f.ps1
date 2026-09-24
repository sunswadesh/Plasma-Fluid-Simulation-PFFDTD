# Sparse frequency set for Paper 2 (soft Delta-r=1 + static brackets)
# Default: 500 kHz and 1.2 MHz (700 kHz already in paper2_rs_t_pilot_soft).

param(
  [int]$Rs0 = 4,
  [double]$DeltaR = 1.0,
  [double]$SoftEdge = 1.0,
  [double]$PhaseDeg = 0.0,
  [int[]]$FrequenciesHz = @(500000, 1200000),
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
if (-not (Test-Path $strTemplate)) { throw "Missing $strTemplate" }

$outbase = Join-Path $root 'results\paper2_sparse_f_soft'
New-Item -ItemType Directory -Path $outbase -Force | Out-Null
$masterLog = Join-Path $outbase 'scan_master.log'

function Get-MaxIterForFrequency {
  param([double]$Frequency, [int]$MinIter)
  if ($Frequency -le 0 -or $Dt -le 0) { return $MinIter }
  $needed = [math]::Ceiling($MinDriveCycles / ($Frequency * $Dt))
  $iter = [math]::Max($MinIter, $needed)
  return [int]([math]::Ceiling($iter / 10000.0) * 10000)
}

function Start-FreqCase {
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
    $edgeArg = if ($DeltaR -gt 0) { $SoftEdge } else { 0.0 }
    if (Test-Path "$outfile.vc") { Remove-Item "$outfile.vc" -Force -ErrorAction SilentlyContinue }
    $t0 = Get-Date
    "START $(Get-Date -Format s) $Name Sd=$Sd dR=$DeltaR soft=$edgeArg f=$F MaxIter=$MaxIter" | Set-Content $logfile
    & $ExePath $inputBase $outfile $Fp 0.1 0 0 0 $T $Sd $VcRate $MaxIter $DeltaR $Phase 0 $edgeArg *> $null
    $code = $LASTEXITCODE
    $mins = [math]::Round(((Get-Date) - $t0).TotalMinutes, 2)
    $vcBytes = if (Test-Path "$outfile.vc") { (Get-Item "$outfile.vc").Length } else { 0 }
    "DONE $(Get-Date -Format s) exit=$code minutes=$mins vc_bytes=$vcBytes" | Add-Content $logfile
    return [PSCustomObject]@{ Name=$Name; ExitCode=$code; Minutes=$mins; VcBytes=$vcBytes }
  } -ArgumentList $Root,$ExePath,$StrTemplate,$OutDir,$Name,$Sd,$DeltaR,$Phase,$SoftEdge,$F,$MaxIter,$Fp,$T,$VcRate,$OmpThreads
}

$rsMax = $Rs0 + [int][math]::Ceiling([math]::Abs($DeltaR))
$cases = @()
foreach ($f in $FrequenciesHz) {
  $maxIter = Get-MaxIterForFrequency -Frequency $f -MinIter $MinIter
  $cases += @{ Name = "static_rs0_f$f"; Sd = $Rs0; DeltaR = 0.0; F = $f; MaxIter = $maxIter }
  $cases += @{ Name = "static_rsmax_f$f"; Sd = $rsMax; DeltaR = 0.0; F = $f; MaxIter = $maxIter }
  $cases += @{ Name = "osc_f$f"; Sd = $Rs0; DeltaR = $DeltaR; F = $f; MaxIter = $maxIter }
}

$startAll = Get-Date
@(
  "[$($startAll.ToString('s'))] Sparse-f soft scan: $($cases.Count) cases freqs=$($FrequenciesHz -join ',')"
  "dR=$DeltaR soft=$SoftEdge MaxParallel=$MaxParallel OMP=$OmpThreads"
) | Set-Content $masterLog

if ($DryRun) {
  $cases | ForEach-Object { Write-Host ("DRY {0} Sd={1} dR={2} f={3} MaxIter={4}" -f $_.Name, $_.Sd, $_.DeltaR, $_.F, $_.MaxIter) }
  return
}

$queue = [System.Collections.Queue]::new()
foreach ($c in $cases) {
  $outDir = Join-Path $outbase $c.Name
  $vc = Join-Path $outDir 'data.vc'
  if ($SkipCompleted -and (Test-Path $vc) -and ((Get-Item $vc).Length -ge 100000)) {
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
    "[$(Get-Date -Format s)] START $($c.Name) f=$($c.F) Sd=$($c.Sd) dR=$($c.DeltaR)" | Tee-Object -FilePath $masterLog -Append
    $job = Start-FreqCase -Root $root -ExePath $exepath -StrTemplate $strTemplate `
      -OutDir $outDir -Name $c.Name -Sd $c.Sd -DeltaR $c.DeltaR -Phase $PhaseDeg `
      -SoftEdge $SoftEdge -F $c.F -MaxIter $c.MaxIter -Fp $Fp -T $T -VcRate $VcRate -OmpThreads $OmpThreads
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
