@echo off
set EXE=pffdtd_parallel.exe
if not exist %EXE% (
    echo Error: %EXE% not found.
    exit /b 1
)

mkdir results\test_freespace
echo Running Free Space Test (No Args)...
%EXE% dipole results\test_freespace\data > results\test_freespace\log.txt 2>&1

echo.
echo Running Plasma Test (With Args)...
mkdir results\test_plasma
%EXE% dipole results\test_plasma\data 5.3 0.0 1.43 > results\test_plasma\log.txt 2>&1

echo.
echo Done. Check logs.
