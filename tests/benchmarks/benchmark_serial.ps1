$startInfo = New-Object System.Diagnostics.ProcessStartInfo
$startInfo.FileName = "g++"
$startInfo.Arguments = "-std=c++11 -O3 src/pffdtd.cpp -o pffdtd_serial.exe"
$startInfo.RedirectStandardOutput = $true
$startInfo.RedirectStandardError = $true
$startInfo.UseShellExecute = $false

echo "Compiling..."
$process = [System.Diagnostics.Process]::Start($startInfo)
$process.WaitForExit()

if ($process.ExitCode -ne 0) {
    echo "Compilation Failed"
    echo $process.StandardError.ReadToEnd()
    exit 1
}

echo "Running Benchmark (Serial)..."
if (-not (Test-Path "tests/benchmarks/output")) { mkdir "tests/benchmarks/output" }

$sw = [System.Diagnostics.Stopwatch]::StartNew()
./pffdtd_serial.exe dipole.str tests/benchmarks/output/bench_serial
$sw.Stop()

echo "Execution Time: $($sw.Elapsed.TotalSeconds) seconds"
