param(
  [int]$Sd = 0,
  [int[]]$Frequencies = @(200000, 250000, 300000, 350000, 400000),
  [int]$VcRate = 10,
  [int]$MaxIter = 100000,
  [int]$T = 100
)

$root = Split-Path -Parent $PSScriptRoot
$exepath = Join-Path $root 'build\pffdtd_parallel.exe'
if(-not (Test-Path $exepath)) {
    $exepath = Join-Path $root 'pffdtd_parallel.exe'
}
if(-not (Test-Path $exepath)) {
    throw 'pffdtd_parallel.exe not found in root or build folder'
}

$outbase = Join-Path $root 'results\sheath_narrow_band'
if(-not (Test-Path $outbase)) { New-Item -ItemType Directory -Path $outbase -Force | Out-Null }

Write-Output "Using executable: $exepath"
Write-Output "Narrow-band sweep for Sd=$Sd, VcRate=$VcRate, MaxIter=$MaxIter"

foreach ($f in $Frequencies) {
    $outdir = Join-Path $outbase "sd$Sd_f$f"
    if (-not (Test-Path $outdir)) { New-Item -ItemType Directory -Path $outdir -Force | Out-Null }
    $outfile = Join-Path $outdir 'data'
    $logfile = Join-Path $outdir 'simulation.log'
    Write-Output "--- Running Source Frequency $f Hz ---"
    Write-Output "Output: $outfile"
    
    # Dynamically generate a .str file for this frequency based on sheath_sine.str
    $tempStr = Join-Path $outdir "temp_f$f.str"
    $strContent = Get-Content (Join-Path $root 'sheath_sine.str')
    for ($i=0; $i -lt $strContent.Length; $i++) {
        if ($strContent[$i] -match '^35\s+35\s+33\s+3\s+1\s+\d+') {
            $strContent[$i] = "35`t35`t33`t3`t1`t$f"
        }
    }
    Set-Content $tempStr $strContent
    
    # We pass FREQ_PLASMA = 2000000 (2 MHz)
    & $exepath (Join-Path $outdir "temp_f$f") $outfile 2000000 0.1 0 0 0 $T $Sd $VcRate $MaxIter > $logfile 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Output "ERROR: run failed at $f Hz with exit code $LASTEXITCODE"
        break
    }
    Write-Output "Finished $f Hz"
}

Write-Output 'Narrow-band sweep complete.'
