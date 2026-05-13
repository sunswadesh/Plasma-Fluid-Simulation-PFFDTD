param(
  [int]$Sd = 4,
  [int]$Iterations = 1000000
)

$exepath = Join-Path (Get-Location) 'build\pffdtd_parallel.exe'
$outdir = Join-Path 'results\sheath_long' ("sd$Sd")
if(-not (Test-Path $outdir)){ New-Item -ItemType Directory -Path $outdir -Force | Out-Null }
$outfile = Join-Path $outdir 'data'
Write-Output "Starting long-run Sd=$Sd Iterations=$Iterations"
& $exepath 'sheath' $outfile 200000 0.1 0 0 0 $Iterations $Sd > (Join-Path $outdir 'simulation.log') 2>&1
Write-Output "Finished Sd=$Sd"
