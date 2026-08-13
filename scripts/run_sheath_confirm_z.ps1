# Short CW confirmation after sheath coupling fix: 1.7 and 1.9 MHz, Sd=0 vs Sd=10.
param(
  [int[]]$SheathWidths = @(0, 10),
  [int[]]$Frequencies = @(1700000, 1900000),
  [double]$Fp = 2000000,
  [int]$VcRate = 10,
  [int]$MaxIter = 100000,
  [int]$T = 100,
  [int]$OmpThreads = 2
)

$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$exepath = Join-Path $root 'pffdtd_parallel.exe'
if (-not (Test-Path $exepath)) {
  throw 'pffdtd_parallel.exe not found in repo root'
}

$strTemplate = Join-Path $root 'sheath_sine.str'
$outbase = Join-Path $root 'results\sheath_confirm_z'
New-Item -ItemType Directory -Path $outbase -Force | Out-Null
$masterLog = Join-Path $outbase 'confirm.log'

$cases = @()
foreach ($f in $Frequencies) {
  foreach ($sd in $SheathWidths) {
    $cases += [PSCustomObject]@{ Sd = $sd; F = $f }
  }
}

$startAll = Get-Date
"[$($startAll.ToString('s'))] Starting confirm-Z: $($cases.Count) cases MaxIter=$MaxIter OMP=$OmpThreads" |
  Set-Content $masterLog

$jobs = @()
foreach ($case in $cases) {
  $Sd = $case.Sd
  $f = $case.F
  $jobs += Start-Job -ScriptBlock {
    param($root, $exepath, $strTemplate, $outbase, $Sd, $f, $Fp, $T, $VcRate, $MaxIter, $OmpThreads)
    $env:OMP_NUM_THREADS = "$OmpThreads"
    Set-Location $root
    $outdir = Join-Path $outbase "sd${Sd}_f${f}"
    New-Item -ItemType Directory -Path $outdir -Force | Out-Null
    $outfile = Join-Path $outdir 'data'
    $logfile = Join-Path $outdir 'simulation.log'
    $tempStr = Join-Path $outdir ("temp_f{0}.str" -f $f)
    $tempBase = Join-Path $outdir ("temp_f{0}" -f $f)

    $strContent = Get-Content $strTemplate
    for ($i = 0; $i -lt $strContent.Length; $i++) {
      if ($strContent[$i] -match '^35\s+35\s+33\s+3\s+1\s+\d+') {
        $strContent[$i] = "35`t35`t33`t3`t1`t$f"
      }
    }
    Set-Content -Path $tempStr -Value $strContent

    $t0 = Get-Date
    & $exepath $tempBase $outfile $Fp 0.1 0 0 0 $T $Sd $VcRate $MaxIter > $logfile 2>&1
    $code = $LASTEXITCODE
    $mins = [math]::Round(((Get-Date) - $t0).TotalMinutes, 1)
    return [PSCustomObject]@{
      Sd = $Sd; F = $f; ExitCode = $code; Minutes = $mins
    }
  } -ArgumentList $root, $exepath, $strTemplate, $outbase, $Sd, $f, $Fp, $T, $VcRate, $MaxIter, $OmpThreads

  "[$((Get-Date).ToString('s'))] QUEUED Sd=$Sd f=$f job=$($jobs[-1].Id)" |
    Add-Content $masterLog
}

while ($true) {
  $pending = @($jobs | Where-Object { $_.State -ne 'Completed' -and $_.State -ne 'Failed' })
  if ($pending.Count -eq 0) { break }
  $running = @($jobs | Where-Object State -eq 'Running').Count
  $done = @($jobs | Where-Object { $_.State -eq 'Completed' -or $_.State -eq 'Failed' }).Count
  "[$((Get-Date).ToString('s'))] heartbeat running=$running done=$done" | Add-Content $masterLog
  Wait-Job -Job $jobs -Timeout 60 | Out-Null
}

foreach ($j in $jobs) {
  $r = Receive-Job $j -ErrorAction SilentlyContinue
  if ($null -ne $r) {
    "[$((Get-Date).ToString('s'))] DONE Sd=$($r.Sd) f=$($r.F) exit=$($r.ExitCode) in $($r.Minutes) min" |
      Add-Content $masterLog
  } else {
    "[$((Get-Date).ToString('s'))] DONE job=$($j.Id) state=$($j.State) (no result)" |
      Add-Content $masterLog
  }
  Remove-Job $j -Force -ErrorAction SilentlyContinue
}

$hrs = [math]::Round(((Get-Date) - $startAll).TotalHours, 2)
"[$((Get-Date).ToString('s'))] confirm-Z finished in $hrs hours" | Add-Content $masterLog
