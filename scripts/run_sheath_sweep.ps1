$exepath = Join-Path (Get-Location) 'build\pffdtd_parallel.exe'
$Sds = @(2,4,6,8,10)
foreach($sd in $Sds){
    $outdir = Join-Path 'results\sheath_sweep' ("sd$sd")
    if(-not (Test-Path $outdir)){ New-Item -ItemType Directory -Path $outdir | Out-Null }
    $outfile = Join-Path $outdir 'data'
    Write-Output "Starting Sd=$sd"
    & $exepath 'sheath' $outfile 200000 0.1 0 0 0 2000 $sd > (Join-Path $outdir 'simulation.log') 2>&1
    Write-Output "Finished Sd=$sd"
}
