param(
  [int]$Sd = 4,
  [int]$T = 2000,
  [int]$VcRate = 10,
  [int]$MaxIter = 1000000
)

$root = Split-Path -Parent $PSScriptRoot
$exepath = Join-Path $root 'build\pffdtd_parallel.exe'
if(-not (Test-Path $exepath)) {
    $exepath = Join-Path $root 'pffdtd_parallel.exe'
}
Write-Output "Using executable: $exepath"
if(-not (Test-Path $exepath)) {
    throw "pffdtd_parallel.exe not found in root or build folder"
}
$outdir = Join-Path -Path (Join-Path $root 'results\sheath_long') -ChildPath ("sd$Sd")
if(-not (Test-Path $outdir)){ New-Item -ItemType Directory -Path $outdir -Force | Out-Null }
$outfile = Join-Path -Path $outdir -ChildPath 'data'
$logfile = Join-Path -Path $outdir -ChildPath 'simulation.log'
if (Test-Path $logfile) {
    $logfile = Join-Path -Path $outdir -ChildPath ("simulation_{0}.log" -f (Get-Date -Format 'yyyyMMdd_HHmmss'))
}
if (Test-Path "$outfile.fd") {
    Remove-Item "$outfile.fd" -Force
}
Write-Output "Starting long-run Sd=$Sd T=$T VcRate=$VcRate MaxIter=$MaxIter"
Write-Output "Logging to: $logfile"
& $exepath 'sheath' $outfile 200000 0.1 0 0 0 $T $Sd $VcRate $MaxIter > $logfile 2>&1
Write-Output "Finished Sd=$Sd"
