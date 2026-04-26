@echo off
setlocal
pushd %~dp0..

REM Parameters for Sheath Regime
REM freq_plasma (Hz) = 200e3 (approx for 5e8 density) -> 0.2 MHz
REM freq_collision = 0.1 (guess)
REM freq_cyclotron = 0 (B=0 for now?) or keep existing
REM angle_e = 0
REM angle_a = 0
REM T = 2000 (Kelvin)

if not exist "results\sheath_test" mkdir "results\sheath_test"

REM Create sheath.str from dipole.str with 30 kHz source
powershell -Command "(Get-Content dipole.str) -replace '100000000', '30000' | Set-Content sheath.str"

echo Running Sheath Test...
REM Printing command for verification
echo pffdtd_parallel.exe sheath "results\sheath_test\data" 200000 0.1 0 0 0 2000

REM Run without redirection to see errors
pffdtd_parallel.exe sheath "results\sheath_test\data" 200000 0.1 0 0 0 2000

echo Done.
popd
