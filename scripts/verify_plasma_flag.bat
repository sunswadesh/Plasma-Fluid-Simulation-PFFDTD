@echo off
pushd %~dp0..

set EXE=pffdtd_parallel.exe
if not exist %EXE% (
    echo Error: %EXE% not found.
    popd
    exit /b 1
)

echo Running Free Space Test (No Args)...
mkdir results\test_freespace 2>nul
%EXE% dipole results\test_freespace\data > results\test_freespace\log.txt 2>&1

echo.
echo Running Plasma Test (With Args)...
mkdir results\test_plasma 2>nul
%EXE% dipole results\test_plasma\data 5.3 0.0 1.43 > results\test_plasma\log.txt 2>&1

echo.
echo Done. Check logs in results\test_freespace and results\test_plasma.
popd
