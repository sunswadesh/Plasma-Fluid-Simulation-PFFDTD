@echo off
setlocal
pushd %~dp0..

echo ========================================================
echo          PFFDTD Benchmark Comparison
echo ========================================================
echo.

if not exist results mkdir results
if not exist results\benchmarks mkdir results\benchmarks

echo [1/2] Running Benchmark on LEGACY Executable (pffdtd_parallel_0.exe)...
if not exist "pffdtd_parallel_0.exe" goto :skip_legacy

rem Run utilizing Powershell to capture precise execution time
powershell -Command "$t = Measure-Command { Start-Process -FilePath '.\pffdtd_parallel_0.exe' -ArgumentList 'dipoleTest', 'results\benchmarks\bench_legacy' -RedirectStandardOutput 'results\benchmarks\bench_legacy_log.txt' -Wait -NoNewWindow }; $msg = 'Legacy Time: ' + $t.TotalSeconds + ' seconds'; Write-Output $msg | Tee-Object -FilePath 'results\benchmarks\benchmark_results.txt'"
goto :next_step

:skip_legacy
echo [SKIPPED] pffdtd_parallel_0.exe not found.

:next_step
echo.
echo --------------------------------------------------------
echo.

echo [2/2] Running Benchmark on NEW Executable (pffdtd_parallel.exe)...
if not exist "pffdtd_parallel.exe" goto :skip_new

powershell -Command "$t = Measure-Command { Start-Process -FilePath '.\pffdtd_parallel.exe' -ArgumentList 'dipoleTest', 'results\benchmarks\bench_new' -RedirectStandardOutput 'results\benchmarks\bench_new_log.txt' -Wait -NoNewWindow }; $msg = 'New Time:    ' + $t.TotalSeconds + ' seconds'; Write-Output $msg | Tee-Object -FilePath 'results\benchmarks\benchmark_results.txt' -Append"
goto :end

:skip_new
echo [SKIPPED] pffdtd_parallel.exe not found. Please compile first.

:end
echo.
echo ========================================================
echo Done.
popd
