$exepath = Join-Path (Get-Location) 'pffdtd_parallel.exe'
$vcStep = 10
$maxIter = 1000000
$Sds = @(0,2,4,6,8,10)
foreach($sd in $Sds){
    $outdir = Join-Path 'results\sheath_sweep' ("sd$sd")
    if(-not (Test-Path $outdir)){ New-Item -ItemType Directory -Path $outdir | Out-Null }
    $outfile = Join-Path $outdir 'data'
    if (Test-Path "$outfile.fd") {
        Remove-Item "$outfile.fd" -Force
    }
    Write-Output "Starting Sd=$sd"
    & $exepath 'sheath' $outfile 200000 0.1 0 0 0 2000 $sd $vcStep $maxIter > (Join-Path $outdir 'simulation.log') 2>&1
    Write-Output "Finished Sd=$sd (vc_step=$vcStep, max_iter=$maxIter)"
}
