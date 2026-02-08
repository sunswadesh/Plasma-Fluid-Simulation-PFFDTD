@echo off
setlocal
pushd %~dp0..

if "%~1"=="" (
    echo Usage: run_simulation.bat [RunName] [F_plasma] [F_collision] [F_cyclotron] ...
    echo Example: run_simulation.bat run_test 5.3 0.0 1.43
    popd
    exit /b 1
)

set RUN_NAME=%~1
set OUT_DIR=results\%RUN_NAME%

if not exist "results" mkdir "results"
if not exist "%OUT_DIR%" mkdir "%OUT_DIR%"

echo ==========================================
echo Starting Simulation: %RUN_NAME%
echo Output Directory: %OUT_DIR%
echo Logging to: %OUT_DIR%\simulation.log
echo ==========================================

REM Check if parallel exe exists, else use serial
if exist "pffdtd_parallel.exe" (
    set EXE=pffdtd_parallel.exe
    echo Using Parallel Executable
) else (
    set EXE=pffdtd_serial.exe
    echo Using Serial Executable
)

echo Start Time: %TIME% > "%OUT_DIR%\simulation.log"
REM Pass all additional arguments (%2, %3...) to the executable
REM Usage: run_simulation.bat RunName [F_p] [F_col] [F_c] [Ang_E] [Ang_A] [T]
%EXE% dipole "%OUT_DIR%\data" %2 %3 %4 %5 %6 %7 %8 %9 >> "%OUT_DIR%\simulation.log" 2>&1
echo End Time: %TIME% >> "%OUT_DIR%\simulation.log"

echo Simulation Complete.
echo Plotting Results...

python visualization/plot_voltage.py "%OUT_DIR%\data.vc" --save "%OUT_DIR%\impedance_plot.png"

echo Done. Results in %OUT_DIR%
popd
