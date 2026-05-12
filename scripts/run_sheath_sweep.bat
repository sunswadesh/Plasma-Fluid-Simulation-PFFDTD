@echo off
setlocal
pushd %~dp0..

REM Sheath Width Sweep: Sd = 0, 2, 4, 6, 8, 10 cells
REM Fixed params: fp=200kHz, fcol=0.1, fcyc=0, angles=0, T=2000K

if not exist "results\sheath_sweep" mkdir "results\sheath_sweep"

echo ============================================
echo  Sheath Width Sweep (Sd = 0,2,4,6,8,10)
echo ============================================

for %%S in (0 2 4 6 8 10) do (
    echo.
    echo --- Running Sd=%%S ---
    if not exist "results\sheath_sweep\sd%%S" mkdir "results\sheath_sweep\sd%%S"
    pffdtd_parallel.exe sheath "results\sheath_sweep\sd%%S\data" 200000 0.1 0 0 0 2000 %%S
    if errorlevel 1 (
        echo ERROR: Sd=%%S failed!
    ) else (
        echo OK: Sd=%%S completed.
    )
)

echo.
echo ============================================
echo  Sweep Complete. Results in results\sheath_sweep\
echo ============================================

popd
endlocal
